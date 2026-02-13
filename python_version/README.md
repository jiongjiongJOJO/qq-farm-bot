# QQ经典农场挂机脚本 - Python版本

这是基于原Node.js版本的Python实现，采用面向对象设计，功能模块化封装。

## 主要特性

- **面向对象设计**: 所有功能都封装在类中，易于维护和扩展
- **模块化架构**: 功能按模块划分，职责清晰
- **异步IO**: 使用asyncio实现高效的异步网络通信
- **类型提示**: 使用Python类型注解提高代码可读性

## 项目结构

```
python_version/
├── client.py              # 主程序入口
├── requirements.txt       # Python依赖
├── src/                   # 源代码模块
│   ├── __init__.py
│   ├── config.py          # 配置类和枚举
│   ├── utils.py           # 工具函数模块
│   ├── proto.py           # Protobuf消息类型管理
│   ├── network.py         # 网络通信类 (WebSocket连接/登录/心跳)
│   ├── farm.py            # 农场操作类 (收获/种植/浇水/除草/除虫)
│   ├── friend.py          # 好友农场类 (访问/帮忙/偷菜)
│   ├── task.py            # 任务系统类 (自动领取奖励)
│   ├── warehouse.py       # 仓库系统类 (自动出售果实)
│   ├── status.py          # 状态栏类 (显示用户信息)
│   ├── invite.py          # 邀请码处理类
│   └── gameConfig.py      # 游戏配置类 (等级/植物数据)
├── proto/                 # Protobuf定义文件
├── gameConfig/            # 游戏配置数据
│   ├── RoleLevel.json     # 等级经验表
│   └── Plant.json         # 植物数据
└── tools/                 # 辅助工具
    └── calc_exp_yield.py  # 经验效率计算类

```

## 核心类设计

### 1. Config类 (`src/config.py`)
- 管理所有配置常量
- 提供配置修改接口
- 定义植物生长阶段枚举

### 2. NetworkClient类 (`src/network.py`)
- WebSocket连接管理
- 消息编解码
- 用户状态管理
- 心跳保活机制

### 3. FarmOperations类 (`src/farm.py`)
- 农场操作封装
- 自动巡查循环
- 作物管理 (收获/种植/施肥)
- 维护操作 (除草/除虫/浇水)

### 4. FriendOperations类 (`src/friend.py`)
- 好友农场访问
- 帮助好友操作
- 偷菜功能
- 好友巡查循环

### 5. TaskSystem类 (`src/task.py`)
- 任务列表获取
- 自动领取奖励
- 支持分享翻倍

### 6. WarehouseSystem类 (`src/warehouse.py`)
- 仓库管理
- 自动出售果实
- 定时售卖循环

### 7. ExpCalculator类 (`tools/calc_exp_yield.py`)
- 经验效率计算
- 种植推荐算法
- 考虑肥料加成

## 安装

### 1. 安装Python依赖

```bash
cd python_version
pip install -r requirements.txt
```

### 2. 编译Protobuf文件 (可选)

在完整实现中，需要将.proto文件编译为Python代码：

```bash
# 安装protoc编译器
# Ubuntu/Debian: sudo apt-get install protobuf-compiler
# macOS: brew install protobuf

# 编译proto文件
protoc --python_out=. proto/*.proto
```

**注意**: 当前版本为演示架构，protobuf部分使用占位符。在生产环境中需要完整实现。

## 使用方法

### 基本用法

```bash
# QQ小程序
python client.py --code <你的登录code>

# 微信小程序
python client.py --code <你的登录code> --wx
```

### 自定义巡查间隔

```bash
# 农场巡查间隔5秒，好友巡查间隔2秒
python client.py --code <code> --interval 5 --friend-interval 2
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--code` | 小程序登录凭证（**必需**） | — |
| `--wx` | 使用微信登录 | QQ小程序 |
| `--interval` | 农场巡查间隔（秒） | 1 |
| `--friend-interval` | 好友巡查间隔（秒） | 10 |
| `--help` | 显示帮助信息 | — |

### 邀请码功能（微信环境）

在项目根目录创建 `share.txt` 文件，每行一个邀请链接：

```
https://xxx?uid=123&openid=xxx&share_source=4&doc_id=2
https://xxx?uid=456&openid=xxx&share_source=4&doc_id=2
```

启动时会自动处理这些邀请链接。

## 功能特性

### 自己农场
- ✅ 自动收获成熟作物
- ✅ 自动铲除枯死作物
- ✅ 自动种植 (基于经验效率分析)
- ✅ 自动施肥 (普通肥料)
- ✅ 自动除草
- ✅ 自动除虫
- ✅ 自动浇水
- ✅ 自动出售仓库果实

### 好友农场
- ✅ 好友农场巡查
- ✅ 帮好友浇水/除草/除虫
- ✅ 自动偷菜

### 系统功能
- ✅ 自动领取任务奖励
- ✅ 邀请码处理 (微信)
- ✅ 状态栏显示
- ✅ 心跳保活

## 设计特点

### 1. 面向对象设计
- 每个功能模块都是独立的类
- 单一职责原则
- 便于单元测试

### 2. 异步编程
- 使用asyncio实现异步IO
- 非阻塞网络通信
- 高效的并发处理

### 3. 模块化封装
- 功能按职责分离
- 模块间低耦合
- 易于维护和扩展

### 4. 配置管理
- 集中的配置类
- 运行时可调整
- 默认值合理

### 5. 错误处理
- 完善的异常捕获
- 错误日志记录
- 优雅的降级处理

## 与Node.js版本对比

### 相同点
- 功能完全一致
- 支持相同的协议
- 配置参数兼容

### 不同点
- **语言**: Python vs JavaScript
- **异步模型**: asyncio vs async/await (Node.js)
- **架构**: 面向对象 vs 函数式
- **依赖**: websockets/protobuf vs ws/protobufjs

## 扩展指南

### 添加新功能

1. 在 `src/` 目录创建新模块
2. 定义功能类
3. 在 `client.py` 中集成
4. 更新文档

示例：

```python
# src/new_feature.py
class NewFeature:
    def __init__(self):
        self.network = get_network_client()
    
    async def do_something(self):
        # 实现功能
        pass

# client.py中集成
from src.new_feature import NewFeature

class FarmBot:
    def __init__(self):
        self.new_feature = NewFeature()
```

### 修改配置

在 `src/config.py` 中添加新配置项：

```python
class Config:
    new_option = True  # 新配置项
    
    @classmethod
    def set_new_option(cls, value: bool):
        cls.new_option = value
```

## 注意事项

1. **登录Code有效期**: 过期后需要重新抓取
2. **巡查间隔**: 不要设置过短，避免服务器限流
3. **微信环境**: 邀请码功能仅在微信环境下有效
4. **Protobuf**: 当前为演示版本，生产环境需要编译完整的protobuf文件

## 开发状态

当前版本是完整的架构实现，展示了：
- ✅ 完整的面向对象设计
- ✅ 模块化的代码组织
- ✅ 清晰的类和接口定义
- ✅ 异步IO实现框架

生产环境需要补充：
- ⚠️ 完整的Protobuf消息编解码
- ⚠️ 实际的网络通信实现
- ⚠️ 完整的业务逻辑

## 许可证

MIT License

## 免责声明

本项目仅供学习和研究用途。使用本脚本可能违反游戏服务条款，由此产生的一切后果由使用者自行承担。
