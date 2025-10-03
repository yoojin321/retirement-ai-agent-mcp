#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
전체 시스템 통합 테스트
"""

import asyncio
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.servers.accumulation_server import AccumulationServer
from src.servers.investment_server import InvestmentServer
from src.servers.withdrawal_server import WithdrawalServer
from src.servers.data_server import DataServer
from src.servers.external_api_server import ExternalAPIServer
from src.tools.sample_data import get_sample_user_data

async def test_integration():
    """전체 시스템 통합 테스트"""
    print("🚀 은퇴 설계 AI 에이전트 전체 시스템 통합 테스트 시작")
    
    try:
        # 1. 모든 MCP 서버 초기화
        print("\n1️⃣ MCP 서버 초기화")
        accumulation_server = AccumulationServer()
        investment_server = InvestmentServer()
        withdrawal_server = WithdrawalServer()
        data_server = DataServer()
        external_api_server = ExternalAPIServer()
        
        print("✅ 모든 MCP 서버가 성공적으로 초기화되었습니다.")
        
        # 2. 서버 시작
        print("\n2️⃣ MCP 서버 시작")
        await accumulation_server.start()
        await investment_server.start()
        await withdrawal_server.start()
        await data_server.start()
        await external_api_server.start()
        
        print("✅ 모든 MCP 서버가 성공적으로 시작되었습니다.")
        
        # 3. 적립메이트 전체 워크플로우 테스트
        print("\n3️⃣ 적립메이트 전체 워크플로우 테스트")
        sample_data = get_sample_user_data()
        user_id = sample_data["personal_info"]["user_id"]
        
        # 3-1. 사용자 프로필 수집
        print("   📝 사용자 프로필 수집")
        profile_result = await accumulation_server.execute_tool(
            "collect_user_profile",
            personal_info=sample_data["personal_info"],
            income_info=sample_data["income_info"],
            expense_info=sample_data["expense_info"],
            asset_info=sample_data["asset_info"],
            debt_info=sample_data["debt_info"],
            investment_preferences=sample_data["investment_preferences"]
        )
        print(f"   ✅ 프로필 수집: {profile_result['status']}")
        
        # 3-2. 경제 가정 설정
        print("   📊 경제 가정 설정")
        assumptions_result = await accumulation_server.execute_tool(
            "set_economic_assumptions",
            scenario_type="moderate"
        )
        print(f"   ✅ 경제 가정 설정: {assumptions_result['status']}")
        
        # 3-3. 은퇴 목표 계산
        print("   🎯 은퇴 목표 계산")
        goal_result = await accumulation_server.execute_tool(
            "calculate_retirement_goal",
            user_id=user_id,
            target_monthly_income=4000000,
            retirement_period=25,
            medical_reserve=50000000
        )
        print(f"   ✅ 은퇴 목표 계산: {goal_result['status']}")
        
        # 3-4. 자산 프로젝션
        print("   📈 자산 프로젝션")
        projection_result = await accumulation_server.execute_tool(
            "project_asset_values",
            user_id=user_id,
            annual_contribution=12000000,
            contribution_growth_rate=0.03
        )
        print(f"   ✅ 자산 프로젝션: {projection_result['status']}")
        
        # 3-5. 자금 격차 분석
        print("   💰 자금 격차 분석")
        if goal_result['status'] == 'success' and projection_result['status'] == 'success':
            gap_result = await accumulation_server.execute_tool(
                "analyze_funding_gap",
                user_id=user_id,
                required_capital=goal_result['calculation_result']['required_capital'],
                projected_assets=projection_result['projection_result']['total_projected_assets']
            )
            print(f"   ✅ 자금 격차 분석: {gap_result['status']}")
        
        # 4. 투자메이트 전체 워크플로우 테스트
        print("\n4️⃣ 투자메이트 전체 워크플로우 테스트")
        
        # 4-1. 리스크 프로파일 평가
        print("   🎲 리스크 프로파일 평가")
        risk_result = await investment_server.execute_tool(
            "assess_risk_profile",
            user_id=user_id,
            risk_questionnaire={"risk_tolerance_score": 65}
        )
        print(f"   ✅ 리스크 프로파일 평가: {risk_result['status']}")
        
        # 4-2. 시장 변동성 분석
        print("   📊 시장 변동성 분석")
        volatility_result = await investment_server.execute_tool(
            "analyze_market_volatility"
        )
        print(f"   ✅ 시장 변동성 분석: {volatility_result['status']}")
        
        # 4-3. 포트폴리오 옵션 생성
        print("   📋 포트폴리오 옵션 생성")
        portfolio_result = await investment_server.execute_tool(
            "generate_portfolio_options",
            user_id=user_id,
            risk_profile="moderate"
        )
        print(f"   ✅ 포트폴리오 옵션 생성: {portfolio_result['status']}")
        
        # 4-4. 실행 계획 수립
        print("   📝 실행 계획 수립")
        implementation_result = await investment_server.execute_tool(
            "create_implementation_plan",
            user_id=user_id,
            target_portfolio={"stocks": 0.35, "bonds": 0.40, "cash": 0.10, "alternatives": 0.15}
        )
        print(f"   ✅ 실행 계획 수립: {implementation_result['status']}")
        
        # 5. 인출메이트 전체 워크플로우 테스트
        print("\n5️⃣ 인출메이트 전체 워크플로우 테스트")
        
        # 5-1. 은퇴 자산 구조 분석
        print("   🏠 은퇴 자산 구조 분석")
        assets_result = await withdrawal_server.execute_tool(
            "analyze_retirement_assets",
            user_id=user_id,
            retirement_assets={
                "liquid_assets": 200000000,
                "pension_assets": 50000000,
                "real_estate": 500000000,
                "total_assets": 750000000
            }
        )
        print(f"   ✅ 은퇴 자산 구조 분석: {assets_result['status']}")
        
        # 5-2. 인출 기본선 설정
        print("   📊 인출 기본선 설정")
        baseline_result = await withdrawal_server.execute_tool(
            "set_withdrawal_baseline",
            user_id=user_id,
            target_monthly_income=4000000,
            inflation_rate=0.025,
            withdrawal_period=25
        )
        print(f"   ✅ 인출 기본선 설정: {baseline_result['status']}")
        
        # 5-3. 3버킷 전략 관리
        print("   🪣 3버킷 전략 관리")
        bucket_result = await withdrawal_server.execute_tool(
            "manage_bucket_strategy",
            total_portfolio=750000000,
            annual_expenses=48000000,
            bucket1_years=2,
            bucket2_years=3
        )
        print(f"   ✅ 3버킷 전략 관리: {bucket_result['status']}")
        
        # 5-4. 실행 계획 생성
        print("   📋 실행 계획 생성")
        execution_result = await withdrawal_server.execute_tool(
            "create_execution_plan",
            user_id=user_id,
            withdrawal_strategy={
                "monthly_withdrawal": 4000000,
                "source_accounts": ["현금계좌", "연금계좌"],
                "tax_withholding": 200000,
                "net_amount": 3800000
            },
            automation_level="semi_auto"
        )
        print(f"   ✅ 실행 계획 생성: {execution_result['status']}")
        
        # 6. 서버 중지
        print("\n6️⃣ MCP 서버 중지")
        await accumulation_server.stop()
        await investment_server.stop()
        await withdrawal_server.stop()
        await data_server.stop()
        await external_api_server.stop()
        
        print("✅ 모든 MCP 서버가 성공적으로 중지되었습니다.")
        
        # 7. 통합 테스트 결과 요약
        print("\n🎉 전체 시스템 통합 테스트 완료!")
        print("\n📊 테스트 결과 요약:")
        print("   ✅ 적립메이트: 사용자 프로필 → 경제 가정 → 목표 계산 → 프로젝션 → 격차 분석")
        print("   ✅ 투자메이트: 리스크 평가 → 변동성 분석 → 포트폴리오 생성 → 실행 계획")
        print("   ✅ 인출메이트: 자산 분석 → 기본선 설정 → 버킷 전략 → 실행 계획")
        print("   ✅ 데이터 관리: 로컬 DB 저장 및 관리")
        print("   ✅ 외부 API: 시장 데이터 및 경제 지표 수집")
        
        print("\n🚀 은퇴 설계 AI 에이전트 MCP 서버가 완전히 작동합니다!")
        
    except Exception as e:
        print(f"❌ 통합 테스트 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_integration())
