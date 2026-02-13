"""Simple tests for Python version"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.config import Config, PlantPhase, PHASE_NAMES
from src.utils import to_long, format_time, ServerTimeSync
from src.gameConfig import game_config


def test_config():
    """Test configuration module"""
    print("Testing Config...")
    assert Config.platform == 'qq'
    
    Config.set_platform('wx')
    assert Config.platform == 'wx'
    
    Config.set_farm_check_interval(5.0)
    assert Config.farm_check_interval == 5.0
    
    # Test minimum interval
    Config.set_farm_check_interval(0.5)
    assert Config.farm_check_interval == 1.0  # Should be clamped to 1.0
    
    print("✓ Config tests passed")


def test_plant_phase():
    """Test plant phase enum"""
    print("Testing PlantPhase...")
    assert PlantPhase.SEED == 1
    assert PlantPhase.MATURE == 6
    assert PlantPhase.DEAD == 7
    assert len(PHASE_NAMES) == 8
    print("✓ PlantPhase tests passed")


def test_utils():
    """Test utility functions"""
    print("Testing utils...")
    
    # Test to_long
    assert to_long(123) == 123
    assert to_long("456") == 456
    
    # Test format_time
    formatted = format_time(1707804000)
    assert "/" in formatted
    
    # Test ServerTimeSync
    ServerTimeSync.sync_time(1707804000)
    server_time = ServerTimeSync.get_server_time_sec()
    assert isinstance(server_time, int)
    
    print("✓ Utils tests passed")


def test_game_config():
    """Test game configuration"""
    print("Testing GameConfig...")
    
    game_config.load_config()
    
    # Test plant name retrieval
    name = game_config.get_plant_name(1001)
    assert isinstance(name, str)
    
    # Test grow time formatting
    formatted = game_config.format_grow_time(3665)
    assert "小时" in formatted or "分钟" in formatted
    
    print("✓ GameConfig tests passed")


def test_imports():
    """Test that all modules can be imported"""
    print("Testing module imports...")
    
    from src.network import NetworkClient
    from src.farm import FarmOperations
    from src.friend import FriendOperations
    from src.task import TaskSystem
    from src.warehouse import WarehouseSystem
    from src.status import StatusBar
    from src.invite import InviteProcessor
    from tools.calc_exp_yield import ExpCalculator
    
    # Test instantiation
    network = NetworkClient()
    farm = FarmOperations()
    friend = FriendOperations()
    task = TaskSystem()
    warehouse = WarehouseSystem()
    status = StatusBar()
    invite = InviteProcessor()
    calc = ExpCalculator()
    
    assert network is not None
    assert farm is not None
    assert friend is not None
    assert task is not None
    assert warehouse is not None
    assert status is not None
    assert invite is not None
    assert calc is not None
    
    print("✓ Import tests passed")


def run_all_tests():
    """Run all tests"""
    print("="*50)
    print("Running Python Version Tests")
    print("="*50)
    print()
    
    try:
        test_config()
        test_plant_phase()
        test_utils()
        test_game_config()
        test_imports()
        
        print()
        print("="*50)
        print("✓ All tests passed!")
        print("="*50)
        return True
    
    except Exception as e:
        print()
        print("="*50)
        print(f"✗ Test failed: {e}")
        print("="*50)
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
