"""Invitation code processing"""

import os
import asyncio
from typing import List

from .config import Config
from .network import get_network_client
from .utils import log, log_warn


class InviteProcessor:
    """Invitation code processor"""
    
    def __init__(self):
        self.network = get_network_client()
    
    async def process_invite_codes(self):
        """Process invitation codes from share.txt (WeChat only)"""
        if Config.platform != 'wx':
            return
        
        share_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'share.txt')
        
        if not os.path.exists(share_file):
            return
        
        try:
            with open(share_file, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
            
            if not lines:
                return
            
            log('邀请', f'发现 {len(lines)} 个邀请码')
            
            # Process each invitation
            processed = 0
            for line in lines:
                try:
                    # Parse invitation parameters
                    # Format: ?uid=xxx&openid=xxx&share_source=xxx&doc_id=xxx
                    params = self._parse_invite_url(line)
                    
                    if params:
                        # In production: send SyncAll or friend request
                        # await self._send_friend_request(params)
                        processed += 1
                        await asyncio.sleep(0.5)  # Small delay
                
                except Exception as e:
                    log_warn('邀请', f'处理失败: {e}')
            
            if processed > 0:
                log('邀请', f'已处理 {processed} 个邀请码')
                
                # Clear the file
                with open(share_file, 'w', encoding='utf-8') as f:
                    f.write('')
        
        except Exception as e:
            log_warn('邀请', f'读取文件失败: {e}')
    
    def _parse_invite_url(self, url: str) -> dict:
        """Parse invitation URL parameters"""
        params = {}
        
        # Extract query parameters
        if '?' in url:
            query = url.split('?')[1]
            for param in query.split('&'):
                if '=' in param:
                    key, value = param.split('=', 1)
                    params[key] = value
        
        return params if params else None


# Global instance
invite_processor = InviteProcessor()


def get_invite_processor() -> InviteProcessor:
    """Get global invite processor instance"""
    return invite_processor
