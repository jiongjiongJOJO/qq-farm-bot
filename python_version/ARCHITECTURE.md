# Python版本架构文档

## 概述

本项目是QQ农场挂机脚本的Python实现版本，采用完整的面向对象设计，功能模块化封装，代码结构清晰，易于维护和扩展。

## 设计原则

### 1. 面向对象设计 (OOP)
- **封装**: 每个功能模块都封装在独立的类中
- **单一职责**: 每个类只负责一个具体的功能领域
- **高内聚**: 相关功能集中在同一个类中
- **低耦合**: 模块间通过清晰的接口通信

### 2. 模块化架构
```
┌─────────────┐
│  client.py  │  主程序入口
└──────┬──────┘
       │
       ├── Config         配置管理
       ├── NetworkClient  网络通信
       ├── FarmOps        农场操作
       ├── FriendOps      好友操作
       ├── TaskSystem     任务系统
       ├── Warehouse      仓库系统
       ├── StatusBar      状态显示
       └── GameConfig     游戏配置
```

### 3. 异步编程模型
- 使用 `asyncio` 实现异步IO
- 非阻塞的网络通信
- 多任务并发执行

## 核心模块详解

### Config类 (`src/config.py`)

**职责**: 管理全局配置

**主要功能**:
- 存储服务器连接信息
- 管理平台设置 (QQ/微信)
- 控制巡查间隔
- 定义游戏枚举 (PlantPhase)

**类方法**:
```python
Config.set_platform(platform: str)           # 设置平台
Config.set_farm_check_interval(seconds: float)  # 设置农场巡查间隔
Config.set_friend_check_interval(seconds: float) # 设置好友巡查间隔
```

**设计特点**:
- 使用类变量存储配置
- 类方法提供修改接口
- 确保配置的一致性

### NetworkClient类 (`src/network.py`)

**职责**: 管理网络通信

**主要功能**:
- WebSocket连接管理
- 用户登录和认证
- 消息编解码
- 心跳保活
- 用户状态同步

**核心方法**:
```python
async def connect(code: str, on_login: Callable)  # 连接服务器
async def send_msg_async(service, method, body)   # 发送消息
def get_user_state() -> UserState                 # 获取用户状态
async def cleanup()                                # 清理连接
```

**UserState子类**:
```python
class UserState:
    gid: int         # 用户ID
    name: str        # 昵称
    level: int       # 等级
    gold: int        # 金币
    exp: int         # 经验
    max_exp: int     # 当前等级最大经验
```

**设计特点**:
- 使用单例模式 (全局实例)
- 异步事件驱动
- 回调机制处理登录成功
- 内部维护用户状态

### FarmOperations类 (`src/farm.py`)

**职责**: 管理农场操作

**主要功能**:
- 获取土地信息
- 收获成熟作物
- 铲除枯死作物
- 种植种子
- 施肥加速
- 除草除虫浇水
- 自动巡查循环

**核心方法**:
```python
async def get_all_lands() -> Dict                  # 获取所有土地
async def harvest(land_ids: List[int])             # 收获
async def water_land(land_ids: List[int])          # 浇水
async def weed_out(land_ids: List[int])            # 除草
async def insecticide(land_ids: List[int])         # 除虫
async def fertilize(land_ids: List[int])           # 施肥
async def remove_plant(land_ids: List[int])        # 铲除
async def plant_seed(land_ids, seed_id)            # 种植
async def check_farm()                             # 检查农场
def start_farm_check_loop()                        # 启动巡查
def stop_farm_check_loop()                         # 停止巡查
```

**设计特点**:
- 操作原子化 (每个方法完成一个操作)
- 批量操作支持
- 自动循环检查
- 状态标志防止重复执行

### FriendOperations类 (`src/friend.py`)

**职责**: 管理好友农场操作

**主要功能**:
- 获取好友列表
- 进入好友农场
- 偷取成熟作物
- 帮助好友 (浇水/除草/除虫)
- 自动巡查好友

**核心方法**:
```python
async def get_friend_list() -> Dict                # 获取好友列表
async def enter_friend_farm(friend_gid)            # 进入好友农场
async def steal(friend_gid, land_ids)              # 偷菜
async def help_friend_water(friend_gid, land_ids)  # 帮助浇水
async def help_friend_weed(friend_gid, land_ids)   # 帮助除草
async def visit_friend_farm(friend_gid, name)      # 访问好友
async def check_friends()                          # 检查所有好友
def start_friend_check_loop()                      # 启动巡查
def stop_friend_check_loop()                       # 停止巡查
```

