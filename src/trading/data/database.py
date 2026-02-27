"""
数据库连接和配置管理
"""
import os
from pathlib import Path
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator

# 数据库文件路径
DB_DIR = Path(__file__).parent.parent.parent.parent / "data"
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "limit_up.db"

# 数据库连接配置
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# 创建数据库引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,  # SQLite 特定配置
        "timeout": 20,               # 查询超时时间
    },
    poolclass=StaticPool,           # SQLite 使用静态连接池
    echo=False,                      # 生产环境关闭 SQL 日志
)

# 启用外键约束（SQLite 特定）
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA journal_mode=WAL")  # 启用 WAL 模式提升并发性能
    cursor.close()

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    获取数据库会话
    
    用于 FastAPI 依赖注入
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_database():
    """
    初始化数据库表结构
    
    在应用启动时调用
    """
    from trading.data.models.limit_up_table import LimitUpSnapshotTable
    
    # 创建所有表
    LimitUpSnapshotTable.metadata.create_all(bind=engine)
    print(f"数据库初始化完成: {DB_PATH}")


def get_database_info() -> dict:
    """
    获取数据库信息
    """
    return {
        "path": str(DB_PATH),
        "size": DB_PATH.stat().st_size if DB_PATH.exists() else 0,
        "url": SQLALCHEMY_DATABASE_URL
    }
