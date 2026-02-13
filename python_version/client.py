#!/usr/bin/env python3
"""QQ Farm Bot - Python Version - Main Entry Point"""

import asyncio
import argparse
import sys
import signal

from src.config import Config
from src.proto import load_proto
from src.network import get_network_client
from src.farm import get_farm_operations
from src.friend import get_friend_operations
from src.task import get_task_system
from src.warehouse import get_warehouse_system
from src.status import get_status_bar
from src.invite import get_invite_processor
from src.gameConfig import game_config
from src.utils import emit_runtime_hint, log


def show_help():
    """Show help information"""
    help_text = """
QQ经典农场 挂机脚本 (Python版)
====================

用法:
  python client.py --code <登录code> [--wx] [--interval <秒>] [--friend-interval <秒>]

参数:
  --code              小程序 login() 返回的临时凭证 (必需)
  --wx                使用微信登录 (默认为QQ小程序)
  --interval          自己农场巡查间隔秒数, 默认1秒, 最低1秒
  --friend-interval   好友巡查间隔秒数, 默认10秒, 最低1秒

功能:
  - 自动收获成熟作物 → 购买种子 → 种植 → 施肥
  - 自动除草、除虫、浇水
  - 自动铲除枯死作物
  - 自动巡查好友农场: 帮忙浇水/除草/除虫 + 偷菜
  - 自动领取任务奖励 (支持分享翻倍)
  - 每分钟自动出售仓库果实
  - 启动时读取 share.txt 处理邀请码 (仅微信)
  - 心跳保活

示例:
  # QQ小程序
  python client.py --code YOUR_CODE_HERE
  
  # 微信小程序
  python client.py --code YOUR_CODE_HERE --wx
  
  # 自定义巡查间隔
  python client.py --code YOUR_CODE_HERE --interval 5 --friend-interval 2

邀请码文件 (share.txt):
  每行一个邀请链接，格式: ?uid=xxx&openid=xxx&share_source=xxx&doc_id=xxx
  启动时会尝试通过 SyncAll API 同步这些好友
"""
    print(help_text)


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='QQ Farm Bot - Python Version',
        add_help=False
    )
    
    parser.add_argument('--code', type=str, help='Login code from mini-program')
    parser.add_argument('--wx', action='store_true', help='Use WeChat platform')
    parser.add_argument('--interval', type=float, default=1.0, help='Farm check interval (seconds)')
    parser.add_argument('--friend-interval', type=float, default=10.0, help='Friend check interval (seconds)')
    parser.add_argument('--help', action='store_true', help='Show help message')
    
    return parser.parse_args()


class FarmBot:
    """Main farm bot controller"""
    
    def __init__(self):
        self.network = get_network_client()
        self.farm = get_farm_operations()
        self.friend = get_friend_operations()
        self.task = get_task_system()
        self.warehouse = get_warehouse_system()
        self.status = get_status_bar()
        self.invite = get_invite_processor()
        self.running = False
    
    async def start(self, code: str):
        """Start the bot"""
        self.running = True
        
        # Initialize status bar
        self.status.init_status_bar()
        self.status.set_platform(Config.platform)
        emit_runtime_hint(True)
        
        platform_name = '微信' if Config.platform == 'wx' else 'QQ'
        log(
            '启动',
            f'{platform_name} code={code[:8]}... '
            f'农场{Config.farm_check_interval}s 好友{Config.friend_check_interval}s'
        )
        
        # Connect and login
        await self.network.connect(code, self.on_login)
        
        # Wait for login
        await self.network.logged_in.wait()
    
    async def on_login(self):
        """Callback after successful login"""
        # Process invitation codes (WeChat only)
        await self.invite.process_invite_codes()
        
        # Start farm operations
        self.farm.start_farm_check_loop()
        
        # Start friend operations
        self.friend.start_friend_check_loop()
        
        # Start task system
        self.task.start_task_system()
        
        # Start warehouse system (sell every 60 seconds)
        self.warehouse.start_sell_loop(60.0)
        
        # Immediate warehouse check after 5 seconds
        asyncio.create_task(self._delayed_warehouse_check())
    
    async def _delayed_warehouse_check(self):
        """Delayed warehouse check"""
        await asyncio.sleep(5.0)
        await self.warehouse.sell_fruits()
    
    async def stop(self):
        """Stop the bot"""
        self.running = False
        
        log('退出', '正在停止...')
        
        # Stop all systems
        self.farm.stop_farm_check_loop()
        self.friend.stop_friend_check_loop()
        self.task.stop_task_system()
        self.warehouse.stop_sell_loop()
        
        # Cleanup
        self.status.cleanup_status_bar()
        await self.network.cleanup()
        
        log('退出', '已停止')
    
    async def run_forever(self):
        """Run bot forever"""
        while self.running:
            await asyncio.sleep(1.0)


async def main():
    """Main function"""
    args = parse_args()
    
    # Show help
    if args.help or not args.code:
        show_help()
        sys.exit(0 if args.help else 1)
    
    # Load protobuf definitions
    load_proto()
    
    # Load game configuration
    game_config.load_config()
    
    # Set configuration
    if args.wx:
        Config.set_platform('wx')
    
    Config.set_farm_check_interval(args.interval)
    Config.set_friend_check_interval(args.friend_interval)
    
    # Create and start bot
    bot = FarmBot()
    
    # Setup signal handlers
    def signal_handler(sig, frame):
        print('\n')
        asyncio.create_task(bot.stop())
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Start bot
        await bot.start(args.code)
        
        # Run forever
        await bot.run_forever()
    
    except KeyboardInterrupt:
        print('\n')
    except Exception as e:
        log('错误', f'启动失败: {e}')
        import traceback
        traceback.print_exc()
    finally:
        await bot.stop()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\n程序已退出')