**设计特点**:
- 访问限流控制
- 操作限制管理
- 配置化的帮助策略
- 日志记录操作结果

### TaskSystem类 (`src/task.py`)

**职责**: 管理任务系统

**主要功能**:
- 获取任务列表
- 领取任务奖励
- 支持分享翻倍
- 自动检查任务

**核心方法**:
```python
async def get_task_list() -> Dict              # 获取任务列表
async def get_reward(task_id, share_times)     # 领取奖励
async def check_tasks()                        # 检查任务
def start_task_system()                        # 启动系统
def stop_task_system()                         # 停止系统
```

**设计特点**:
- 自动尝试最大倍数奖励
- 失败降级处理
- 定时检查机制

### WarehouseSystem类 (`src/warehouse.py`)

**职责**: 管理仓库和物品

**主要功能**:
- 获取背包内容
- 出售果实
- 自动售卖循环

**核心方法**:
```python
async def get_backpack() -> Dict               # 获取背包
async def sell_item(item_id, count)            # 出售物品
async def sell_fruits()                        # 出售所有果实
def start_sell_loop(interval: float)           # 启动售卖
def stop_sell_loop()                           # 停止售卖
```

**设计特点**:
- 批量出售优化
- 可配置的售卖间隔
- 错误处理和日志

### StatusBar类 (`src/status.py`)

**职责**: 管理状态显示

**主要功能**:
- 显示用户信息
- 更新状态栏
- 平台标识

**核心方法**:
```python
def init_status_bar()                          # 初始化
def cleanup_status_bar()                       # 清理
def set_platform(platform: str)                # 设置平台
def update_display()                           # 更新显示
def update_gold(gold: int)                     # 更新金币
def update_level(level, exp, max_exp)          # 更新等级
```

**设计特点**:
- 实时状态同步
- 终端UI优化
- 自动格式化

### GameConfig类 (`src/gameConfig.py`)

**职责**: 管理游戏配置数据

**主要功能**:
- 加载配置文件
- 提供植物数据
- 提供等级数据
- 辅助函数

**核心方法**:
```python
def load_config()                              # 加载配置
def get_plant_name(plant_id) -> str            # 获取植物名称
def get_plant_exp(plant_id) -> int             # 获取经验值
def get_plant_grow_time(plant_id) -> int       # 获取生长时间
def format_grow_time(seconds) -> str           # 格式化时间
def get_level_exp(level) -> int                # 获取等级经验
```

**设计特点**:
- 懒加载机制
- JSON数据解析
- 便捷访问函数

### ExpCalculator类 (`tools/calc_exp_yield.py`)

**职责**: 计算经验效率

**主要功能**:
- 计算作物经验效率
- 考虑肥料加成
- 推荐最优作物

**核心方法**:
```python
def calculate_exp_yield(exp, grow_time, lands, use_fertilizer) -> float
def get_planting_recommendation(level, lands) -> Dict
```

**算法说明**:
```
经验效率 = (收获经验 + 铲地经验) × 土地数 × 每小时循环次数
每小时循环次数 = 3600 / (生长时间 + 种植时间)
```

**设计特点**:
- 数学模型精确
- 考虑实际游戏机制
- 可配置的参数

### InviteProcessor类 (`src/invite.py`)

**职责**: 处理邀请码

**主要功能**:
- 读取邀请文件
- 解析邀请链接
- 发送好友申请

**核心方法**:
```python
async def process_invite_codes()               # 处理邀请码
def _parse_invite_url(url: str) -> dict        # 解析URL
```

**设计特点**:
- 仅微信环境启用
- 自动清空已处理
- 错误容忍

## 工作流程

### 1. 启动流程

```
main()
  ├── 解析命令行参数
  ├── 加载Proto定义
  ├── 加载游戏配置
  ├── 设置Config
  └── 创建FarmBot实例
      └── FarmBot.start()
          ├── 初始化状态栏
          ├── NetworkClient.connect()
          │   ├── 建立WebSocket连接
          │   ├── 发送登录请求
          │   └── 启动心跳循环
          └── on_login回调
              ├── 处理邀请码
              ├── 启动农场巡查
              ├── 启动好友巡查
              ├── 启动任务系统
              └── 启动仓库系统
```

