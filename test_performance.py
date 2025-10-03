#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
성능 최적화 테스트
"""

import asyncio
import time
import random
from typing import List, Dict, Any
from src.utils.cache_manager import cache_manager, cached
from src.utils.performance_monitor import performance_monitor, track_performance
from src.utils.async_worker import thread_pool, data_processor

async def test_cache_performance():
    """캐시 성능 테스트"""
    print("🔧 캐시 성능 테스트 시작")
    
    # 캐시 키 생성
    cache_key = "test_calculation_100"
    
    # 첫 번째 실행 (캐시 없음)
    start_time = time.time()
    result1 = await cache_manager.get(cache_key)
    if result1 is None:
        # 계산 수행
        await asyncio.sleep(0.1)  # 시뮬레이션
        result1 = 100 * 100 * 100
        await cache_manager.set(cache_key, result1, ttl=60)
    first_duration = time.time() - start_time
    
    # 두 번째 실행 (캐시 있음)
    start_time = time.time()
    result2 = await cache_manager.get(cache_key)
    second_duration = time.time() - start_time
    
    print(f"✅ 첫 번째 실행: {first_duration:.3f}초")
    print(f"✅ 두 번째 실행: {second_duration:.3f}초")
    if second_duration > 0:
        print(f"🚀 캐시 효과: {first_duration/second_duration:.1f}배 빨라짐")
    else:
        print(f"🚀 캐시 효과: 즉시 반환 (매우 빠름)")
    
    # 캐시 통계
    stats = cache_manager.get_cache_stats()
    print(f"📊 캐시 통계: {stats}")

async def test_performance_monitoring():
    """성능 모니터링 테스트"""
    print("\n📊 성능 모니터링 테스트 시작")
    
    # 모니터링 시작
    performance_monitor.start_monitoring(interval=1.0)
    
    @track_performance("test_endpoint")
    async def test_endpoint(user_id: str = "test_user"):
        """테스트 엔드포인트"""
        await asyncio.sleep(0.1)
        return {"status": "success", "user_id": user_id}
    
    # 여러 요청 실행
    for i in range(5):
        await test_endpoint(f"user_{i}")
        await asyncio.sleep(0.1)
    
    # 성능 요약 조회
    await asyncio.sleep(2)  # 모니터링 데이터 수집 대기
    
    summary = performance_monitor.get_performance_summary(hours=1)
    print(f"✅ 성능 요약: {summary}")
    
    # 엔드포인트별 성능
    endpoint_perf = performance_monitor.get_endpoint_performance("test_endpoint")
    print(f"📈 엔드포인트 성능: {endpoint_perf}")
    
    # 모니터링 중지
    performance_monitor.stop_monitoring()

async def test_async_worker_pool():
    """비동기 워커 풀 테스트"""
    print("\n⚡ 비동기 워커 풀 테스트 시작")
    
    def cpu_intensive_task(data: List[int]) -> int:
        """CPU 집약적 작업"""
        result = 0
        for i in data:
            result += i ** 2
        return result
    
    # 테스트 데이터 생성
    test_data = [list(range(1000)) for _ in range(10)]
    
    # 순차 처리
    start_time = time.time()
    sequential_results = []
    for data in test_data:
        result = cpu_intensive_task(data)
        sequential_results.append(result)
    sequential_duration = time.time() - start_time
    
    # 병렬 처리
    start_time = time.time()
    parallel_results = await thread_pool.map_async(
        cpu_intensive_task,
        test_data
    )
    parallel_duration = time.time() - start_time
    
    print(f"✅ 순차 처리: {sequential_duration:.3f}초")
    print(f"✅ 병렬 처리: {parallel_duration:.3f}초")
    print(f"🚀 병렬화 효과: {sequential_duration/parallel_duration:.1f}배 빨라짐")
    
    # 워커 풀 통계
    stats = thread_pool.get_pool_stats()
    print(f"📊 워커 풀 통계: {stats}")

async def test_data_processing():
    """데이터 처리 성능 테스트"""
    print("\n📊 데이터 처리 성능 테스트 시작")
    
    # 금융 데이터 생성
    financial_data = []
    for i in range(100):
        data = {
            'symbol': f'STOCK_{i}',
            'price': random.uniform(50, 200),
            'volume': random.randint(1000, 10000),
            'returns': [random.uniform(-0.1, 0.1) for _ in range(30)]
        }
        financial_data.append(data)
    
    def process_financial_chunk(chunk: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """금융 데이터 청크 처리"""
        processed = []
        for data in chunk:
            # 간단한 처리 로직
            processed_data = {
                **data,
                'processed': True,
                'avg_return': sum(data['returns']) / len(data['returns']),
                'volatility': sum(abs(r) for r in data['returns']) / len(data['returns'])
            }
            processed.append(processed_data)
        return processed
    
    # 데이터 처리
    start_time = time.time()
    processed_data = await data_processor.process_financial_data(
        financial_data,
        process_financial_chunk
    )
    processing_duration = time.time() - start_time
    
    print(f"✅ 처리된 데이터: {len(processed_data)}개")
    print(f"⏱️ 처리 시간: {processing_duration:.3f}초")
    print(f"📈 처리 속도: {len(processed_data)/processing_duration:.1f}개/초")

async def test_portfolio_optimization():
    """포트폴리오 최적화 테스트"""
    print("\n💼 포트폴리오 최적화 테스트 시작")
    
    # 포트폴리오 데이터 생성
    portfolios = []
    for i in range(50):
        portfolio = {
            'portfolio_id': f'portfolio_{i}',
            'stocks': random.uniform(20, 80),
            'bonds': random.uniform(10, 60),
            'cash': random.uniform(5, 30),
            'returns': [random.uniform(-0.05, 0.05) for _ in range(252)]  # 1년 데이터
        }
        portfolios.append(portfolio)
    
    # 포트폴리오 메트릭 계산
    start_time = time.time()
    optimized_portfolios = await data_processor.calculate_portfolio_metrics(portfolios)
    optimization_duration = time.time() - start_time
    
    # 결과 분석
    best_portfolio = max(optimized_portfolios, key=lambda x: x.get('sharpe_ratio', 0))
    
    print(f"✅ 최적화된 포트폴리오: {len(optimized_portfolios)}개")
    print(f"⏱️ 최적화 시간: {optimization_duration:.3f}초")
    print(f"🏆 최고 샤프 비율: {best_portfolio.get('sharpe_ratio', 0):.3f}")
    print(f"📊 최고 포트폴리오: 주식 {best_portfolio.get('stocks', 0):.1f}%, "
          f"채권 {best_portfolio.get('bonds', 0):.1f}%, "
          f"현금 {best_portfolio.get('cash', 0):.1f}%")

async def main():
    """메인 테스트 함수"""
    print("🚀 성능 최적화 테스트 시작")
    print("=" * 50)
    
    try:
        # 캐시 성능 테스트
        await test_cache_performance()
        
        # 성능 모니터링 테스트
        await test_performance_monitoring()
        
        # 비동기 워커 풀 테스트
        await test_async_worker_pool()
        
        # 데이터 처리 테스트
        await test_data_processing()
        
        # 포트폴리오 최적화 테스트
        await test_portfolio_optimization()
        
        print("\n🎉 성능 최적화 테스트 완료!")
        
    except Exception as e:
        print(f"❌ 테스트 실패: {str(e)}")
    
    finally:
        # 리소스 정리
        thread_pool.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
