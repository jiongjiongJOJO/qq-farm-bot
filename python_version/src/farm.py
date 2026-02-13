"""Farm operations - harvest, water, weed, insect control, plant, fertilize"""

import asyncio
from typing import List, Dict, Any, Optional

from .config import Config, PlantPhase
from .proto import types
from .network import get_network_client
from .utils import to_long, to_num, log, log_warn, sleep


class FarmOperations:
    """Farm operations manager"""
    
    NORMAL_FERTILIZER_ID = 1011
    
    def __init__(self):
        self.network = get_network_client()
        self.is_checking = False
        self.is_first_check = True
        self.check_task: Optional[asyncio.Task] = None
        self.running = False
        self.operation_limits_callback: Optional[callable] = None
    
    def set_operation_limits_callback(self, callback: callable):
        """Set callback for operation limits update"""
        self.operation_limits_callback = callback
    
    async def get_all_lands(self) -> Dict[str, Any]:
        """Get all land information"""
        # In production: encode AllLandsRequest and send
        body = b''  # Placeholder
        reply = await self.network.send_msg_async(
            'gamepb.plantpb.PlantService', 
            'AllLands', 
            body
        )
        
        # Update operation limits if callback is set
        if self.operation_limits_callback and 'operation_limits' in reply:
            self.operation_limits_callback(reply['operation_limits'])
        
        return reply
    
    async def harvest(self, land_ids: List[int]) -> Dict[str, Any]:
        """Harvest crops from lands"""
        state = self.network.get_user_state()
        # In production: encode HarvestRequest with land_ids, host_gid, is_all
        body = b''  # Placeholder
        reply = await self.network.send_msg_async(
            'gamepb.plantpb.PlantService',
            'Harvest',
            body
        )
        return reply
    
    async def water_land(self, land_ids: List[int]) -> Dict[str, Any]:
        """Water lands"""
        state = self.network.get_user_state()
        body = b''  # Placeholder
        reply = await self.network.send_msg_async(
            'gamepb.plantpb.PlantService',
            'WaterLand',
            body
        )
        return reply
    
    async def weed_out(self, land_ids: List[int]) -> Dict[str, Any]:
        """Remove weeds from lands"""
        state = self.network.get_user_state()
        body = b''  # Placeholder
        reply = await self.network.send_msg_async(
            'gamepb.plantpb.PlantService',
            'WeedOut',
            body
        )
        return reply
    
    async def insecticide(self, land_ids: List[int]) -> Dict[str, Any]:
        """Remove insects from lands"""
        state = self.network.get_user_state()
        body = b''  # Placeholder
        reply = await self.network.send_msg_async(
            'gamepb.plantpb.PlantService',
            'Insecticide',
            body
        )
        return reply
    
    async def fertilize(self, land_ids: List[int], fertilizer_id: int = NORMAL_FERTILIZER_ID) -> int:
        """Fertilize lands (must be done one by one)
        
        Returns:
            Number of successfully fertilized lands
        """
        success_count = 0
        for land_id in land_ids:
            try:
                body = b''  # Placeholder
                await self.network.send_msg_async(
                    'gamepb.plantpb.PlantService',
                    'Fertilize',
                    body
                )
                success_count += 1
            except Exception as e:
                # Stop if fertilizer runs out
                break
            
            if len(land_ids) > 1:
                await sleep(50)  # 50ms interval
        
        return success_count
    
    async def remove_plant(self, land_ids: List[int]) -> Dict[str, Any]:
        """Remove dead plants"""
        state = self.network.get_user_state()
        body = b''  # Placeholder
        reply = await self.network.send_msg_async(
            'gamepb.plantpb.PlantService',
            'RemovePlant',
            body
        )
        return reply
    
    async def plant_seed(self, land_ids: List[int], seed_id: int) -> Dict[str, Any]:
        """Plant seeds on lands"""
        state = self.network.get_user_state()
        body = b''  # Placeholder
        reply = await self.network.send_msg_async(
            'gamepb.plantpb.PlantService',
            'PlantSeed',
            body
        )
        return reply
    
    async def get_shop(self) -> Dict[str, Any]:
        """Get shop information"""
        body = b''  # Placeholder
        reply = await self.network.send_msg_async(
            'gamepb.shoppb.ShopService',
            'GetShop',
            body
        )
        return reply
    
    async def buy_seeds(self, seed_id: int, count: int) -> Dict[str, Any]:
        """Buy seeds from shop"""
        body = b''  # Placeholder
        reply = await self.network.send_msg_async(
            'gamepb.shoppb.ShopService',
            'Buy',
            body
        )
        return reply
    
    async def check_farm(self):
        """Check and manage farm"""
        if self.is_checking:
            return
        
        self.is_checking = True
        try:
            # Get all lands
            lands_reply = await self.get_all_lands()
            
            # Mock implementation for demonstration
            # In production: analyze lands and perform operations
            
            if self.is_first_check:
                log('农场', '开始巡查')
                self.is_first_check = False
            
            # Categorize lands
            mature_lands = []  # Ready to harvest
            dead_lands = []    # Dead plants to remove
            weed_lands = []    # Lands with weeds
            insect_lands = []  # Lands with insects
            water_lands = []   # Lands needing water
            empty_lands = []   # Empty lands ready to plant
            
            # Process operations based on categorization
            # 1. Harvest mature crops
            if mature_lands:
                await self.harvest(mature_lands)
                log('农场', f'收获 {len(mature_lands)} 块地')
            
            # 2. Remove dead plants
            if dead_lands:
                await self.remove_plant(dead_lands)
                log('农场', f'铲除 {len(dead_lands)} 块地')
            
            # 3. Plant seeds on empty lands
            if empty_lands:
                # Choose best seed (would use calc_exp_yield in production)
                seed_id = 1001  # Placeholder
                await self.buy_seeds(seed_id, len(empty_lands))
                await self.plant_seed(empty_lands, seed_id)
                log('农场', f'种植 {len(empty_lands)} 块地')
                
                # Fertilize newly planted lands
                fertilized = await self.fertilize(empty_lands)
                if fertilized > 0:
                    log('施肥', f'已为 {fertilized}/{len(empty_lands)} 块地施肥')
            
            # 4. Maintenance operations
            if weed_lands:
                await self.weed_out(weed_lands)
                log('农场', f'除草 {len(weed_lands)} 块地')
            
            if insect_lands:
                await self.insecticide(insect_lands)
                log('农场', f'除虫 {len(insect_lands)} 块地')
            
            if water_lands:
                await self.water_land(water_lands)
                log('农场', f'浇水 {len(water_lands)} 块地')
            
        except Exception as e:
            log_warn('农场', f'巡查错误: {e}')
        finally:
            self.is_checking = False
    
    async def farm_check_loop(self):
        """Farm check loop"""
        while self.running:
            await self.check_farm()
            await asyncio.sleep(Config.farm_check_interval)
    
    def start_farm_check_loop(self):
        """Start farm check loop"""
        if not self.running:
            self.running = True
            self.check_task = asyncio.create_task(self.farm_check_loop())
            log('农场', '巡查循环已启动')
    
    def stop_farm_check_loop(self):
        """Stop farm check loop"""
        self.running = False
        if self.check_task:
            self.check_task.cancel()
            log('农场', '巡查循环已停止')


# Global instance
farm_operations = FarmOperations()


def get_farm_operations() -> FarmOperations:
    """Get global farm operations instance"""
    return farm_operations
