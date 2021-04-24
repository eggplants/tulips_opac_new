#!/usr/bin/env python3

import pyppeteer as p
import asyncio
import json
import urllib.request
import os, time, sys

import tweepy
from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv

os.environ['TZ'] = 'Asia/Tokyo'
time.tzset()
DATE_STAMP = time.strftime('%Y-%m-%d')

SOURCE_PATH = os.path.join(os.path.dirname(__file__), 'source')
os.makedirs(SOURCE_PATH, exist_ok=True)

SOURCE_NAME = os.path.join(SOURCE_PATH, DATE_STAMP + '.html')

TWEET_LOG_PATH = os.path.join(os.path.dirname(__file__), 'tweet.log')
open(TWEET_LOG_PATH, 'w') # touch

load_dotenv('.twitter.keys')
CK = os.getenv('CONSUMER_KEY')
CS = os.getenv('CONSUMER_SECRET')
AT = os.getenv('ACCESS_TOKEN')
AS = os.getenv('ACCESS_TOKEN_SECRET')
KEYS = (CK, CS, AT, AS)

BASE = 'https://www.tulips.tsukuba.ac.jp'
QUERY = {
  'arrivedwithin': '1',
  'type%5B%5D': 'book',
  'target': 'local',
  'searchmode': 'complex',
  'count': '100'
}

def connect(host='http://google.com'):
  try:
    urllib.request.urlopen(host)
    return True
  except:
    return False

async def getpage():
  b    = await p.launch(
                 # headless=False
               )
  pg   = await b.newPage()
  r    = await pg.goto(
    BASE + '/opac/search?' + '&'.join(
      [f'{k}={v}' for k,v in QUERY.items()]),
      {'waitUntil':'networkidle0'})
  cont = await pg.content()
  await b.close()
  return cont

def scrape(source):
  def get_book_info_text(book, class_):
    try:
      return book.find('dl', class_=class_).dd.span.text
    except (AttributeError, TypeError):
      return ''

  soup = bs(source, 'html.parser')
  books = soup.select('div.informationArea.c_information_area.l_informationArea')
  res = {}
  for ind, book in enumerate(books):
    res[ind] = {}
    res[ind]['link'] = BASE + book.h3.a.get('href')
    res[ind]['title'] = book.h3.a.text
    res[ind]['author'] = get_book_info_text(book, 'l_detail_info_au_book')
    res[ind]['publisher'] = get_book_info_text(book, 'l_detail_info_au_pu')
    res[ind]['isbn'] = get_book_info_text(book, 'l_detail_info_au_sb')
    res[ind]['holding'] = get_book_info_text(book, 'l_detail_info_au_hd')
    res[ind]['status'] = get_book_info_text(book, 'l_detail_info_au_st')

  return res

def get_tweeted_list():
  return open(TWEET_LOG_PATH, 'r').read().rstrip().split("\n")

def make_content(data):
  content =  "\n".join([
    "{date}の新刊: {title}({author}, {publisher})",
    "場所: {location}({status})\n"
    "詳細情報: {link}"])
  return content.format(
      date=DATE_STAMP,
      title=data['title'],
      publisher=data['publisher'],
      location=data['location'],
      status=data['status'],
      link=data['link'])

def make_tweepy_oauth(ck, cs, at, as_):
  return tweepy.OAuthHandler(ck, cs).set_access_token(at, as_)

def tweet(res):
  tweeted_list = get_tweeted_list()
  f = open(TWEET_LOG_PATH, 'a')
  auth = make_tweepy_oauth(*KEYS)
  api = tweepy.API(auth)
  for data in [data for data in res.values()
         if data['link'] not in tweeted_list + ['']]:
    content = make_content(data)
    res, status = _tweet(content, api)
    if res:
      print(data['link'], file=f)
      print(status.id, file=sys.stderr)
    else:
      print(status.reason, file=sys.stderr)

    time.sleep(40)

def _tweet(content, api):
  try:
    status = api.update_status(content)
    return tuple([True, status])
  except tweepy.TweepError as e:
    return tuple([False, e])

if __name__ == '__main__':
  if not connect(BASE):
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
  # print(json.dumps(res, indent=True), file=sys.stderr)
