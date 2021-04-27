#!/usr/bin/env python3

import asyncio
import json
import os
import sys
import time
import urllib.request
from typing import Any, List, Tuple, TypedDict

import bs4
import pyppeteer
import tweepy
from dotenv import load_dotenv

PWD = os.path.dirname(__file__)

os.environ['TZ'] = 'Asia/Tokyo'
time.tzset()
DATE_STAMP = time.strftime('%Y-%m-%d')

SOURCE_PATH = os.path.join(PWD, 'source')
os.makedirs(SOURCE_PATH, exist_ok=True)

SOURCE_NAME = os.path.join(SOURCE_PATH, DATE_STAMP + '.html')

TWEET_LOG_PATH = os.path.join(PWD, 'tweet.log')
open(TWEET_LOG_PATH, 'w')  # touch

load_dotenv(os.path.join(PWD, '.twitter.keys'))
KEYS = (
    os.getenv('CONSUMER_KEY', ''),
    os.getenv('CONSUMER_SECRET', ''),
    os.getenv('ACCESS_TOKEN', ''),
    os.getenv('ACCESS_TOKEN_SECRET', ''))

BASE = 'https://www.tulips.tsukuba.ac.jp'
QUERY = {
    'arrivedwithin': '1',
    'type%5B%5D': 'book',
    'target': 'local',
    'searchmode': 'complex',
    'count': '100'}

DRYRUN = False

class BookData(TypedDict):
    link: str
    title: str
    author: str
    publisher: str
    isbn: str
    holding: str
    status: str


class BookInfo(TypedDict):
    index: int
    data: BookData


def connect(host: str = 'http://google.com') -> bool:
    try:
        urllib.request.urlopen(host)
        return True
    except Exception:
        return False


async def getpage() -> str:
    browser = await pyppeteer.launch(
        # headless=False
    )
    page = await browser.newPage()
    await page.goto(
        BASE + '/opac/search?' + '&'.join(
            [f'{k}={v}' for k, v in QUERY.items()]),
        {'waitUntil': 'networkidle0'})
    cont = await page.content()
    await browser.close()
    return cont


def scrape(source: str) -> List[BookInfo]:
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
        res_i: BookInfo = {'index': idx, 'data': {
            'link': '',
            'title': '',
            'author': '',
            'publisher': '',
            'isbn': '',
            'holding': '',
            'status': ''}}
        res_i['data']['link'] = BASE + book.h3.a.get('href')
        res_i['data']['title'] = book.h3.a.text
        res_i['data']['author'] = get_book_info_text(
            book, 'l_detail_info_au_book')
        res_i['data']['publisher'] = get_book_info_text(
            book, 'l_detail_info_pu')
        res_i['data']['isbn'] = get_book_info_text(
            book, 'l_detail_info_sb')
        res_i['data']['holding'] = get_book_info_text(
            book, 'l_detail_info_hd')
        res_i['data']['status'] = get_book_info_text(
            book, 'l_detail_info_st')
        res.append(res_i)
    return res


def get_tweeted_list() -> List[str]:
    return open(TWEET_LOG_PATH, 'r').read().rstrip().split("\n")


def make_content(data: BookData) -> str:
    content = "\n".join([
        "{date}の新刊: {title}({author}, {publisher})",
        "場所: {holding}({status})\n"
        "詳細情報: {link}"])
    return content.format(
        date=DATE_STAMP,
        title=data['title'],
        author=data['author'],
        publisher=data['publisher'],
        holding=data['holding'],
        status=data['status'],
        link=data['link'])


def make_tweepy_oauth(
        ck: str, cs: str, at: str, as_: str) -> tweepy.API:
    oauth = tweepy.OAuthHandler(ck, cs)
    oauth.set_access_token(at, as_)
    return tweepy.API(oauth)


def tweet(res: List[BookInfo]) -> None:
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

# Union[tweepy.Status, tweepy.TweepError]


def _tweet(content: str, api: tweepy.API) -> Tuple[bool, Any]:
    try:
        status = api.update_status(content)
        return (True, status)
    except tweepy.TweepError as e:
        return (False, e)


if __name__ == '__main__':
    args = sys.argv[1:]
    if '-d' in args:
        DRYRUN = True
        args = [arg for arg in args if arg != '-d']

    if not connect(BASE):
        print('Internet currently not available', file=sys.stderr)
        exit(1)

    if os.path.exists(SOURCE_NAME):
        fname = (args[0] if len(args) == 1 else SOURCE_NAME)
        if not os.path.exists(fname):
            raise FileNotFoundError("{}: Not found".format(fname))
        else:
            source = open(fname, 'r').read()
    else:
        source = asyncio.get_event_loop().run_until_complete(getpage())
        print(source, file=open(SOURCE_NAME, 'w'))

    res = scrape(source)
    print(json.dumps(res, indent=True),
          file=open(SOURCE_NAME[:-4]+'json', 'w'))
    if not DRYRUN:
        tweet(res)
