"""Utility functions"""

import asyncio
import time
from datetime import datetime
from typing import Union, Any
from .config import RUNTIME_HINT_MASK, RUNTIME_HINT_DATA


class ServerTimeSync:
    """Server time synchronization"""
    
    _server_time_offset = 0.0
    
    @classmethod
    def sync_time(cls, server_timestamp: int):
        """Sync with server time"""
        local_time = time.time()
        cls._server_time_offset = server_timestamp - local_time
    
    @classmethod
    def get_server_time(cls) -> float:
        """Get current server time"""
        return time.time() + cls._server_time_offset
    
    @classmethod
    def get_server_time_sec(cls) -> int:
        """Get current server time in seconds"""
        return int(cls.get_server_time())


def to_long(value: Union[int, str]) -> int:
    """Convert value to long integer"""
    if isinstance(value, str):
        return int(value)
    return int(value)


def to_num(value: Any) -> int:
    """Convert value to number"""
    if hasattr(value, 'toInt'):
        return value.toInt()
    if isinstance(value, str):
        return int(value)
    return int(value)


def to_time_sec(timestamp: Union[int, float]) -> int:
    """Convert timestamp to seconds"""
    return int(timestamp)


def log(tag: str, message: str):
    """Log message with tag"""
    now = datetime.now().strftime('%H:%M:%S')
    print(f'[{now}] [{tag}] {message}')


def log_warn(tag: str, message: str):
    """Log warning message"""
    now = datetime.now().strftime('%H:%M:%S')
    print(f'[{now}] [警告:{tag}] {message}')


async def sleep(milliseconds: float):
    """Sleep for milliseconds"""
    await asyncio.sleep(milliseconds / 1000.0)


def emit_runtime_hint(show: bool):
    """Emit runtime hint"""
    if show:
        hint = ''.join(chr(code ^ RUNTIME_HINT_MASK) for code in RUNTIME_HINT_DATA)
        print(hint)


def format_time(timestamp: int) -> str:
    """Format timestamp to readable time"""
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime('%Y/%m/%d %H:%M:%S')
