#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
투자메이트 서버 테스트 스크립트
"""

import asyncio
import sys
import numpy as np
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.tools.investment_tools import InvestmentTools
from src.tools.sample_data import get_sample_user_data

async def test_investment_tools():
    """투자메이트 도구 테스트"""
    print("🚀 투자메이트 도구 테스트 시작")
    
    # 도구 인스턴스 생성
    tools = InvestmentTools()
    
    # 샘플 데이터 로드
    sample_data = get_sample_user_data()
    user_id = sample_data["personal_info"]["user_id"]
    
    try:
        # 1. 리스크 프로파일 평가 테스트
        print("\n1️⃣ 리스크 프로파일 평가 테스트")
        risk_result = await tools.assess_risk_profile(
            user_id=user_id,
            risk_questionnaire={"risk_tolerance_score": 65}
        )
        print(f"✅ 리스크 프로파일 평가 결과: {risk_result['status']}")
        if risk_result['status'] == 'success':
            risk_assessment = risk_result['risk_assessment']
            print(f"   리스크 점수: {risk_assessment['risk_score']:.1f}")
            print(f"   리스크 프로파일: {risk_assessment['risk_profile']}")
            print(f"   최대 주식 비중: {risk_assessment['max_stock_ratio']*100:.1f}%")
        else:
            print(f"   오류 메시지: {risk_result.get('message', '알 수 없는 오류')}")
        
        # 2. 시장 변동성 분석 테스트
        print("\n2️⃣ 시장 변동성 분석 테스트")
        volatility_result = await tools.analyze_market_volatility()
        print(f"✅ 시장 변동성 분석 결과: {volatility_result['status']}")
        if volatility_result['status'] == 'success':
            vol_analysis = volatility_result['volatility_analysis']
            print(f"   전체 변동성: {vol_analysis['overall_volatility']*100:.2f}%")
            print(f"   시장 체제: {vol_analysis['market_regime']}")
            print(f"   권장사항: {vol_analysis['recommendation']}")
        else:
            print(f"   오류 메시지: {volatility_result.get('message', '알 수 없는 오류')}")
        
        # 3. 계좌 활용 최적화 테스트
        print("\n3️⃣ 계좌 활용 최적화 테스트")
        account_result = await tools.optimize_account_utilization(
            user_id=user_id
        )
        print(f"✅ 계좌 활용 최적화 결과: {account_result['status']}")
        if account_result['status'] == 'success':
            opt_result = account_result['optimization_result']
            print(f"   연간 저축 가능액: {opt_result['annual_savings_capacity']:,.0f}원")
            print(f"   세제 혜택: {opt_result['tax_benefits']['총_세제혜택']:,.0f}원")
            print("   계좌별 배분:")
            for account, amount in opt_result['tax_advantaged_allocation'].items():
                print(f"     {account}: {amount:,.0f}원")
        else:
            print(f"   오류 메시지: {account_result.get('message', '알 수 없는 오류')}")
        
        # 4. 포트폴리오 옵션 생성 테스트
        print("\n4️⃣ 포트폴리오 옵션 생성 테스트")
        portfolio_result = await tools.generate_portfolio_options(
            user_id=user_id,
            risk_profile="moderate"
        )
        print(f"✅ 포트폴리오 옵션 생성 결과: {portfolio_result['status']}")
        if portfolio_result['status'] == 'success':
            port_options = portfolio_result['portfolio_options']
            selected = port_options['selected_portfolio']
            print(f"   선택된 포트폴리오: {selected['description']}")
            print(f"   주식 비중: {selected['stocks']*100:.1f}%")
            print(f"   채권 비중: {selected['bonds']*100:.1f}%")
            print(f"   예상 수익률: {selected['expected_return']*100:.1f}%")
            print(f"   예상 변동성: {selected['expected_volatility']*100:.1f}%")
        else:
            print(f"   오류 메시지: {portfolio_result.get('message', '알 수 없는 오류')}")
        
        # 5. 변동성 조정 테스트
        print("\n5️⃣ 변동성 조정 테스트")
        base_portfolio = {"stocks": 0.35, "bonds": 0.40, "cash": 0.10, "alternatives": 0.15}
        adjustment_result = await tools.adjust_for_volatility(
            base_portfolio=base_portfolio,
            market_volatility=0.025  # 2.5% 변동성
        )
        print(f"✅ 변동성 조정 결과: {adjustment_result['status']}")
        if adjustment_result['status'] == 'success':
            adj_result = adjustment_result['adjustment_result']
            print(f"   조정 유형: {adj_result['adjustment_type']}")
            print(f"   조정 사유: {adj_result['adjustment_reason']}")
            print("   조정된 포트폴리오:")
            for asset, ratio in adj_result['adjusted_portfolio'].items():
                print(f"     {asset}: {ratio*100:.1f}%")
        else:
            print(f"   오류 메시지: {adjustment_result.get('message', '알 수 없는 오류')}")
        
        # 6. 실행 계획 수립 테스트
        print("\n6️⃣ 실행 계획 수립 테스트")
        implementation_result = await tools.create_implementation_plan(
            user_id=user_id,
            target_portfolio={"stocks": 0.35, "bonds": 0.40, "cash": 0.10, "alternatives": 0.15}
        )
        print(f"✅ 실행 계획 수립 결과: {implementation_result['status']}")
        if implementation_result['status'] == 'success':
            impl_result = implementation_result['implementation_plan']
            print(f"   총 투자금액: {impl_result['total_investment']:,.0f}원")
            print(f"   리밸런싱 비용: {impl_result['rebalancing_cost']:,.0f}원")
            print("   실행 단계:")
            for step in impl_result['implementation_steps']:
                print(f"     {step['step']}. {step['action']}: {step['description']}")
        else:
            print(f"   오류 메시지: {implementation_result.get('message', '알 수 없는 오류')}")
        
        # 7. 성과 모니터링 테스트
        print("\n7️⃣ 성과 모니터링 테스트")
        # 샘플 수익률 데이터 생성
        np.random.seed(42)
        portfolio_returns = np.random.normal(0.0008, 0.015, 252).tolist()  # 1년간 일일 수익률
        benchmark_returns = np.random.normal(0.0006, 0.012, 252).tolist()
        
        performance_result = await tools.monitor_performance(
            portfolio_returns=portfolio_returns,
            benchmark_returns=benchmark_returns
        )
        print(f"✅ 성과 모니터링 결과: {performance_result['status']}")
        if performance_result['status'] == 'success':
            perf_analysis = performance_result['performance_analysis']
            metrics = perf_analysis['portfolio_metrics']
            print(f"   평균 수익률: {metrics['mean_return']*100:.2f}%")
            print(f"   변동성: {metrics['volatility']*100:.2f}%")
            print(f"   샤프 비율: {metrics['sharpe_ratio']:.2f}")
            print(f"   성과 등급: {perf_analysis['performance_rating']}")
            print("   권장사항:")
            for rec in perf_analysis['recommendations']:
                print(f"     - {rec}")
        else:
            print(f"   오류 메시지: {performance_result.get('message', '알 수 없는 오류')}")
        
        print("\n🎉 모든 투자메이트 테스트가 성공적으로 완료되었습니다!")
        
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_investment_tools())
