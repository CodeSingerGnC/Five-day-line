"""
打板股票快照API测试
"""
import pytest
from fastapi.testclient import TestClient
from datetime import date, datetime
from decimal import Decimal

from src.api.main import app
from src.trading.data.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.trading.data.models.limit_up_table import LimitUpSnapshotTable


# 创建测试数据库
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# 创建测试客户端
client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    """设置测试数据库"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestLimitUpAPI:
    """打板快照API测试类"""
    
    def test_health_check(self):
        """测试健康检查接口"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "service" in data
    
    def test_create_snapshot_success(self):
        """测试成功创建打板快照"""
        snapshot_data = {
            "symbol": "000001.SZ",
            "date": "2024-01-15",
            "notes": "测试打板快照"
        }
        
        response = client.post("/api/v1/limit-up/snapshots", json=snapshot_data)
        
        # 检查响应状态
        assert response.status_code == 201
        
        # 检查响应数据结构
        data = response.json()
        assert data["symbol"] == "000001.SZ"
        assert data["snapshot_date"] == "2024-01-15"
        assert data["notes"] == "测试打板快照"
        assert "id" in data
        assert "created_at" in data
        assert "is_limit_up" in data
    
    def test_create_snapshot_invalid_symbol(self):
        """测试无效股票编码"""
        snapshot_data = {
            "symbol": "INVALID",
            "date": "2024-01-15"
        }
        
        response = client.post("/api/v1/limit-up/snapshots", json=snapshot_data)
        assert response.status_code == 400
        assert "获取股票" in response.json()["detail"]
    
    def test_create_snapshot_future_date(self):
        """测试未来日期"""
        future_date = (datetime.now().date() + datetime.timedelta(days=1)).isoformat()
        snapshot_data = {
            "symbol": "000001.SZ",
            "date": future_date
        }
        
        response = client.post("/api/v1/limit-up/snapshots", json=snapshot_data)
        assert response.status_code == 400
    
    def test_create_duplicate_snapshot(self):
        """测试重复录入"""
        snapshot_data = {
            "symbol": "000001.SZ",
            "date": "2024-01-16"
        }
        
        # 第一次录入
        response1 = client.post("/api/v1/limit-up/snapshots", json=snapshot_data)
        assert response1.status_code == 201
        
        # 第二次录入相同股票相同日期
        response2 = client.post("/api/v1/limit-up/snapshots", json=snapshot_data)
        assert response2.status_code == 400
        assert "已存在" in response2.json()["detail"]
    
    def test_list_snapshots_empty(self):
        """测试查询空列表"""
        response = client.get("/api/v1/limit-up/snapshots")
        assert response.status_code == 200
        
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0
        assert data["page"] == 1
        assert data["limit"] == 20
        assert data["pages"] == 0
    
    def test_list_snapshots_with_data(self):
        """测试查询有数据的列表"""
        # 先创建一些测试数据
        test_snapshots = [
            {"symbol": "000001.SZ", "date": "2024-01-10"},
            {"symbol": "600000.SH", "date": "2024-01-11"},
            {"symbol": "000333.SZ", "date": "2024-01-12"}
        ]
        
        for snapshot in test_snapshots:
            client.post("/api/v1/limit-up/snapshots", json=snapshot)
        
        # 查询列表
        response = client.get("/api/v1/limit-up/snapshots")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["items"]) == 3
        assert data["total"] == 3
        assert data["page"] == 1
        assert data["pages"] == 1
        
        # 检查数据按日期降序排列
        dates = [item["snapshot_date"] for item in data["items"]]
        assert dates == sorted(dates, reverse=True)
    
    def test_list_snapshots_with_filters(self):
        """测试带过滤条件的查询"""
        # 创建测试数据
        client.post("/api/v1/limit-up/snapshots", json={"symbol": "000001.SZ", "date": "2024-01-10"})
        client.post("/api/v1/limit-up/snapshots", json={"symbol": "600000.SH", "date": "2024-01-11"})
        
        # 按股票编码过滤
        response = client.get("/api/v1/limit-up/snapshots?symbol=000001.SZ")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["symbol"] == "000001.SZ"
        
        # 按日期范围过滤
        response = client.get("/api/v1/limit-up/snapshots?start_date=2024-01-10&end_date=2024-01-10")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["snapshot_date"] == "2024-01-10"
    
    def test_list_snapshots_pagination(self):
        """测试分页查询"""
        # 创建多个测试数据
        for i in range(25):
            client.post("/api/v1/limit-up/snapshots", json={
                "symbol": f"00000{i}.SZ",
                "date": f"2024-01-{i+1:02d}"
            })
        
        # 第一页
        response = client.get("/api/v1/limit-up/snapshots?page=1&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 10
        assert data["total"] == 25
        assert data["page"] == 1
        assert data["pages"] == 3
        
        # 第二页
        response = client.get("/api/v1/limit-up/snapshots?page=2&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 10
        assert data["page"] == 2
    
    def test_get_snapshot_by_id_success(self):
        """测试根据ID获取快照"""
        # 创建快照
        create_response = client.post("/api/v1/limit-up/snapshots", json={
            "symbol": "000001.SZ",
            "date": "2024-01-20",
            "notes": "测试获取"
        })
        assert create_response.status_code == 201
        
        snapshot_id = create_response.json()["id"]
        
        # 获取快照
        response = client.get(f"/api/v1/limit-up/snapshots/{snapshot_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == snapshot_id
        assert data["symbol"] == "000001.SZ"
        assert data["notes"] == "测试获取"
    
    def test_get_snapshot_by_id_not_found(self):
        """测试获取不存在的快照"""
        response = client.get("/api/v1/limit-up/snapshots/99999")
        assert response.status_code == 404
        assert "不存在" in response.json()["detail"]
    
    def test_delete_snapshot_success(self):
        """测试删除快照"""
        # 创建快照
        create_response = client.post("/api/v1/limit-up/snapshots", json={
            "symbol": "000001.SZ",
            "date": "2024-01-21"
        })
        assert create_response.status_code == 201
        
        snapshot_id = create_response.json()["id"]
        
        # 删除快照
        response = client.delete(f"/api/v1/limit-up/snapshots/{snapshot_id}")
        assert response.status_code == 204
        
        # 确认已删除
        get_response = client.get(f"/api/v1/limit-up/snapshots/{snapshot_id}")
        assert get_response.status_code == 404
    
    def test_delete_snapshot_not_found(self):
        """测试删除不存在的快照"""
        response = client.delete("/api/v1/limit-up/snapshots/99999")
        assert response.status_code == 404
    
    def test_statistics_endpoint(self):
        """测试统计接口"""
        # 创建一些测试数据
        for i in range(5):
            client.post("/api/v1/limit-up/snapshots", json={
                "symbol": "000001.SZ",
                "date": f"2024-01-{i+1:02d}"
            })
        
        response = client.get("/api/v1/limit-up/snapshots/statistics")
        assert response.status_code == 200
        
        data = response.json()
        assert "total_snapshots" in data
        assert "today_new" in data
        assert "most_active_stocks" in data
        assert "latest_date" in data
        
        assert data["total_snapshots"] >= 5
        assert isinstance(data["most_active_stocks"], list)
    
    def test_create_snapshot_default_date(self):
        """测试使用默认日期（今天）创建快照"""
        snapshot_data = {
            "symbol": "000002.SZ"
            # 不提供date字段
        }
        
        response = client.post("/api/v1/limit-up/snapshots", json=snapshot_data)
        assert response.status_code == 201
        
        data = response.json()
        # 检查日期是今天
        today = date.today().isoformat()
        assert data["snapshot_date"] == today
    
    def test_create_snapshot_without_notes(self):
        """测试不提供备注创建快照"""
        snapshot_data = {
            "symbol": "000002.SZ",
            "date": "2024-01-22"
        }
        
        response = client.post("/api/v1/limit-up/snapshots", json=snapshot_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["notes"] is None


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])
