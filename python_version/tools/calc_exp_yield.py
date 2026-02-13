"""Experience yield calculation tool"""

import os
import json
from typing import Dict, List, Optional, Tuple


class ExpCalculator:
    """Experience yield calculator"""
    
    # Planting speed (lands per second)
    SPEED_NO_FERTILIZER = 9.0  # 18 lands in 2 seconds
    SPEED_WITH_FERTILIZER = 6.0  # 12 lands in 2 seconds
    
    # Normal fertilizer reduces grow time by 20%, minimum 30 seconds
    FERTILIZER_REDUCTION = 0.2
    FERTILIZER_MIN_REDUCTION = 30
    
    def __init__(self):
        self.seed_data: List[Dict] = []
        self._loaded = False
    
    def load_seed_data(self):
        """Load seed shop data"""
        if self._loaded:
            return
        
        data_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'tools',
            'seed-shop-merged-export.json'
        )
        
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                self.seed_data = json.load(f)
        
        self._loaded = True
    
    def calculate_grow_time_with_fertilizer(self, grow_time: int) -> int:
        """Calculate growth time with normal fertilizer"""
        reduction = max(int(grow_time * self.FERTILIZER_REDUCTION), self.FERTILIZER_MIN_REDUCTION)
        return grow_time - reduction
    
    def calculate_exp_yield(
        self,
        exp: int,
        grow_time: int,
        lands: int,
        use_fertilizer: bool = True
    ) -> float:
        """Calculate experience yield per hour
        
        Args:
            exp: Experience gained per harvest
            grow_time: Growth time in seconds
            lands: Number of lands
            use_fertilizer: Whether to use fertilizer
        
        Returns:
            Experience yield per hour
        """
        # Total experience per round (harvest + remove)
        total_exp = exp + 1
        
        # Effective growth time
        if use_fertilizer:
            effective_grow_time = self.calculate_grow_time_with_fertilizer(grow_time)
            planting_speed = self.SPEED_WITH_FERTILIZER
        else:
            effective_grow_time = grow_time
            planting_speed = self.SPEED_NO_FERTILIZER
        
        # Planting time
        planting_time = lands / planting_speed
        
        # Total cycle time
        cycle_time = effective_grow_time + planting_time
        
        # Cycles per hour
        cycles_per_hour = 3600.0 / cycle_time
        
        # Total experience per hour
        exp_per_hour = total_exp * lands * cycles_per_hour
        
        return exp_per_hour
    
    def get_planting_recommendation(
        self,
        level: int,
        lands: int
    ) -> Optional[Dict]:
        """Get planting recommendation based on experience yield
        
        Args:
            level: Player level
            lands: Number of unlocked lands
        
        Returns:
            Recommended seed information or None
        """
        self.load_seed_data()
        
        if not self.seed_data:
            return None
        
        # Filter seeds available for the level
        available_seeds = [
            seed for seed in self.seed_data
            if seed.get('RequiredLevel', 999) <= level
        ]
        
        if not available_seeds:
            return None
        
        # Calculate exp yield for each seed
        seed_yields = []
        for seed in available_seeds:
            exp = seed.get('Exp', 0)
            grow_time = seed.get('GrowTime', 0)
            
            if grow_time > 0:
                yield_value = self.calculate_exp_yield(exp, grow_time, lands, True)
                seed_yields.append({
                    'seed': seed,
                    'yield': yield_value
                })
        
        if not seed_yields:
            return None
        
        # Sort by yield (descending)
        seed_yields.sort(key=lambda x: x['yield'], reverse=True)
        
        # Return best seed
        return seed_yields[0]['seed']


# Global instance
exp_calculator = ExpCalculator()


def get_planting_recommendation(level: int, lands: int) -> Optional[Dict]:
    """Get planting recommendation
    
    Args:
        level: Player level
        lands: Number of unlocked lands
    
    Returns:
        Recommended seed information
    """
    return exp_calculator.get_planting_recommendation(level, lands)
