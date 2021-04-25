from tweepy.error import TweepError as TweepError
from tweepy.parsers import ModelParser as ModelParser, RawParser as RawParser
from typing import Any

class Cursor:
    iterator: Any = ...
    def __init__(self, method: Any, *args: Any, **kwargs: Any) -> None: ...
    def pages(self, limit: int = ...): ...
    def items(self, limit: int = ...): ...

class BaseIterator:
    method: Any = ...
    args: Any = ...
    kwargs: Any = ...
    limit: int = ...
    def __init__(self, method: Any, *args: Any, **kwargs: Any) -> None: ...
    def __next__(self): ...
    def next(self) -> None: ...
    def prev(self) -> None: ...
    def __iter__(self) -> Any: ...

class CursorIterator(BaseIterator):
    next_cursor: Any = ...
    prev_cursor: Any = ...
    num_tweets: int = ...
    def __init__(self, method: Any, *args: Any, **kwargs: Any) -> None: ...
    def next(self): ...
    def prev(self): ...

class DMCursorIterator(BaseIterator):
    next_cursor: Any = ...
    page_count: int = ...
    def __init__(self, method: Any, *args: Any, **kwargs: Any) -> None: ...
    def next(self): ...
    def prev(self) -> None: ...

class IdIterator(BaseIterator):
    max_id: Any = ...
    num_tweets: int = ...
    results: Any = ...
    model_results: Any = ...
    index: int = ...
    def __init__(self, method: Any, *args: Any, **kwargs: Any) -> None: ...
    def next(self): ...
    def prev(self): ...

class PageIterator(BaseIterator):
    current_page: int = ...
    def __init__(self, method: Any, *args: Any, **kwargs: Any) -> None: ...
    def next(self): ...
    def prev(self): ...

class ItemIterator(BaseIterator):
    page_iterator: Any = ...
    limit: int = ...
    current_page: Any = ...
    page_index: int = ...
    num_tweets: int = ...
    def __init__(self, page_iterator: Any) -> None: ...
    def next(self): ...
    def prev(self): ...
