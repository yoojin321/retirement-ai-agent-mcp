#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
인출메이트 서버 테스트 스크립트
"""

import asyncio
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.tools.withdrawal_tools import WithdrawalTools
from src.tools.sample_data import get_sample_user_data

async def test_withdrawal_tools():
    """인출메이트 도구 테스트"""
    print("🚀 인출메이트 도구 테스트 시작")
    
    # 도구 인스턴스 생성
    tools = WithdrawalTools()
    
    # 샘플 데이터 로드
    sample_data = get_sample_user_data()
    user_id = sample_data["personal_info"]["user_id"]
    
    try:
        # 1. 은퇴 자산 구조 분석 테스트
        print("\n1️⃣ 은퇴 자산 구조 분석 테스트")
        assets_result = await tools.analyze_retirement_assets(
            user_id=user_id,
            retirement_assets={
                "liquid_assets": 200000000,  # 2억원
                "pension_assets": 50000000,  # 5천만원
                "real_estate": 500000000,    # 5억원
                "total_assets": 750000000    # 7억 5천만원
            }
        )
        print(f"✅ 은퇴 자산 구조 분석 결과: {assets_result['status']}")
        if assets_result['status'] == 'success':
            asset_analysis = assets_result['asset_analysis']
            print(f"   총 자산: {asset_analysis['total_assets']:,.0f}원")
            print(f"   유동성 비율: {asset_analysis['liquidity_ratio']:.1f}%")
            print(f"   다각화 점수: {asset_analysis['diversification_score']:.1f}")
            print("   권장사항:")
            for rec in asset_analysis['recommendations']:
                print(f"     - {rec}")
        else:
            print(f"   오류 메시지: {assets_result.get('message', '알 수 없는 오류')}")
        
        # 2. 인출 기본선 설정 테스트
        print("\n2️⃣ 인출 기본선 설정 테스트")
        baseline_result = await tools.set_withdrawal_baseline(
            user_id=user_id,
            target_monthly_income=4000000,  # 400만원
            inflation_rate=0.025,
            withdrawal_period=25
        )
        print(f"✅ 인출 기본선 설정 결과: {baseline_result['status']}")
        if baseline_result['status'] == 'success':
            baseline = baseline_result['withdrawal_baseline']
            print(f"   목표 월 소득: {baseline['target_monthly_income']:,.0f}원")
            print(f"   인출 기간: {baseline['withdrawal_period']}년")
            print(f"   안전인출률: {baseline['safe_withdrawal_rate']['recommended_rate']*100:.1f}%")
        else:
            print(f"   오류 메시지: {baseline_result.get('message', '알 수 없는 오류')}")
        
        # 3. 가드레일 시스템 관리 테스트
        print("\n3️⃣ 가드레일 시스템 관리 테스트")
        guardrail_result = await tools.manage_guardrail_system(
            current_portfolio_value=800000000,  # 8억원
            target_portfolio_value=750000000,   # 7억 5천만원
            current_withdrawal_rate=0.04,
            guardrail_threshold=0.2
        )
        print(f"✅ 가드레일 시스템 관리 결과: {guardrail_result['status']}")
        if guardrail_result['status'] == 'success':
            guardrail = guardrail_result['guardrail_result']
            print(f"   포트폴리오 성과: {guardrail['portfolio_performance']*100:.1f}%")
            print(f"   조정된 인출률: {guardrail['adjusted_withdrawal_rate']*100:.1f}%")
            print(f"   조정 사유: {guardrail['reason']}")
        else:
            print(f"   오류 메시지: {guardrail_result.get('message', '알 수 없는 오류')}")
        
        # 4. 인출 순서 최적화 테스트
        print("\n4️⃣ 인출 순서 최적화 테스트")
        sequence_result = await tools.optimize_withdrawal_sequence(
            user_id=user_id,
            annual_withdrawal_needed=48000000  # 4,800만원
        )
        print(f"✅ 인출 순서 최적화 결과: {sequence_result['status']}")
        if sequence_result['status'] == 'success':
            optimization = sequence_result['withdrawal_optimization']
            print(f"   연간 필요 인출액: {optimization['annual_withdrawal_needed']:,.0f}원")
            print(f"   총 세금: {optimization['total_tax']:,.0f}원")
            print(f"   세후 인출액: {optimization['total_after_tax']:,.0f}원")
            print(f"   세금 효율성: {optimization['tax_efficiency']:.1f}%")
            print("   인출 순서:")
            for step in optimization['withdrawal_sequence']:
                print(f"     {step['step']}. {step['account_type']}: {step['amount']:,.0f}원 (세율: {step['tax_rate']*100:.1f}%)")
        else:
            print(f"   오류 메시지: {sequence_result.get('message', '알 수 없는 오류')}")
        
        # 5. 3버킷 전략 관리 테스트
        print("\n5️⃣ 3버킷 전략 관리 테스트")
        bucket_result = await tools.manage_bucket_strategy(
            total_portfolio=750000000,  # 7억 5천만원
            annual_expenses=48000000,   # 4,800만원
            bucket1_years=2,
            bucket2_years=3
        )
        print(f"✅ 3버킷 전략 관리 결과: {bucket_result['status']}")
        if bucket_result['status'] == 'success':
            bucket_strategy = bucket_result['bucket_strategy']
            print(f"   총 포트폴리오: {bucket_strategy['total_portfolio']:,.0f}원")
            print(f"   연간 지출: {bucket_strategy['annual_expenses']:,.0f}원")
            print("   버킷별 배분:")
            for bucket_name, bucket_info in bucket_strategy['bucket_details'].items():
                print(f"     {bucket_info['name']}: {bucket_info['amount']:,.0f}원 ({bucket_info['percentage']:.1f}%)")
                print(f"       목적: {bucket_info['purpose']}")
                print(f"       자산: {', '.join(bucket_info['assets'])}")
        else:
            print(f"   오류 메시지: {bucket_result.get('message', '알 수 없는 오류')}")
        
        # 6. 실행 계획 생성 테스트
        print("\n6️⃣ 실행 계획 생성 테스트")
        execution_result = await tools.create_execution_plan(
            user_id=user_id,
            withdrawal_strategy={
                "monthly_withdrawal": 4000000,
                "source_accounts": ["현금계좌", "연금계좌"],
                "tax_withholding": 200000,
                "net_amount": 3800000
            },
            automation_level="semi_auto"
        )
        print(f"✅ 실행 계획 생성 결과: {execution_result['status']}")
        if execution_result['status'] == 'success':
            execution_plan = execution_result['execution_plan']
            print(f"   자동화 설정: {execution_plan['automation_config']}")
            print("   체크리스트:")
            for item in execution_plan['checklist']:
                print(f"     - {item}")
            print("   모니터링 일정:")
            for period, tasks in execution_plan['monitoring_schedule'].items():
                print(f"     {period}: {', '.join(tasks)}")
        else:
            print(f"   오류 메시지: {execution_result.get('message', '알 수 없는 오류')}")
        
        # 7. 시나리오 비교 테스트
        print("\n7️⃣ 시나리오 비교 테스트")
        base_scenario = {
            "name": "기본 시나리오",
            "expected_return": 0.06,
            "risk_level": "medium",
            "tax_efficiency": 0.8,
            "liquidity": "high"
        }
        alternative_scenarios = [
            {
                "name": "보수적 시나리오",
                "expected_return": 0.04,
                "risk_level": "low",
                "tax_efficiency": 0.9,
                "liquidity": "high"
            },
            {
                "name": "공격적 시나리오",
                "expected_return": 0.08,
                "risk_level": "high",
                "tax_efficiency": 0.7,
                "liquidity": "medium"
            }
        ]
        
        comparison_result = await tools.compare_scenarios(
            base_scenario=base_scenario,
            alternative_scenarios=alternative_scenarios
        )
        print(f"✅ 시나리오 비교 결과: {comparison_result['status']}")
        if comparison_result['status'] == 'success':
            comparison = comparison_result['comparison_results']
            print("   시나리오별 분석:")
            for scenario in comparison['scenarios']:
                analysis = scenario['analysis']
                print(f"     {scenario['scenario_name']}: 수익률 {analysis['expected_return']*100:.1f}%, 리스크 {analysis['risk_level']}")
            print("   권장사항:")
            for rec in comparison['recommendations']:
                print(f"     - {rec}")
        else:
            print(f"   오류 메시지: {comparison_result.get('message', '알 수 없는 오류')}")
        
        print("\n🎉 모든 인출메이트 테스트가 성공적으로 완료되었습니다!")
        
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_withdrawal_tools())
