"""
简化的API测试
"""
import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    print("🧪 测试API接口...")
    
    # 1. 测试健康检查
    print("\n1. 测试健康检查...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {response.json()}")
        assert response.status_code == 200
        print("   ✅ 健康检查通过")
    except Exception as e:
        print(f"   ❌ 健康检查失败: {e}")
        return
    
    # 2. 测试创建打板快照
    print("\n2. 测试创建打板快照...")
    try:
        snapshot_data = {
            "symbol": "600519.SH"  # 使用今天日期
        }
        
        response = requests.post(
            f"{base_url}/api/v1/limit-up/snapshots",
            json=snapshot_data
        )
        print(f"   状态码: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            print(f"   创建成功: ID={data.get('id')}")
            print("   ✅ 创建快照通过")
            snapshot_id = data.get('id')
        else:
            print(f"   响应: {response.text}")
            print("   ❌ 创建快照失败")
            return
    except Exception as e:
        print(f"   ❌ 创建快照异常: {e}")
        return
    
    # 3. 测试查询快照列表
    print("\n3. 测试查询快照列表...")
    try:
        response = requests.get(f"{base_url}/api/v1/limit-up/snapshots")
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   查询到 {data.get('total', 0)} 条记录")
            print("   ✅ 查询列表通过")
        else:
            print(f"   响应: {response.text}")
            print("   ❌ 查询列表失败")
    except Exception as e:
        print(f"   ❌ 查询列表异常: {e}")
    
    # 4. 测试获取单个快照
    print("\n4. 测试获取单个快照...")
    try:
        response = requests.get(f"{base_url}/api/v1/limit-up/snapshots/{snapshot_id}")
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   快照详情: {data.get('symbol')} - {data.get('snapshot_date')}")
            print("   ✅ 获取单个快照通过")
        else:
            print(f"   响应: {response.text}")
            print("   ❌ 获取单个快照失败")
    except Exception as e:
        print(f"   ❌ 获取单个快照异常: {e}")
    
    # 5. 测试统计接口
    print("\n5. 测试统计接口...")
    try:
        response = requests.get(f"{base_url}/api/v1/limit-up/snapshots/statistics")
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   统计信息: 总数={data.get('total_snapshots')}")
            print("   ✅ 统计接口通过")
        else:
            print(f"   响应: {response.text}")
            print("   ❌ 统计接口失败")
    except Exception as e:
        print(f"   ❌ 统计接口异常: {e}")
    
    print("\n🎉 API测试完成!")

if __name__ == "__main__":
    test_api()
