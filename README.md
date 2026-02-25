# Five-day-line — 运行指南

## 项目概览

-   后端：FastAPI（A 股数据由 Akshare 提供封装），入口见 [main.py](file:///Users/wangkangru/develop/non_open_source/Finance/Five-day-line/src/api/main.py) 和路由 [market.py](file:///Users/wangkangru/develop/non_open_source/Finance/Five-day-line/src/api/routers/market.py)
-   前端：Next.js + Tremor UI + Lightweight Charts，可视化页面见 [page.tsx](file:///Users/wangkangru/develop/non_open_source/Finance/Five-day-line/web/app/page.tsx) 与图表组件 [CandlestickChart.tsx](file:///Users/wangkangru/develop/non_open_source/Finance/Five-day-line/web/components/chart/CandlestickChart.tsx)
-   代码布局：Python 使用 src-layout（PYTHONPATH=src），前端在 web/ 目录

## 环境要求

-   Python：3.8+（推荐 3.11 及以上）并安装 uv 包管理器
-   Node.js：18+（建议 18 LTS 或以上）

## 快速开始（脚本）

-   一键启动（自动安装前端依赖、自动避让端口占用）：

```bash
./scripts/dev.sh
```

-   指定端口（可选）：

```bash
BACKEND_PORT=8010 FRONTEND_PORT=3010 ./scripts/dev.sh
```

-   仅启动后端或前端：

```bash
./scripts/dev.sh --backend-only
./scripts/dev.sh --frontend-only
```

-   停止并回收资源（优雅退出，必要时强制）：

```bash
./scripts/stop.sh
./scripts/stop.sh --force
```

脚本位置：

-   启动脚本：[scripts/dev.sh](file:///Users/wangkangru/develop/non_open_source/Finance/Five-day-line/scripts/dev.sh)
-   退出脚本：[scripts/stop.sh](file:///Users/wangkangru/develop/non_open_source/Finance/Five-day-line/scripts/stop.sh)

## 安装 uv（如未安装）

macOS / Linux：

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

Windows（PowerShell）：

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

## 后端（FastAPI）运行

1. 安装依赖

```bash
cd /path/to/Five-day-line
uv sync
```

2. 启动开发服务（热重载）

```bash
PYTHONPATH=src uv run uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

3. 验证接口

-   文档：打开 http://localhost:8000/docs
-   示例：获取平安银行最近日线

```bash
curl "http://localhost:8000/api/v1/market/bars/000001.SZ?start=2024-01-01&end=2024-01-10"
```

## 前端（Next.js）运行

1. 安装依赖

```bash
cd web
npm install
```

2. 启动开发服务

```bash
npm run dev
```

3. 打开页面

-   浏览器访问：http://localhost:3000
-   页面默认拉取后端 `http://localhost:8000` 的数据进行 K 线渲染

## 生产构建

-   后端：

```bash
PYTHONPATH=src uv run uvicorn api.main:app --host 0.0.0.0 --port 8000
```

-   前端：

```bash
cd web
npm run build
npm run start
```

## 测试（可选）

如果仓库包含测试：

```bash
PYTHONPATH=src uv run -m pytest -q
```

## 常见问题

-   前端请求失败
    -   确认后端已在 :8000 启动，且 CORS 已允许（已在后端开启）
    -   检查前端请求的接口地址是否正确
-   安装速度慢
    -   使用 uv.lock 快速安装：`uv sync`
    -   根据网络情况配置国内镜像（如需，我可为 uv 配置提供示例）

## 目录参考

-   后端入口：[src/api/main.py](file:///Users/wangkangru/develop/non_open_source/Finance/Five-day-line/src/api/main.py)
-   数据路由：[src/api/routers/market.py](file:///Users/wangkangru/develop/non_open_source/Finance/Five-day-line/src/api/routers/market.py)
-   数据模型（Bar）：[src/trading/data/models/bar.py](file:///Users/wangkangru/develop/non_open_source/Finance/Five-day-line/src/trading/data/models/bar.py)
-   可视化组件：[web/components/chart/CandlestickChart.tsx](file:///Users/wangkangru/develop/non_open_source/Finance/Five-day-line/web/components/chart/CandlestickChart.tsx)
