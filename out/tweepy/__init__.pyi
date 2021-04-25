from tweepy.api import API as API
from tweepy.auth import AppAuthHandler as AppAuthHandler, OAuthHandler as OAuthHandler
from tweepy.cache import Cache as Cache, FileCache as FileCache, MemoryCache as MemoryCache
from tweepy.cursor import Cursor as Cursor
from tweepy.error import RateLimitError as RateLimitError, TweepError as TweepError
from tweepy.models import DirectMessage as DirectMessage, Friendship as Friendship, ModelFactory as ModelFactory, SavedSearch as SavedSearch, SearchResults as SearchResults, Status as Status, User as User
from tweepy.streaming import Stream as Stream, StreamListener as StreamListener
from typing import Any

api: Any

def debug(enable: bool = ..., level: int = ...) -> None: ...
