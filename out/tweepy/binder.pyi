from tweepy.error import RateLimitError as RateLimitError, TweepError as TweepError, is_rate_limit_error_message as is_rate_limit_error_message
from tweepy.models import Model as Model
from tweepy.utils import convert_to_utf8_str as convert_to_utf8_str
from typing import Any

re_path_template: Any
log: Any

def bind_api(**config: Any): ...
