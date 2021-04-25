from pyppeteer.connection import CDPSession as CDPSession
from pyppeteer.util import merge_dict as merge_dict
from typing import Any

class Tracing:
    def __init__(self, client: CDPSession) -> None: ...
    async def start(self, options: dict=..., **kwargs: Any) -> None: ...
    async def stop(self) -> str: ...
