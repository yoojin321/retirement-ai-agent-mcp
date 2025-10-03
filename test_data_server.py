#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
데이터 관리 서버 테스트
"""

import asyncio
import json
from src.servers.data_server import DataServer

async def test_data_server():
    """데이터 관리 서버 테스트"""
    print("🔧 데이터 관리 서버 테스트 시작")
    
    # 서버 초기화
    server = DataServer()
    await server.start()
    
    test_user_id = "test_user_001"
    
    try:
        # 1. 사용자 프로필 저장 테스트
        print("\n1️⃣ 사용자 프로필 저장 테스트")
        profile_data = {
            "name": "홍길동",
            "age": 35,
            "income": 80000000,
            "email": "hong@example.com",
            "phone": "010-1234-5678",
            "ssn": "123456-1234567"
        }
        
        result = await server.manage_local_database(
            operation="create",
            table="user_profiles",
            user_id=test_user_id,
            data=profile_data
        )
        print(f"✅ 프로필 저장: {result}")
        
        # 2. 민감 데이터 암호화 테스트
        print("\n2️⃣ 민감 데이터 암호화 테스트")
        encrypted_result = await server.encrypt_sensitive_data(
            data=profile_data,
            user_id=test_user_id
        )
        print(f"✅ 암호화 결과: {encrypted_result['status']}")
        print(f"🔐 암호화된 데이터 키: {list(encrypted_result['encrypted_data'].keys())}")
        
        # 3. 암호화된 데이터 복호화 테스트
        print("\n3️⃣ 암호화된 데이터 복호화 테스트")
        decrypted_result = await server.decrypt_sensitive_data(
            encrypted_data=encrypted_result['encrypted_data'],
            user_id=test_user_id
        )
        print(f"✅ 복호화 결과: {decrypted_result['status']}")
        print(f"🔓 복호화된 데이터: {decrypted_result['decrypted_data']}")
        
        # 4. 경제 가정 저장 테스트
        print("\n4️⃣ 경제 가정 저장 테스트")
        economic_data = {
            "scenario_type": "moderate",
            "inflation_rate": 2.5,
            "market_return": 7.0,
            "risk_free_rate": 3.0
        }
        
        result = await server.manage_local_database(
            operation="create",
            table="economic_assumptions",
            user_id=test_user_id,
            data=economic_data
        )
        print(f"✅ 경제 가정 저장: {result}")
        
        # 5. 투자 포트폴리오 저장 테스트
        print("\n5️⃣ 투자 포트폴리오 저장 테스트")
        portfolio_data = {
            "portfolio_id": "portfolio_001",
            "stocks": 40,
            "bonds": 50,
            "cash": 10,
            "expected_return": 6.5,
            "volatility": 12.0
        }
        
        result = await server.manage_local_database(
            operation="create",
            table="investment_portfolios",
            user_id=test_user_id,
            data=portfolio_data
        )
        print(f"✅ 포트폴리오 저장: {result}")
        
        # 6. 데이터 백업 테스트
        print("\n6️⃣ 데이터 백업 테스트")
        backup_result = await server.backup_user_data(
            user_id=test_user_id,
            backup_type="full"
        )
        print(f"✅ 백업 완료: {backup_result}")
        
        # 7. 백업 목록 조회 테스트
        print("\n7️⃣ 백업 목록 조회 테스트")
        list_result = await server.list_backups(user_id=test_user_id)
        print(f"✅ 백업 목록: {list_result}")
        
        # 8. 데이터 복원 테스트
        print("\n8️⃣ 데이터 복원 테스트")
        if list_result['backups']:
            backup_id = list_result['backups'][0]['backup_id']
            restore_result = await server.restore_user_data(
                backup_id=backup_id,
                user_id=test_user_id
            )
            print(f"✅ 복원 완료: {restore_result}")
        
        # 9. 데이터 조회 테스트
        print("\n9️⃣ 데이터 조회 테스트")
        
        # 사용자 프로필 조회
        profile_result = await server.manage_local_database(
            operation="read",
            table="user_profiles",
            user_id=test_user_id
        )
        print(f"✅ 프로필 조회: {profile_result['status']}")
        
        # 경제 가정 조회
        economic_result = await server.manage_local_database(
            operation="read",
            table="economic_assumptions",
            user_id=test_user_id,
            scenario_type="moderate"
        )
        print(f"✅ 경제 가정 조회: {economic_result['status']}")
        
        # 포트폴리오 조회
        portfolio_result = await server.manage_local_database(
            operation="read",
            table="investment_portfolios",
            user_id=test_user_id
        )
        print(f"✅ 포트폴리오 조회: {portfolio_result['status']}")
        
        print("\n🎉 데이터 관리 서버 테스트 완료!")
        
    except Exception as e:
        print(f"❌ 테스트 실패: {str(e)}")
    
    finally:
        await server.stop()

if __name__ == "__main__":
    asyncio.run(test_data_server())
