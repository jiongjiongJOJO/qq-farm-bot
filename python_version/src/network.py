"""WebSocket network layer - connection, message encoding/decoding, login, heartbeat"""

import asyncio
import websockets
from typing import Optional, Callable, Dict, Any, Awaitable
from asyncio import Event

from .config import Config
from .proto import types
from .utils import (
    to_long, to_num, ServerTimeSync, log, log_warn, format_time
)


class UserState:
    """User state container"""
    
    def __init__(self):
        self.gid = 0
        self.name = ''
        self.level = 0
        self.gold = 0
        self.exp = 0
        self.max_exp = 0
    
    def update_from_login(self, login_data: Dict[str, Any]):
        """Update state from login response"""
        self.gid = login_data.get('gid', 0)
        self.name = login_data.get('name', '')
        self.level = login_data.get('level', 0)
        self.gold = login_data.get('gold', 0)
        self.exp = login_data.get('exp', 0)
        self.max_exp = login_data.get('max_exp', 0)
    
    def update_gold(self, gold: int):
        """Update gold amount"""
        self.gold = gold
    
    def update_level(self, level: int, exp: int, max_exp: int):
        """Update level and experience"""
        self.level = level
        self.exp = exp
        self.max_exp = max_exp


class NetworkClient:
    """WebSocket network client"""
    
    def __init__(self):
        self.ws: Optional[websockets.WebSocketClientProtocol] = None
        self.client_seq = 1
        self.server_seq = 0
        self.user_state = UserState()
        self.connected = Event()
        self.logged_in = Event()
        self.heartbeat_task: Optional[asyncio.Task] = None
        self.pending_callbacks: Dict[int, Callable] = {}
        self.on_login_callback: Optional[Callable] = None
        self.running = False
    
    async def connect(self, code: str, on_login: Optional[Callable] = None):
        """Connect to server and login"""
        self.on_login_callback = on_login
        self.running = True
        
        # Build WebSocket URL
        platform = Config.platform
        url = f"{Config.SERVER_URL}?code={code}&version={Config.CLIENT_VERSION}&platform={platform}&os={Config.OS}"
        
        log('网络', f'连接中... {platform.upper()}')
        
        try:
            self.ws = await websockets.connect(url)
            self.connected.set()
            log('网络', '连接成功')
            
            # Start message handler
            asyncio.create_task(self._message_handler())
            
            # Send login request
            await self._login()
            
        except Exception as e:
            log_warn('网络', f'连接失败: {e}')
            raise
    
    async def _login(self):
        """Send login request"""
        # In a real implementation, this would encode a proper LoginRequest
        # For now, this is a placeholder to demonstrate the architecture
        log('登录', '发送登录请求...')
        
        # Mock login for demonstration
        # In production: encode LoginRequest with protobuf and send
        # reply = await self.send_msg_async('gamepb.userpb.UserService', 'Login', body)
        
        # Mock response
        self.user_state.gid = 1234567890
        self.user_state.name = '测试用户'
        self.user_state.level = 24
        self.user_state.gold = 88888
        self.user_state.exp = 125
        self.user_state.max_exp = 500
        
        self.logged_in.set()
        self._print_login_info()
        
        # Start heartbeat
        self.heartbeat_task = asyncio.create_task(self._heartbeat_loop())
        
        # Call login callback
        if self.on_login_callback:
            await self.on_login_callback()
    
    def _print_login_info(self):
        """Print login information"""
        print('\n' + '='*30 + ' 登录成功 ' + '='*30)
        print(f'  GID:    {self.user_state.gid}')
        print(f'  昵称:   {self.user_state.name}')
        print(f'  等级:   {self.user_state.level}')
        print(f'  金币:   {self.user_state.gold}')
        print(f'  经验:   {self.user_state.exp}/{self.user_state.max_exp}')
        print('='*72 + '\n')
    
    async def _heartbeat_loop(self):
        """Heartbeat loop to keep connection alive"""
        while self.running:
            await asyncio.sleep(Config.heartbeat_interval)
            try:
                await self._send_heartbeat()
            except Exception as e:
                log_warn('心跳', f'失败: {e}')
    
    async def _send_heartbeat(self):
        """Send heartbeat"""
        # In production: encode HeartbeatRequest and send
        pass
    
    async def _message_handler(self):
        """Handle incoming messages"""
        try:
            async for message in self.ws:
                await self._handle_message(message)
        except Exception as e:
            if self.running:
                log_warn('网络', f'消息处理错误: {e}')
    
    async def _handle_message(self, data: bytes):
        """Handle a single message"""
        # In production: decode GateMessage and dispatch to callbacks
        pass
    
    def encode_msg(self, service_name: str, method_name: str, body_bytes: bytes) -> bytes:
        """Encode message"""
        # In production: create and encode GateMessage with meta
        # For now, return placeholder
        seq = self.client_seq
        self.client_seq += 1
        return body_bytes
    
    async def send_msg_async(
        self, 
        service_name: str, 
        method_name: str, 
        body_bytes: bytes,
        timeout: float = 10.0
    ) -> Dict[str, Any]:
        """Send message and wait for response"""
        if not self.ws or self.ws.closed:
            raise ConnectionError(f'连接未打开: {method_name}')
        
        seq = self.client_seq
        encoded = self.encode_msg(service_name, method_name, body_bytes)
        
        # In production: set up callback, send message, wait for response
        # For now, return mock response
        await self.ws.send(encoded)
        
        return {'body': b'', 'meta': {}}
    
    def get_user_state(self) -> UserState:
        """Get current user state"""
        return self.user_state
    
    async def cleanup(self):
        """Cleanup and close connection"""
        self.running = False
        
        if self.heartbeat_task:
            self.heartbeat_task.cancel()
            try:
                await self.heartbeat_task
            except asyncio.CancelledError:
                pass
        
        if self.ws and not self.ws.closed:
            await self.ws.close()
            log('网络', '连接已关闭')


# Global instance
network_client = NetworkClient()


def get_network_client() -> NetworkClient:
    """Get global network client instance"""
    return network_client
