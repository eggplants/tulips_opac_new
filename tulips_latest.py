#!/usr/bin/env python3

import asyncio
import json
import os
import sys
import time
import urllib.request
from io import BytesIO
from typing import Any, List, Tuple, TypedDict

import bs4
import pyppeteer
import requests
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
if not os.path.exists(TWEET_LOG_PATH):
    open(TWEET_LOG_PATH, 'w')

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
    """Doctionary contains data of one book.

    Attributes:
        link (str): A link of a detail page of book.
        title (str): Title of book.
        author (str): Author of book.
        publisher (str): Publisher of book.
        isbn (str): ISBN code of book.
        holding (str): Holding location of book.
        status (str): Status of arranging a book.
        imagesrc (str): URL of book image.
    """
    link: str
    title: str
    author: str
    publisher: str
    isbn: str
    holding: str
    status: str
    imagesrc: str


class BookInfo(TypedDict):
    """Doctionary contains data of book.

    Attributes:
        index (int): Index of data of books.
        data (BookData): Data of book.
    """
    index: int
    data: BookData


def connect(host: str = 'http://google.com') -> bool:
    """Check connectivity.

    Args:
        host (str, optional): URL of a site for checking to connect.
        default 'http://google.com'.

    Returns:
        bool: Is it connectable?
    """
    try:
        urllib.request.urlopen(host)
        return True
    except Exception:
        return False


async def getpage() -> str:
    """Get a source code string from tulips's opac page.

    Returns:
        str: Source code of opac page
    """
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
    """Scrape the opac source code and make list of BookInfo.

    Args:
        source (str): Source code of opac page

    Returns:
        List[BookInfo]: List of scraped data of books from opac
    """
    def get_book_info_text(book: bs4.element.Tag, class_: str) -> str:
        """[summary]

        Args:
            book (bs4.element.Tag): An element contains a book info
            class_ (str): Class name of the information to be extracted

        Returns:
            str: Extracted info
        """
        try:
            return book.find('dl', class_=class_).dd.span.text
        except (AttributeError, TypeError):
            return ''

    soup = bs4.BeautifulSoup(source, 'html.parser')
    books: bs4.element.ResultSet = soup.select(
        'div.panel.searchCard.l_searchCard.c_search_card.p_search_card')
    res = []
    default_img = '/bookimage-kango.png'
    for idx, book_d in enumerate(books):
        book = book_d.select_one(
            'div.informationArea.c_information_area.l_informationArea')
        res_i: BookInfo = {'index': idx, 'data': {
            'link': '',
            'title': '',
            'author': '',
            'publisher': '',
            'isbn': '',
            'holding': '',
            'status': '',
            'imagesrc': ''}}
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
        imgsrc = book_d.select_one('img')['src']
        res_i['data']['imagesrc'] = (
            '' if imgsrc[-20:] == default_img else imgsrc)
        res.append(res_i)

    return res


def get_tweeted_list() -> List[str]:
    """Get links of tweeted books from tweet log file.

    Returns:
        List[str]: URL lists of links of tweeted books
    """
    return open(TWEET_LOG_PATH, 'r').read().rstrip().split("\n")


def make_content(data: BookData) -> str:
    """Make a content text of tweet.

    Args:
        data (BookData): data of a book

    Returns:
        str: tweet content
    """
    def shorten(text: str, byte_len: int = 40, encoding: str = 'utf-8') -> str:
        """Shorten a text if a length of a text is longer than given limit.

        Args:
            text (str): text
            byte_len (int, optional): limit of text length. Defaults to 40.
            encoding (str, optional): encoding. Defaults to 'utf-8'.

        Returns:
            str: shortened text
        """
        if len(text.encode(encoding)) <= byte_len:
            return replace_nd(text)
        while len(text.encode(encoding)) > byte_len:
            text = text[:-1]
        else:
            return text + '???'

    def replace_nd(text: str) -> str:
        """Replace blank str to '<no data>'

        Args:
            text (str): text

        Returns:
            str: text or '<no data>' if text is blank
        """
        return ('<no data>' if text == '' else text)

    content = "\n".join([
        "???{date}??????????????????",
        "????: {title}",
        "????: {author}",
        "????: {publisher}",
        "???????: {holding}",
        "????: {link}"])
    return content.format(
        date=DATE_STAMP,
        title=shorten(data['title'], 70),
        author=shorten(data['author'], 40),
        publisher=shorten(data['publisher'], 40),
        holding=shorten(data['holding'], 50),
        link=replace_nd(data['link']))


