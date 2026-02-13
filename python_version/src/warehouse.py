"""Warehouse system - automatic fruit selling"""

import asyncio
from typing import Dict, Any, Optional, List

from .proto import types
from .network import get_network_client
from .utils import log, log_warn


class WarehouseSystem:
    """Warehouse system manager"""
    
    def __init__(self):
        self.network = get_network_client()
        self.sell_task: Optional[asyncio.Task] = None
        self.running = False
        self.sell_interval = 60.0  # seconds
    
    async def get_backpack(self) -> Dict[str, Any]:
        """Get backpack/warehouse contents"""
        body = b''  # Placeholder
        reply = await self.network.send_msg_async(
            'gamepb.itempb.ItemService',
            'GetBackpack',
            body
        )
        return reply
    
    async def sell_item(self, item_id: int, count: int) -> Dict[str, Any]:
        """Sell items from backpack"""
        body = b''  # Placeholder
        reply = await self.network.send_msg_async(
            'gamepb.itempb.ItemService',
            'SellItem',
            body
        )
        return reply
    
    async def sell_fruits(self):
        """Sell all fruits in warehouse"""
        try:
            # Get backpack contents
            backpack_reply = await self.get_backpack()
            
            # Mock implementation
            # In production: filter fruit items and sell them
            fruits = []  # List of {item_id, count, name}
            
            if fruits:
                total_gold = 0
                sold_types = 0
                
                for fruit in fruits:
                    try:
                        sell_reply = await self.sell_item(fruit['item_id'], fruit['count'])
                        gold_earned = fruit['count'] * 2  # Mock price
                        total_gold += gold_earned
                        sold_types += 1
                    except Exception as e:
                        log_warn('仓库', f'出售失败: {fruit["name"]}: {e}')
                
                if sold_types > 0:
                    log('仓库', f'出售 {sold_types} 种果实，获得 {total_gold} 金币')
        
        except Exception as e:
            log_warn('仓库', f'出售错误: {e}')
    
    async def sell_loop(self):
        """Automatic selling loop"""
        while self.running:
            await asyncio.sleep(self.sell_interval)
            await self.sell_fruits()
    
    def start_sell_loop(self, interval: float = 60.0):
        """Start automatic selling loop
        
        Args:
            interval: Selling interval in seconds
        """
        if not self.running:
            self.sell_interval = interval
            self.running = True
            self.sell_task = asyncio.create_task(self.sell_loop())
            log('仓库', f'自动出售已启动 (每{int(interval)}秒)')
    
    def stop_sell_loop(self):
        """Stop automatic selling loop"""
        self.running = False
        if self.sell_task:
            self.sell_task.cancel()
            log('仓库', '自动出售已停止')


# Global instance
warehouse_system = WarehouseSystem()


def get_warehouse_system() -> WarehouseSystem:
    """Get global warehouse system instance"""
    return warehouse_system
