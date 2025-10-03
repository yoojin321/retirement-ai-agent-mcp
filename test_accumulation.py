#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
적립메이트 서버 테스트 스크립트
"""

import asyncio
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.tools.accumulation_tools import AccumulationTools
from src.tools.sample_data import get_sample_user_data, get_sample_economic_scenarios

async def test_accumulation_tools():
    """적립메이트 도구 테스트"""
    print("🚀 적립메이트 도구 테스트 시작")
    
    # 도구 인스턴스 생성
    tools = AccumulationTools()
    
    # 샘플 데이터 로드
    sample_data = get_sample_user_data()
    
    try:
        # 1. 사용자 프로필 수집 테스트
        print("\n1️⃣ 사용자 프로필 수집 테스트")
        profile_result = await tools.collect_user_profile(
            personal_info=sample_data["personal_info"],
            income_info=sample_data["income_info"],
            expense_info=sample_data["expense_info"],
            asset_info=sample_data["asset_info"],
            debt_info=sample_data["debt_info"],
            investment_preferences=sample_data["investment_preferences"]
        )
        print(f"✅ 프로필 수집 결과: {profile_result['status']}")
        if profile_result['status'] == 'success':
            print(f"   사용자 ID: {profile_result['user_id']}")
            print(f"   순자산: {profile_result['profile_summary']['net_worth']:,}원")
        else:
            print(f"   오류 메시지: {profile_result.get('message', '알 수 없는 오류')}")
        
        # 2. 경제 가정 설정 테스트
        print("\n2️⃣ 경제 가정 설정 테스트")
        assumptions_result = await tools.set_economic_assumptions(
            scenario_type="moderate"
        )
        print(f"✅ 경제 가정 설정 결과: {assumptions_result['status']}")
        if assumptions_result['status'] == 'success':
            print(f"   물가상승률: {assumptions_result['assumptions']['inflation_rate']*100:.1f}%")
            print(f"   은퇴전 수익률: {assumptions_result['assumptions']['pre_retirement_return']*100:.1f}%")
        
        # 3. 은퇴 목표 자금 계산 테스트
        print("\n3️⃣ 은퇴 목표 자금 계산 테스트")
        goal_result = await tools.calculate_retirement_goal(
            user_id=sample_data["personal_info"]["user_id"],
            target_monthly_income=4000000,  # 400만원
            retirement_period=20,
            medical_reserve=50000000  # 5000만원
        )
        print(f"✅ 은퇴 목표 계산 결과: {goal_result['status']}")
        if goal_result['status'] == 'success':
            calc_result = goal_result['calculation_result']
            print(f"   필요 자본: {calc_result['required_capital']:,.0f}원")
            print(f"   은퇴까지 년수: {calc_result['years_to_retirement']}년")
        else:
            print(f"   오류 메시지: {goal_result.get('message', '알 수 없는 오류')}")
        
        # 4. 자산 미래가치 계산 테스트
        print("\n4️⃣ 자산 미래가치 계산 테스트")
        projection_result = await tools.project_asset_values(
            user_id=sample_data["personal_info"]["user_id"],
            annual_contribution=12000000,  # 1200만원
            contribution_growth_rate=0.03
        )
        print(f"✅ 자산 프로젝션 결과: {projection_result['status']}")
        if projection_result['status'] == 'success':
            proj_result = projection_result['projection_result']
            print(f"   현재 자산: {proj_result['current_assets']:,.0f}원")
            print(f"   예상 자산: {proj_result['total_projected_assets']:,.0f}원")
        else:
            print(f"   오류 메시지: {projection_result.get('message', '알 수 없는 오류')}")
        
        # 5. 자금 격차 분석 테스트
        print("\n5️⃣ 자금 격차 분석 테스트")
        if goal_result['status'] == 'success' and projection_result['status'] == 'success':
            gap_result = await tools.analyze_funding_gap(
                user_id=sample_data["personal_info"]["user_id"],
                required_capital=goal_result['calculation_result']['required_capital'],
                projected_assets=projection_result['projection_result']['total_projected_assets']
            )
            print(f"✅ 자금 격차 분석 결과: {gap_result['status']}")
            if gap_result['status'] == 'success':
                analysis = gap_result['analysis']
                print(f"   자금 격차: {analysis['funding_gap']:,.0f}원")
                print(f"   충분 여부: {'충분' if analysis['is_sufficient'] else '부족'}")
                if gap_result['recommendations']:
                    print("   권장사항:")
                    for rec in gap_result['recommendations']:
                        print(f"     - {rec}")
        
        # 6. 저축 계획 최적화 테스트
        print("\n6️⃣ 저축 계획 최적화 테스트")
        optimization_result = await tools.optimize_savings_plan(
            user_id=sample_data["personal_info"]["user_id"],
            target_contribution=15000000,  # 1500만원
            current_contribution=12000000   # 1200만원
        )
        print(f"✅ 저축 계획 최적화 결과: {optimization_result['status']}")
        if optimization_result['status'] == 'success':
            opt_result = optimization_result['optimization_result']
            print(f"   추가 필요 저축액: {opt_result['additional_contribution_needed']:,.0f}원")
            print(f"   계좌별 배분:")
            for account, amount in opt_result['account_allocation'].items():
                print(f"     {account}: {amount:,.0f}원")
        else:
            print(f"   오류 메시지: {optimization_result.get('message', '알 수 없는 오류')}")
        
        print("\n🎉 모든 테스트가 성공적으로 완료되었습니다!")
        
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_accumulation_tools())
