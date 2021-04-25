from pyppeteer import helper as helper
from pyppeteer.errors import TimeoutError as TimeoutError
from pyppeteer.frame_manager import Frame as Frame, FrameManager as FrameManager
from pyppeteer.util import merge_dict as merge_dict
from typing import Any, Dict

class NavigatorWatcher:
    def __init__(self, frameManager: FrameManager, frame: Frame, timeout: int, options: Dict=..., **kwargs: Any): ...
    def navigationPromise(self) -> Any: ...
    def cancel(self) -> None: ...

pyppeteerToProtocolLifecycle: Any
