from requests.auth import AuthBase
from tweepy.api import API as API
from tweepy.error import TweepError as TweepError
from typing import Any, Optional

WARNING_MESSAGE: str
log: Any

class AuthHandler:
    def apply_auth(self, url: Any, method: Any, headers: Any, parameters: Any) -> None: ...
    def get_username(self) -> None: ...

class OAuthHandler(AuthHandler):
    OAUTH_HOST: str = ...
    OAUTH_ROOT: str = ...
    consumer_key: Any = ...
    consumer_secret: Any = ...
    access_token: Any = ...
    access_token_secret: Any = ...
    callback: Any = ...
    username: Any = ...
    request_token: Any = ...
    oauth: Any = ...
    def __init__(self, consumer_key: Any, consumer_secret: Any, callback: Optional[Any] = ...) -> None: ...
    def apply_auth(self): ...
    def set_access_token(self, key: Any, secret: Any) -> None: ...
    def get_authorization_url(self, signin_with_twitter: bool = ..., access_type: Optional[Any] = ...): ...
    def get_access_token(self, verifier: Optional[Any] = ...): ...
    def get_xauth_access_token(self, username: Any, password: Any): ...
    def get_username(self): ...

class OAuth2Bearer(AuthBase):
    bearer_token: Any = ...
    def __init__(self, bearer_token: Any) -> None: ...
    def __call__(self, request: Any): ...

class AppAuthHandler(AuthHandler):
    OAUTH_HOST: str = ...
    OAUTH_ROOT: str = ...
    consumer_key: Any = ...
    consumer_secret: Any = ...
    def __init__(self, consumer_key: Any, consumer_secret: Any) -> None: ...
    def apply_auth(self): ...