def make_tweepy_oauth(
        ck: str, cs: str, at: str, as_: str) -> tweepy.API:
    """Make an 0Authed api object from tokens. 

    Args:
        ck (str): twitter customer token
        cs (str): twitter customer secret token
        at (str): twitter access token
        as_ (str): twitter access secret token

    Returns:
        tweepy.API: 0Authed api object
    """
    oauth = tweepy.OAuthHandler(ck, cs)
    oauth.set_access_token(at, as_)
    return tweepy.API(oauth)


def get_imagesrc_to_image(src: str) -> bytes:
    """

    Args:
        src (str): URL of book image

    Returns:
        bytes: image data
    """
    if src == '':
        return b''
    else:
        return requests.get(src).content


def tweet(res: List[BookInfo]) -> None:
    """Post a tweet.

    Args:
        res (List[BookInfo]): data of books
    """
    tweeted_list = get_tweeted_list()
    f = open(TWEET_LOG_PATH, 'a')
    api = make_tweepy_oauth(*KEYS)
    for data in [data['data'] for data in res
                 if data['data']['link'] not in tweeted_list + ['']]:

        content = make_content(data)
        book_img_data = get_imagesrc_to_image(data['imagesrc'])

        if book_img_data != b'':
            status, detail = _tweet(content, api, book_img_data)
        else:
            status, detail = _tweet(content, api)

        if status:
            print(data['link'], file=f)
            print(detail.id, file=sys.stderr)
        else:
            print(detail.reason, file=sys.stderr)

        time.sleep(40)


def _tweet(content: str, api: tweepy.API, img_data: bytes = b'') \
        -> Tuple[bool, Any]:
    """Post a tweet. (helper function for tweet)

    Returns:
        Tuple[bool, Any]: (if tweet is successful) and (tweetobj|errobj)
    """
    try:
        if img_data == b'':
            status = api.update_status(content)
        else:
            result_img = api.media_upload(
                filename='img.png', file=BytesIO(img_data))
            status = api.update_status(
                content, media_ids=[result_img.media_id])

        return (True, status)
    except tweepy.TweepError as e:
        print(content, file=sys.stderr)
        return (False, e)


def get_source(args: List[str]) -> str:
    """Get latest opac source code.

    Read latest cache file if already exist.

    Args:
        args (List[str]): Given args from command line

    Raises:
        FileNotFoundError: If cache file does not exist

    Returns:
        str: source code
    """
    if os.path.exists(SOURCE_NAME):
        fname = (args[0] if len(args) == 1 else SOURCE_NAME)
        if not os.path.exists(fname):
            raise FileNotFoundError("{}: Not found".format(fname))
        else:
            source = open(fname, 'r').read()
    else:
        source = asyncio.get_event_loop().run_until_complete(getpage())
        print(source, file=open(SOURCE_NAME, 'w'))

    return source


if __name__ == '__main__':
    args = sys.argv[1:]
    if '-d' in args:
        DRYRUN = True
        args = [arg for arg in args if arg != '-d']

    if not connect(BASE):
        print('Internet currently not available', file=sys.stderr)
        exit(1)

    source = get_source(args)
    res = scrape(source)
    print(json.dumps(res, indent=True),
          file=open(SOURCE_NAME[:-4]+'json', 'w'))
    if not DRYRUN:
        tweet(res)
