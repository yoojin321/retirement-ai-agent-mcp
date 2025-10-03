#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
외부 API 서버 테스트
"""

import asyncio
from src.servers.external_api_server import ExternalAPIServer

async def test_external_api():
    """외부 API 서버 테스트"""
    print("🌐 외부 API 서버 테스트 시작")
    
    # 서버 초기화
    server = ExternalAPIServer()
    await server.start()
    
    try:
        # 1. 시장 데이터 수집 테스트
        print("\n1️⃣ 시장 데이터 수집 테스트")
        market_result = await server.fetch_market_data(
            symbols=["^GSPC", "QQQ", "SPY"],
            period="5d"
        )
        print(f"✅ 시장 데이터: {market_result['status']}")
        if market_result['status'] == 'success':
            print(f"📊 수집된 데이터: {len(market_result['data'])}개 심볼")
        
        # 2. 경제 지표 수집 테스트
        print("\n2️⃣ 경제 지표 수집 테스트")
        economic_result = await server.fetch_economic_indicators(country="KR")
        print(f"✅ 경제 지표: {economic_result['status']}")
        if economic_result['status'] == 'success':
            print(f"📈 수집된 지표: {list(economic_result['data'].keys())}")
        
        # 3. 연금 정보 수집 테스트
        print("\n3️⃣ 연금 정보 수집 테스트")
        pension_result = await server.fetch_pension_info(country="KR")
        print(f"✅ 연금 정보: {pension_result['status']}")
        if pension_result['status'] == 'success':
            print(f"🏦 연금 제도: {list(pension_result['data'].keys())}")
        
        # 4. 금리 정보 수집 테스트
        print("\n4️⃣ 금리 정보 수집 테스트")
        interest_result = await server.fetch_interest_rates(country="KR")
        print(f"✅ 금리 정보: {interest_result['status']}")
        if interest_result['status'] == 'success':
            print(f"💰 수집된 금리: {list(interest_result['data'].keys())}")
        
        # 5. 주식 데이터 수집 테스트
        print("\n5️⃣ 주식 데이터 수집 테스트")
        stock_result = await server.fetch_stock_data(
            symbols=["AAPL", "MSFT", "GOOGL"],
            period="1mo"
        )
        print(f"✅ 주식 데이터: {stock_result['status']}")
        if stock_result['status'] == 'success':
            print(f"📈 수집된 주식: {list(stock_result['data'].keys())}")
        
        # 6. 채권 데이터 수집 테스트
        print("\n6️⃣ 채권 데이터 수집 테스트")
        bond_result = await server.fetch_bond_data(country="US")
        print(f"✅ 채권 데이터: {bond_result['status']}")
        if bond_result['status'] == 'success':
            print(f"📊 수집된 채권: {list(bond_result['data'].keys())}")
        
        # 7. 환율 정보 수집 테스트
        print("\n7️⃣ 환율 정보 수집 테스트")
        currency_result = await server.fetch_currency_rates(base_currency="USD")
        print(f"✅ 환율 정보: {currency_result['status']}")
        if currency_result['status'] == 'success':
            print(f"💱 수집된 환율: {list(currency_result['data'].keys())}")
        
        # 8. 인플레이션 데이터 수집 테스트
        print("\n8️⃣ 인플레이션 데이터 수집 테스트")
        inflation_result = await server.fetch_inflation_data(country="US")
        print(f"✅ 인플레이션: {inflation_result['status']}")
        if inflation_result['status'] == 'success':
            print(f"📊 수집된 인플레이션: {list(inflation_result['data'].keys())}")
        
        print("\n🎉 외부 API 서버 테스트 완료!")
        
    except Exception as e:
        print(f"❌ 테스트 실패: {str(e)}")
    
    finally:
        await server.stop()

if __name__ == "__main__":
    asyncio.run(test_external_api())
