"""Friend farm operations - visit, help, steal"""

import asyncio
from typing import List, Dict, Any, Optional

from .config import Config
from .proto import types
from .network import get_network_client
from .utils import to_long, log, log_warn, sleep


class FriendOperations:
    """Friend farm operations manager"""
    
    HELP_ONLY_WITH_EXP = True  # Only help friends when it gives experience
    ENABLE_PUT_BAD_THINGS = False  # Whether to enable putting weeds/insects
    
    def __init__(self):
        self.network = get_network_client()
        self.is_checking = False
        self.check_task: Optional[asyncio.Task] = None
        self.running = False
        self.operation_limits: Dict[str, Any] = {}
    
    def update_operation_limits(self, limits: Dict[str, Any]):
        """Update operation limits"""
        self.operation_limits = limits
    
    async def get_friend_list(self) -> Dict[str, Any]:
        """Get friend list"""
        body = b''  # Placeholder
        reply = await self.network.send_msg_async(
            'gamepb.friendpb.FriendService',
            'GetFriendList',
            body
        )
        return reply
    
    async def enter_friend_farm(self, friend_gid: int) -> Dict[str, Any]:
        """Enter friend's farm"""
        body = b''  # Placeholder
        reply = await self.network.send_msg_async(
            'gamepb.visitpb.VisitService',
            'EnterFriendFarm',
            body
        )
        return reply
    
    async def steal(self, friend_gid: int, land_ids: List[int]) -> Dict[str, Any]:
        """Steal crops from friend"""
        body = b''  # Placeholder
        reply = await self.network.send_msg_async(
            'gamepb.visitpb.VisitService',
            'Steal',
            body
        )
        return reply
    
    async def help_friend_water(self, friend_gid: int, land_ids: List[int]) -> Dict[str, Any]:
        """Help friend water lands"""
        body = b''  # Placeholder
        reply = await self.network.send_msg_async(
            'gamepb.visitpb.VisitService',
            'HelpWater',
            body
        )
        return reply
    
    async def help_friend_weed(self, friend_gid: int, land_ids: List[int]) -> Dict[str, Any]:
        """Help friend remove weeds"""
        body = b''  # Placeholder
        reply = await self.network.send_msg_async(
            'gamepb.visitpb.VisitService',
            'HelpWeedOut',
            body
        )
        return reply
    
    async def help_friend_insecticide(self, friend_gid: int, land_ids: List[int]) -> Dict[str, Any]:
        """Help friend remove insects"""
        body = b''  # Placeholder
        reply = await self.network.send_msg_async(
            'gamepb.visitpb.VisitService',
            'HelpInsecticide',
            body
        )
        return reply
    
    async def visit_friend_farm(self, friend_gid: int, friend_name: str):
        """Visit a friend's farm and perform operations"""
        try:
            # Enter friend's farm
            farm_reply = await self.enter_friend_farm(friend_gid)
            
            # Mock implementation for demonstration
            # In production: analyze friend's lands and perform operations
            
            mature_lands = []  # Mature crops to steal
            weed_lands = []    # Lands with weeds to help
            insect_lands = []  # Lands with insects to help
            water_lands = []   # Lands needing water to help
            
            stolen_count = 0
            helped_water = 0
            helped_weed = 0
            helped_insect = 0
            
            # Steal mature crops
            if mature_lands:
                steal_reply = await self.steal(friend_gid, mature_lands)
                stolen_count = len(mature_lands)
            
            # Help with maintenance
            if weed_lands:
                await self.help_friend_weed(friend_gid, weed_lands)
                helped_weed = len(weed_lands)
            
            if insect_lands:
                await self.help_friend_insecticide(friend_gid, insect_lands)
                helped_insect = len(insect_lands)
            
            if water_lands:
                await self.help_friend_water(friend_gid, water_lands)
                helped_water = len(water_lands)
            
            # Log actions
            actions = []
            if stolen_count > 0:
                actions.append(f'偷{stolen_count}')
            if helped_weed > 0:
                actions.append(f'除草{helped_weed}')
            if helped_insect > 0:
                actions.append(f'除虫{helped_insect}')
            if helped_water > 0:
                actions.append(f'浇水{helped_water}')
            
            if actions:
                log('好友', f'{friend_name}: {"/".join(actions)}')
            
        except Exception as e:
            log_warn('好友', f'访问 {friend_name} 失败: {e}')
    
    async def check_friends(self):
        """Check and visit all friends"""
        if self.is_checking:
            return
        
        self.is_checking = True
        try:
            # Get friend list
            friends_reply = await self.get_friend_list()
            
            # Mock implementation
            # In production: iterate through friends and visit each
            friends = []  # List of {gid, name}
            
            if friends:
                total_stolen = 0
                total_helped = 0
                
                for friend in friends:
                    await self.visit_friend_farm(friend['gid'], friend['name'])
                    await sleep(100)  # Small delay between visits
                
                log('好友', f'巡查完成: 共访问 {len(friends)} 位好友')
            
        except Exception as e:
            log_warn('好友', f'巡查错误: {e}')
        finally:
            self.is_checking = False
    
    async def friend_check_loop(self):
        """Friend check loop"""
        while self.running:
            await self.check_friends()
            await asyncio.sleep(Config.friend_check_interval)
    
    def start_friend_check_loop(self):
        """Start friend check loop"""
        if not self.running:
            self.running = True
            self.check_task = asyncio.create_task(self.friend_check_loop())
            log('好友', '巡查循环已启动')
    
    def stop_friend_check_loop(self):
        """Stop friend check loop"""
        self.running = False
        if self.check_task:
            self.check_task.cancel()
            log('好友', '巡查循环已停止')


# Global instance
friend_operations = FriendOperations()


def get_friend_operations() -> FriendOperations:
    """Get global friend operations instance"""
    return friend_operations
