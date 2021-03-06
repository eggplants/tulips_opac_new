import asyncio
import logging
from pyee import EventEmitter as EventEmitter
from pyppeteer.connection import CDPSession as CDPSession
from pyppeteer.errors import ElementHandleError as ElementHandleError, TimeoutError as TimeoutError
from typing import Any, Awaitable, Callable, Dict, List

logger: Any

def debugError(_logger: logging.Logger, msg: Any) -> None: ...
def evaluationString(fun: str, *args: Any) -> str: ...
def getExceptionMessage(exceptionDetails: dict) -> str: ...
def addEventListener(emitter: EventEmitter, eventName: str, handler: Callable) -> Dict[str, Any]: ...
def removeEventListeners(listeners: List[dict]) -> None: ...

unserializableValueMap: Any

def valueFromRemoteObject(remoteObject: Dict) -> Any: ...
def releaseObject(client: CDPSession, remoteObject: dict) -> Awaitable: ...
def waitForEvent(emitter: EventEmitter, eventName: str, predicate: Callable[[Any], bool], timeout: float, loop: asyncio.AbstractEventLoop) -> Awaitable: ...
def get_positive_int(obj: dict, name: str) -> int: ...
def is_jsfunc(func: str) -> bool: ...
