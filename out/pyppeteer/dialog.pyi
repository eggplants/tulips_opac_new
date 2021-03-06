from pyppeteer.connection import CDPSession as CDPSession
from typing import Any

class Dialog:
    Type: Any = ...
    def __init__(self, client: CDPSession, type: str, message: str, defaultValue: str=...) -> None: ...
    @property
    def type(self) -> str: ...
    @property
    def message(self) -> str: ...
    @property
    def defaultValue(self) -> str: ...
    async def accept(self, promptText: str=...) -> None: ...
    async def dismiss(self) -> None: ...
