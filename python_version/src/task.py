"""Task system - automatic task reward collection"""

import asyncio
from typing import Dict, Any, Optional, List

from .proto import types
from .network import get_network_client
from .utils import log, log_warn


class TaskSystem:
    """Task system manager"""
    
    def __init__(self):
        self.network = get_network_client()
        self.check_task: Optional[asyncio.Task] = None
        self.running = False
    
    async def get_task_list(self) -> Dict[str, Any]:
        """Get task list"""
        body = b''  # Placeholder
        reply = await self.network.send_msg_async(
            'gamepb.taskpb.TaskService',
            'GetTaskList',
            body
        )
        return reply
    
    async def get_reward(self, task_id: int, share_times: int = 1) -> Dict[str, Any]:
        """Get task reward
        
        Args:
            task_id: Task ID
            share_times: Share multiplier (1, 2, or 3)
        """
        body = b''  # Placeholder
        reply = await self.network.send_msg_async(
            'gamepb.taskpb.TaskService',
            'GetReward',
            body
        )
        return reply
    
    async def check_tasks(self):
        """Check and collect task rewards"""
        try:
            # Get task list
            tasks_reply = await self.get_task_list()
            
            # Mock implementation
            # In production: filter completed tasks and collect rewards
            completed_tasks = []  # List of completed task IDs
            
            for task_id in completed_tasks:
                try:
                    # Try to get 3x reward (share bonus)
                    reward_reply = await self.get_reward(task_id, 3)
                    log('任务', f'领取: 任务{task_id} → 3倍奖励')
                except Exception:
                    # Fallback to normal reward
                    try:
                        reward_reply = await self.get_reward(task_id, 1)
                        log('任务', f'领取: 任务{task_id} → 普通奖励')
                    except Exception as e:
                        log_warn('任务', f'领取失败: 任务{task_id}: {e}')
        
        except Exception as e:
            log_warn('任务', f'检查错误: {e}')
    
    async def task_check_loop(self):
        """Task check loop"""
        while self.running:
            await self.check_tasks()
            await asyncio.sleep(60.0)  # Check every minute
    
    def start_task_system(self):
        """Start task system"""
        if not self.running:
            self.running = True
            self.check_task = asyncio.create_task(self.task_check_loop())
            log('任务', '系统已启动')
    
    def stop_task_system(self):
        """Stop task system"""
        self.running = False
        if self.check_task:
            self.check_task.cancel()
            log('任务', '系统已停止')


# Global instance
task_system = TaskSystem()


def get_task_system() -> TaskSystem:
    """Get global task system instance"""
    return task_system
