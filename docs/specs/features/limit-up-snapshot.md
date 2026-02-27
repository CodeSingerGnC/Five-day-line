# 打板股票快照库功能规格

## 功能概述

打板股票快照库是一个专门用于记录和分析涨停板股票数据的系统，支持通过股票编码录入涨停股票信息，自动获取并保存当天的关键交易数据。

## 需求描述

### 核心功能
1. **股票录入**: 通过股票编码录入涨停股票
2. **日期处理**: 支持指定日期或默认使用当天北京时间
3. **数据获取**: 自动获取并保存当天的完整交易数据
4. **数据查询**: 支持按条件查询历史打板记录

### 数据字段
- **基础信息**: 股票编码、股票名称、打板日期
- **价格数据**: 涨停价、开盘价、收盘价、最高价、最低价
- **市值数据**: 总市值、流通市值
- **交易数据**: 最大封板金额、成交量、成交额、换手率
- **技术指标**: 涨跌幅、量比、委比等

## 接口定义

### 1. 录入打板股票
```
POST /api/v1/limit-up/snapshots
Content-Type: application/json

{
  "symbol": "000001.SZ",
  "date": "2024-01-15",  // 可选，默认当天
  "notes": "备注信息"     // 可选
}
```

### 2. 查询打板记录
```
GET /api/v1/limit-up/snapshots
Query Parameters:
- symbol: 股票编码 (可选)
- start_date: 开始日期 (可选)
- end_date: 结束日期 (可选)
- page: 页码 (默认1)
- limit: 每页数量 (默认20)
```

### 3. 获取单条记录
```
GET /api/v1/limit-up/snapshots/{id}
```

### 4. 删除记录
```
DELETE /api/v1/limit-up/snapshots/{id}
```

## 数据模型

### LimitUpSnapshot 数据模型
```python
@dataclass
class LimitUpSnapshot:
    id: int                    # 主键
    symbol: str               # 股票编码
    name: str                 # 股票名称
    date: date                # 打板日期
    limit_price: float       # 涨停价
    open_price: float        # 开盘价
    close_price: float       # 收盘价
    high_price: float        # 最高价
    low_price: float         # 最低价
    total_market_value: float # 总市值
    circulating_market_value: float # 流通市值
    max_sealed_amount: float # 最大封板金额
    volume: float            # 成交量
    turnover: float          # 成交额
    turnover_rate: float     # 换手率
    change_percent: float    # 涨跌幅
    volume_ratio: float      # 量比
    created_at: datetime     # 创建时间
    updated_at: datetime     # 更新时间
    notes: str               # 备注
```

## 数据库设计

### 表结构设计
```sql
CREATE TABLE limit_up_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    limit_price DECIMAL(10,3) NOT NULL,
    open_price DECIMAL(10,3) NOT NULL,
    close_price DECIMAL(10,3) NOT NULL,
    high_price DECIMAL(10,3) NOT NULL,
    low_price DECIMAL(10,3) NOT NULL,
    total_market_value DECIMAL(20,2),
    circulating_market_value DECIMAL(20,2),
    max_sealed_amount DECIMAL(20,2),
    volume DECIMAL(20,2),
    turnover DECIMAL(20,2),
    turnover_rate DECIMAL(8,4),
    change_percent DECIMAL(8,4),
    volume_ratio DECIMAL(8,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    UNIQUE(symbol, date)
);

CREATE INDEX idx_symbol_date ON limit_up_snapshots(symbol, date);
CREATE INDEX idx_date ON limit_up_snapshots(date);
```

## 验收标准

### 功能验收
1. ✅ 成功录入指定股票的打板数据
2. ✅ 自动获取当天完整交易数据
3. ✅ 支持按日期和股票编码查询
4. ✅ 数据验证和错误处理完善
5. ✅ 支持批量导入和导出

### 性能验收
1. ✅ 单次录入响应时间 < 2秒
2. ✅ 查询响应时间 < 1秒
3. ✅ 支持 10万+ 记录存储
4. ✅ 并发录入支持

### 数据质量验收
1. ✅ 数据完整性验证
2. ✅ 重复数据防护
3. ✅ 数据格式标准化
4. ✅ 异常数据检测

## 测试用例

### 基础功能测试
```python
def test_create_snapshot():
    # 测试正常录入
    response = client.post("/api/v1/limit-up/snapshots", json={
        "symbol": "000001.SZ"
    })
    assert response.status_code == 201

def test_create_with_date():
    # 测试指定日期录入
    response = client.post("/api/v1/limit-up/snapshots", json={
        "symbol": "000001.SZ",
        "date": "2024-01-15"
    })
    assert response.status_code == 201

def test_duplicate_prevention():
    # 测试重复录入防护
    # 第一次录入成功
    # 第二次相同股票相同日期失败
```

### 数据验证测试
```python
def test_invalid_symbol():
    # 测试无效股票编码
    response = client.post("/api/v1/limit-up/snapshots", json={
        "symbol": "INVALID"
    })
    assert response.status_code == 400

def test_future_date():
    # 测试未来日期
    future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    response = client.post("/api/v1/limit-up/snapshots", json={
        "symbol": "000001.SZ",
        "date": future_date
    })
    assert response.status_code == 400
```

## 技术选型建议

### 数据库选型
1. **SQLite** (推荐)
   - 轻量级，无需额外服务
   - 适合中小规模数据
   - 支持全文搜索
   
2. **DuckDB**
   - 更高性能的列式存储
   - 适合分析查询
   - 兼容 SQLite 语法

3. **PostgreSQL**
   - 功能最强大
   - 适合大规模数据
   - 需要额外部署

### ORM 选型
1. **SQLAlchemy** (推荐)
   - 成熟稳定
   - 支持多种数据库
   - 良好的 FastAPI 集成

2. **SQLite3 直接操作**
   - 简单直接
   - 性能较好
   - 适合简单场景

---

*文档版本: 1.0*  
*创建日期: 2026-02-26*
