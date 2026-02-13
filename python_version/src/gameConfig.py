"""Game configuration - level experience table and plant data"""

import os
import json
from typing import Dict, Any, Optional


class GameConfig:
    """Game configuration manager"""
    
    def __init__(self):
        self.role_levels: Dict[int, Any] = {}
        self.plants: Dict[int, Any] = {}
        self._loaded = False
    
    def load_config(self):
        """Load game configuration files"""
        if self._loaded:
            return
        
        config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'gameConfig')
        
        # Load role levels
        role_level_file = os.path.join(config_dir, 'RoleLevel.json')
        if os.path.exists(role_level_file):
            with open(role_level_file, 'r', encoding='utf-8') as f:
                role_level_data = json.load(f)
                for item in role_level_data:
                    level = item.get('Level', 0)
                    if level:
                        self.role_levels[level] = item
        
        # Load plant data
        plant_file = os.path.join(config_dir, 'Plant.json')
        if os.path.exists(plant_file):
            with open(plant_file, 'r', encoding='utf-8') as f:
                plant_data = json.load(f)
                for item in plant_data:
                    plant_id = item.get('ID', 0)
                    if plant_id:
                        self.plants[plant_id] = item
        
        self._loaded = True
    
    def get_plant_name_by_seed_id(self, seed_id: int) -> str:
        """Get plant name by seed ID"""
        plant = self.plants.get(seed_id)
        if plant:
            return plant.get('Name', f'种子{seed_id}')
        return f'种子{seed_id}'
    
    def get_plant_name(self, plant_id: int) -> str:
        """Get plant name by plant ID"""
        return self.get_plant_name_by_seed_id(plant_id)
    
    def get_plant_exp(self, plant_id: int) -> int:
        """Get plant experience value"""
        plant = self.plants.get(plant_id)
        if plant:
            return plant.get('Exp', 0)
        return 0
    
    def get_plant_grow_time(self, plant_id: int) -> int:
        """Get plant growth time in seconds"""
        plant = self.plants.get(plant_id)
        if plant:
            return plant.get('GrowTime', 0)
        return 0
    
    def format_grow_time(self, seconds: int) -> str:
        """Format growth time to human readable string"""
        if seconds < 60:
            return f'{seconds}秒'
        elif seconds < 3600:
            minutes = seconds // 60
            return f'{minutes}分钟'
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            if minutes > 0:
                return f'{hours}小时{minutes}分钟'
            return f'{hours}小时'
    
    def get_level_exp(self, level: int) -> int:
        """Get required experience for level"""
        role = self.role_levels.get(level)
        if role:
            return role.get('Exp', 0)
        return 0


# Global instance
game_config = GameConfig()


def get_game_config() -> GameConfig:
    """Get global game config instance"""
    return game_config


# Convenience functions
def get_plant_name_by_seed_id(seed_id: int) -> str:
    return game_config.get_plant_name_by_seed_id(seed_id)


def get_plant_name(plant_id: int) -> str:
    return game_config.get_plant_name(plant_id)


def get_plant_exp(plant_id: int) -> int:
    return game_config.get_plant_exp(plant_id)


def get_plant_grow_time(plant_id: int) -> int:
    return game_config.get_plant_grow_time(plant_id)


def format_grow_time(seconds: int) -> str:
    return game_config.format_grow_time(seconds)