### 2. 农场巡查循环

```
farm_check_loop()
  └── while running:
      ├── check_farm()
      │   ├── get_all_lands()
      │   ├── 分类土地状态
      │   ├── harvest(mature_lands)
      │   ├── remove_plant(dead_lands)
      │   ├── plant_seed(empty_lands)
      │   ├── fertilize(new_lands)
      │   ├── weed_out(weed_lands)
      │   ├── insecticide(insect_lands)
      │   └── water_land(water_lands)
      └── sleep(farm_check_interval)
```

### 3. 好友巡查循环

```
friend_check_loop()
  └── while running:
      ├── check_friends()
      │   ├── get_friend_list()
      │   └── for each friend:
      │       └── visit_friend_farm()
      │           ├── enter_friend_farm()
      │           ├── steal(mature_lands)
      │           ├── help_friend_weed()
      │           ├── help_friend_insecticide()
      │           └── help_friend_water()
      └── sleep(friend_check_interval)
```

## 数据流

```
用户输入 (code)
    ↓
NetworkClient (连接+登录)
    ↓
UserState (存储用户信息)
    ↓
各操作模块 (Farm/Friend/Task/Warehouse)
    ↓
网络请求 (通过NetworkClient)
    ↓
服务器响应
    ↓
更新本地状态
    ↓
StatusBar显示
```

## 扩展指南

### 添加新功能模块

1. **创建新模块文件** (`src/new_module.py`)
```python
from .network import get_network_client

class NewModule:
    def __init__(self):
        self.network = get_network_client()
        self.running = False
    
    async def do_something(self):
        # 实现功能
        pass
    
    def start(self):
        self.running = True
    
    def stop(self):
        self.running = False

# 全局实例
new_module = NewModule()

def get_new_module() -> NewModule:
    return new_module
```

2. **在client.py中集成**
```python
from src.new_module import get_new_module

class FarmBot:
    def __init__(self):
        self.new_module = get_new_module()
    
    async def on_login(self):
        self.new_module.start()
    
    async def stop(self):
        self.new_module.stop()
```

### 添加新的API调用

在对应的模块类中添加方法:
```python
async def new_api_call(self, param: int) -> Dict[str, Any]:
    """新的API调用"""
    body = b''  # 编码请求体
    reply = await self.network.send_msg_async(
        'service.name',
        'MethodName',
        body
    )
    return reply
```

### 修改配置项

在 `src/config.py` 中:
```python
class Config:
    new_config_item = 'default_value'
    
    @classmethod
    def set_new_config(cls, value):
        cls.new_config_item = value
```

## 最佳实践

### 1. 异步编程
- 所有IO操作使用 `async/await`
- 使用 `asyncio.create_task()` 创建后台任务
- 使用 `asyncio.sleep()` 而不是 `time.sleep()`

### 2. 错误处理
```python
try:
    await some_operation()
except Exception as e:
    log_warn('模块', f'操作失败: {e}')
```

### 3. 资源清理
```python
async def cleanup(self):
    self.running = False
    if self.task:
        self.task.cancel()
        try:
            await self.task
        except asyncio.CancelledError:
            pass
```

### 4. 日志记录
```python
from .utils import log, log_warn

log('标签', '正常消息')
log_warn('标签', '警告消息')
```

## 性能优化

### 1. 批量操作
- 尽可能批量发送请求
- 减少网络往返次数

### 2. 异步并发
- 使用 `asyncio.gather()` 并发执行
- 独立操作可以并行

### 3. 智能间隔
- 根据服务器响应调整间隔
- 避免过于频繁的请求

## 安全考虑

### 1. 不存储敏感信息
- 不在代码中硬编码密码
- 不提交敏感配置到版本控制

### 2. 输入验证
- 验证用户输入
- 检查API响应

### 3. 异常处理
- 捕获所有可能的异常
- 优雅降级

## 总结

Python版本通过面向对象设计和模块化架构，提供了:
- ✅ 清晰的代码结构
- ✅ 易于理解和维护
- ✅ 方便测试和调试
- ✅ 灵活的扩展能力
- ✅ 良好的错误处理

这是一个完整、可扩展的农场挂机脚本架构实现。
