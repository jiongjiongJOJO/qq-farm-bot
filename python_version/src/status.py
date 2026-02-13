"""Status bar display"""

import sys
from typing import Optional

from .network import get_network_client
from .config import Config


class StatusBar:
    """Status bar manager for displaying user info"""
    
    def __init__(self):
        self.enabled = False
        self.platform = 'QQ'
    
    def init_status_bar(self):
        """Initialize status bar"""
        self.enabled = True
    
    def cleanup_status_bar(self):
        """Cleanup status bar"""
        self.enabled = False
    
    def set_platform(self, platform: str):
        """Set platform display"""
        self.platform = platform.upper()
    
    def update_display(self):
        """Update status bar display"""
        if not self.enabled:
            return
        
        network = get_network_client()
        state = network.get_user_state()
        
        # Build status line
        status = f"{self.platform} | {state.name} | Lv{state.level} {state.exp}/{state.max_exp} | 金币:{state.gold}"
        separator = "─" * len(status)
        
        # Move cursor to top and display
        sys.stdout.write(f'\033[H\033[J')  # Clear screen
        sys.stdout.write(f'{status}\n')
        sys.stdout.write(f'{separator}\n\n')
        sys.stdout.flush()
    
    def update_from_login(self, login_data: dict):
        """Update status from login data"""
        self.update_display()
    
    def update_gold(self, gold: int):
        """Update gold display"""
        network = get_network_client()
        network.get_user_state().update_gold(gold)
        self.update_display()
    
    def update_level(self, level: int, exp: int, max_exp: int):
        """Update level and experience display"""
        network = get_network_client()
        network.get_user_state().update_level(level, exp, max_exp)
        self.update_display()


# Global instance
status_bar = StatusBar()


def get_status_bar() -> StatusBar:
    """Get global status bar instance"""
    return status_bar
