#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP 클라이언트 테스트 - Claude 연결 전 테스트용
"""

import asyncio
import json
import sys
import os
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.servers.accumulation_server import AccumulationServer
from src.servers.investment_server import InvestmentServer
from src.servers.withdrawal_server import WithdrawalServer
from src.servers.data_server import DataServer
from src.servers.external_api_server import ExternalAPIServer

async def test_mcp_servers():
    """MCP 서버들 테스트"""
    print("🔧 MCP 서버 테스트 시작")
    print("=" * 50)
    
    # 서버들 초기화
    accumulation_server = AccumulationServer()
    investment_server = InvestmentServer()
    withdrawal_server = WithdrawalServer()
    data_server = DataServer()
    external_api_server = ExternalAPIServer()
    
    try:
        # 모든 서버 시작
        await accumulation_server.start()
        await investment_server.start()
        await withdrawal_server.start()
        await data_server.start()
        await external_api_server.start()
        
        print("✅ 모든 MCP 서버가 성공적으로 시작되었습니다.")
        
        # 적립메이트 테스트
        print("\n1️⃣ 적립메이트 테스트")
        accumulation_result = await accumulation_server.collect_user_profile(
            user_id="test_user_001",
            age=35,
            income=80000000,
            current_assets=500000000,
            retirement_age=65,
            target_assets=750000000,
            risk_tolerance="중립적"
        )
        print(f"✅ 적립메이트: {accumulation_result['status']}")
        
        # 투자메이트 테스트
        print("\n2️⃣ 투자메이트 테스트")
        investment_result = await investment_server.evaluate_risk_profile(
            user_id="test_user_001",
            age=35,
            income=80000000,
            assets=500000000,
            investment_experience="중급",
            risk_tolerance="중립적",
            time_horizon=30
        )
        print(f"✅ 투자메이트: {investment_result['status']}")
        
        # 인출메이트 테스트
        print("\n3️⃣ 인출메이트 테스트")
        withdrawal_result = await withdrawal_server.analyze_retirement_assets(
            user_id="test_user_001",
            total_assets=750000000,
            monthly_income_needed=4000000,
            retirement_years=25,
            inflation_rate=2.5,
            tax_rate=20.0,
            risk_tolerance="중립적"
        )
        print(f"✅ 인출메이트: {withdrawal_result['status']}")
        
        # 데이터 관리 테스트
        print("\n4️⃣ 데이터 관리 테스트")
        data_result = await data_server.backup_user_data(
            user_id="test_user_001",
            backup_type="full"
        )
        print(f"✅ 데이터 관리: {data_result['status']}")
        
        # 외부 API 테스트
        print("\n5️⃣ 외부 API 테스트")
        external_result = await external_api_server.fetch_market_data(
            symbols=["^GSPC", "QQQ"],
            period="1mo"
        )
        print(f"✅ 외부 API: {external_result['status']}")
        
        print("\n🎉 모든 MCP 서버 테스트 완료!")
        
        # 서버 상태 확인
        print("\n📊 서버 상태:")
        print(f"- 적립메이트: {'실행 중' if accumulation_server.is_running else '중지됨'}")
        print(f"- 투자메이트: {'실행 중' if investment_server.is_running else '중지됨'}")
        print(f"- 인출메이트: {'실행 중' if withdrawal_server.is_running else '중지됨'}")
        print(f"- 데이터 관리: {'실행 중' if data_server.is_running else '중지됨'}")
        print(f"- 외부 API: {'실행 중' if external_api_server.is_running else '중지됨'}")
        
    except Exception as e:
        print(f"❌ 테스트 실패: {str(e)}")
    
    finally:
        # 모든 서버 중지
        await accumulation_server.stop()
        await investment_server.stop()
        await withdrawal_server.stop()
        await data_server.stop()
        await external_api_server.stop()
        print("\n🛑 모든 MCP 서버가 중지되었습니다.")

if __name__ == "__main__":
    asyncio.run(test_mcp_servers())
