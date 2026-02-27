from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import market, limit_up
from trading.data.database import init_database

app = FastAPI(
    title="Five-Day-Line Trading API",
    description="Backend service for stock market analysis",
    version="1.0.0",
)

# 配置 CORS 允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应改为前端具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(market.router, prefix="/api/v1")
app.include_router(limit_up.router, prefix="/api/v1")

# 启动时初始化数据库
@app.on_event("startup")
async def startup_event():
    init_database()


@app.get("/")
def health_check():
    return {"status": "ok", "service": "Five-Day-Line API"}
