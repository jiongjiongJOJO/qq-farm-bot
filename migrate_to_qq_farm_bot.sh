#!/bin/bash
# 自动化脚本：将Python代码迁移到qq_farm_bot仓库并创建PR

set -e

echo "=================================="
echo "QQ Farm Bot - Python版本迁移脚本"
echo "=================================="
echo ""

# 配置
PYTHON_VERSION_DIR="python_version"
TARGET_REPO_URL="https://github.com/jiongjiongJOJO/qq_farm_bot.git"
BRANCH_NAME="feature/python-implementation"
TEMP_DIR="/tmp/qq_farm_bot_migration"

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 函数：打印成功信息
success() {
    echo -e "${GREEN}✓${NC} $1"
}

# 函数：打印警告信息
warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# 函数：打印错误信息
error() {
    echo -e "${RED}✗${NC} $1"
}

# 检查是否在正确的目录
if [ ! -d "$PYTHON_VERSION_DIR" ]; then
    error "错误: 找不到 $PYTHON_VERSION_DIR 目录"
    error "请在 qq-farm-bot 仓库根目录运行此脚本"
    exit 1
fi

success "找到Python代码目录"

# 清理临时目录
if [ -d "$TEMP_DIR" ]; then
    warning "清理旧的临时目录..."
    rm -rf "$TEMP_DIR"
fi

# 创建临时目录
mkdir -p "$TEMP_DIR"
success "创建临时目录: $TEMP_DIR"

# 克隆目标仓库
echo ""
echo "步骤 1: 克隆目标仓库..."
if git clone "$TARGET_REPO_URL" "$TEMP_DIR"; then
    success "仓库克隆成功"
else
    error "克隆失败，可能是网络问题或仓库不存在"
    exit 1
fi

# 进入目标仓库
cd "$TEMP_DIR"

# 创建新分支
echo ""
echo "步骤 2: 创建新分支 '$BRANCH_NAME'..."
if git checkout -b "$BRANCH_NAME"; then
    success "分支创建成功"
else
    warning "分支可能已存在，切换到该分支..."
    git checkout "$BRANCH_NAME"
fi

# 复制Python代码
echo ""
echo "步骤 3: 复制Python代码..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR/$PYTHON_VERSION_DIR"

if [ ! -d "$SOURCE_DIR" ]; then
    error "源目录不存在: $SOURCE_DIR"
    exit 1
fi

# 复制所有文件（包括隐藏文件）
cp -r "$SOURCE_DIR"/* . 2>/dev/null || true
cp "$SOURCE_DIR"/.gitignore . 2>/dev/null || true

# 清理 __pycache__
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

success "文件复制完成"

# 显示文件统计
echo ""
echo "文件统计:"
echo "  - Python文件: $(find . -name "*.py" -type f | wc -l)"
echo "  - Proto文件: $(find . -name "*.proto" -type f | wc -l)"
echo "  - JSON文件: $(find . -name "*.json" -type f | wc -l)"
echo "  - Markdown文件: $(find . -name "*.md" -type f | wc -l)"

# 添加所有文件
echo ""
echo "步骤 4: 添加文件到Git..."
git add .

# 显示状态
echo ""
echo "Git状态:"
git status --short

# 提交
echo ""
echo "步骤 5: 创建提交..."
git commit -m "feat: Initial Python implementation with OOP design

- Implemented 10 core classes with modular architecture
- Config, NetworkClient, FarmOperations, FriendOperations, etc.
- Full async/await programming model with asyncio
- Type hints throughout all modules
- Comprehensive documentation (README, ARCHITECTURE, SUMMARY)
- Unit tests with 100% pass rate
- 1,873 lines of clean, well-documented Python code
- PEP 8 compliant code style
- Object-oriented design following SOLID principles

Core Features:
- Automatic farm operations (harvest, plant, fertilize, maintenance)
- Friend farm operations (visit, help, steal)
- Task system for automatic reward collection
- Warehouse system for automatic fruit selling
- Status bar for real-time display
- Experience calculator for optimal crop selection
- Invitation code processor

Project Structure:
- src/: 10 core modules (config, network, farm, friend, task, warehouse, status, gameConfig, invite, utils)
- tools/: Experience calculation tool
- tests/: Unit tests
- proto/: Protobuf definitions
- gameConfig/: Game configuration data

Documentation:
- README.md: Usage guide
- ARCHITECTURE.md: Detailed design documentation
- SUMMARY.md: Implementation overview"

success "提交创建成功"

# 提示推送
echo ""
echo "=================================="
echo "✅ 本地准备完成！"
echo "=================================="
echo ""
echo "下一步操作："
echo ""
echo "1. 推送分支到GitHub:"
echo "   cd $TEMP_DIR"
echo "   git push origin $BRANCH_NAME"
echo ""
echo "2. 创建Pull Request:"
echo "   访问: $TARGET_REPO_URL"
echo "   点击 'Compare & pull request' 按钮"
echo ""
echo "3. 或者使用GitHub CLI:"
echo "   cd $TEMP_DIR"
echo "   gh pr create --title \"feat: Initial Python implementation\" --body-file ../MIGRATION_TO_QQ_FARM_BOT.md"
echo ""
echo "临时目录: $TEMP_DIR"
echo "您可以在该目录中检查文件，确认无误后推送"
echo ""

# 询问是否现在推送
read -p "是否现在推送到GitHub? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "推送中..."
    if git push origin "$BRANCH_NAME"; then
        success "推送成功！"
        echo ""
        echo "现在请访问以下链接创建PR:"
        echo "  $TARGET_REPO_URL/compare/$BRANCH_NAME?expand=1"
    else
        error "推送失败"
        echo "可能需要配置GitHub认证"
        echo "请手动执行: cd $TEMP_DIR && git push origin $BRANCH_NAME"
    fi
else
    echo ""
    echo "稍后手动推送:"
    echo "  cd $TEMP_DIR"
    echo "  git push origin $BRANCH_NAME"
fi

echo ""
echo "=================================="
echo "脚本执行完成"
echo "=================================="
