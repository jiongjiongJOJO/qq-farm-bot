"""Configuration constants and enums"""

from enum import IntEnum
from typing import Dict, Any


class Config:
    """Application configuration"""
    
    SERVER_URL = 'wss://gate-obt.nqf.qq.com/prod/ws'
    CLIENT_VERSION = '1.6.0.14_20251224'
    OS = 'iOS'
    
    # Default values (can be overridden)
    platform = 'qq'  # 'qq' or 'wx'
    heartbeat_interval = 25.0  # seconds
    farm_check_interval = 1.0  # seconds (minimum 1s)
    friend_check_interval = 10.0  # seconds (minimum 1s)
    force_lowest_level_crop = False  # Force lowest level crop
    
    @classmethod
    def set_platform(cls, platform: str):
        """Set platform (qq or wx)"""
        cls.platform = platform
    
    @classmethod
    def set_farm_check_interval(cls, seconds: float):
        """Set farm check interval (minimum 1s)"""
        cls.farm_check_interval = max(seconds, 1.0)
    
    @classmethod
    def set_friend_check_interval(cls, seconds: float):
        """Set friend check interval (minimum 1s)"""
        cls.friend_check_interval = max(seconds, 1.0)


class PlantPhase(IntEnum):
    """Plant growth phases"""
    UNKNOWN = 0
    SEED = 1
    GERMINATION = 2
    SMALL_LEAVES = 3
    LARGE_LEAVES = 4
    BLOOMING = 5
    MATURE = 6
    DEAD = 7


# Phase names in Chinese
PHASE_NAMES = ['未知', '种子', '发芽', '小叶', '大叶', '开花', '成熟', '枯死']

# Runtime hint (encoded)
RUNTIME_HINT_MASK = 23
RUNTIME_HINT_DATA = [
    12295, 22759, 26137, 12294, 26427, 39022, 30457, 24343, 28295, 20826,
    36142, 65307, 20018, 31126, 20485, 21313, 12309, 35808, 20185, 20859,
    24343, 20164, 24196, 20826, 36142, 33696, 21441, 12309,
]
