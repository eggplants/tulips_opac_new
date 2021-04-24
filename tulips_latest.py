#!/usr/bin/env python3

import asyncio
import json
import os
import sys
import time
import urllib.request
from typing import List, Tuple, TypedDict, Union

import bs4
import pyppeteer as p
import tweepy
from dotenv import load_dotenv

os.environ['TZ'] = 'Asia/Tokyo'
time.tzset()
DATE_STAMP = time.strftime('%Y-%m-%d')

SOURCE_PATH = os.path.join(os.path.dirname(__file__), 'source')
os.makedirs(SOURCE_PATH, exist_ok=True)

SOURCE_NAME = os.path.join(SOURCE_PATH, DATE_STAMP + '.html')

TWEET_LOG_PATH = os.path.join(os.path.dirname(__file__), 'tweet.log')
open(TWEET_LOG_PATH, 'w')  # touch

load_dotenv('.twitter.keys')
CK = os.getenv('CONSUMER_KEY', '')
CS = os.getenv('CONSUMER_SECRET', '')
AT = os.getenv('ACCESS_TOKEN', '')
AS = os.getenv('ACCESS_TOKEN_SECRET', '')
KEYS = (CK, CS, AT, AS)

BASE = 'https://www.tulips.tsukuba.ac.jp'
QUERY = {
    'arrivedwithin': '1',
    'type%5B%5D': 'book',
    'target': 'local',
    'searchmode': 'complex',
    'count': '100'
}


class BookInfo(TypedDict):
    link: str
    title: str
    author: str
    publisher: str
    isbn: str
    holding: str
    status: str


class BookInfos(TypedDict):
    index: int
    data: BookInfo


def connect(host: str = 'http://google.com') -> bool:
    try:
        urllib.request.urlopen(host)
        return True
    except Exception:
        return False


async def getpage() -> str:
    b = await p.launch(
        # headless=False
    )
    pg = await b.newPage()
    await pg.goto(
        BASE + '/opac/search?' + '&'.join(
            [f'{k}={v}' for k, v in QUERY.items()]),
        {'waitUntil': 'networkidle0'})
    cont = await pg.content()
    await b.close()
    return cont


def scrape(source: str) -> List[BookInfos]:
    def get_book_info_text(book: bs4.element.Tag, class_: str) -> str:
        try:
            return book.find('dl', class_=class_).dd.span.text
        except (AttributeError, TypeError):
            return ''

    soup = bs4.BeautifulSoup(source, 'html.parser')
    books: bs4.element.ResultSet = soup.select(
        'div.informationArea.c_information_area.l_informationArea')
    res = []
    for idx, book in enumerate(books):
        res_i = {'index': idx, 'data': {}}
        res_i['data']['link'] = BASE + book.h3.a.get('href')
        res_i['data']['title'] = book.h3.a.text
        res_i['data']['author'] = get_book_info_text(
            book, 'l_detail_info_au_book')
        res_i['data']['publisher'] = get_book_info_text(
            book, 'l_detail_info_au_pu')
        res_i['data']['isbn'] = get_book_info_text(
            book, 'l_detail_info_au_sb')
        res_i['data']['holding'] = get_book_info_text(
            book, 'l_detail_info_au_hd')
        res_i['data']['status'] = get_book_info_text(
            book, 'l_detail_info_au_st')
        res.append(res_i)
    return res


def get_tweeted_list() -> List[str]:
    return open(TWEET_LOG_PATH, 'r').read().rstrip().split("\n")


def make_content(data: BookInfo) -> str:
    content = "\n".join([
        "{date}の新刊: {title}({author}, {publisher})",
        "場所: {holding}({status})\n"
        "詳細情報: {link}"])
    return content.format(
        date=DATE_STAMP,
        title=data['title'],
        publisher=data['publisher'],
        holding=data['holding'],
        status=data['status'],
        link=data['link'])


def make_tweepy_oauth(
        ck: str, cs: str, at: str, as_: str) -> tweepy.API:
    oauth = tweepy.OAuthHandler(ck, cs)
    oauth.set_access_token(at, as_)
    return tweepy.API(oauth)


def tweet(res: List[BookInfos]) -> None:
    tweeted_list = get_tweeted_list()
    f = open(TWEET_LOG_PATH, 'a')
    api = make_tweepy_oauth(*KEYS)
    for data in [data['data'] for data in res
                 if data['data']['link'] not in tweeted_list + ['']]:
        content = make_content(data)
        status, detail = _tweet(content, api)
        if status:
            print(data['link'], file=f)
            print(detail.id, file=sys.stderr)
        else:
            print(detail.reason, file=sys.stderr)

        time.sleep(40)


def _tweet(content: str, api: tweepy.API) \
        -> Tuple[bool, Union[tweepy.Status, tweepy.TweepError]]:
    try:
        status = api.update_status(content)
        return (True, status)
    except tweepy.TweepError as e:
        return (False, e)


if __name__ == '__main__':
    if not connect(BASE):
        print('Internet currentry not available', file=sys.stderr)
        exit(1)

    if os.path.exists(SOURCE_NAME):
        fname = (sys.argv[1] if len(sys.argv) > 1 else SOURCE_NAME)
        if not os.path.exists(fname):
            raise FileNotFoundError("{}: Not found".format(fname))
        else:
            source = open(fname, 'r').read()
    else:
        source = asyncio.get_event_loop().run_until_complete(getpage())
        print(source, file=open(SOURCE_NAME, 'w'))

    res = scrape(source)
    tweet(res)
    print(json.dumps(res, indent=True), file=sys.stderr)
