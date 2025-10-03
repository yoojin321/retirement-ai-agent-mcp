#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
비동기 워커 풀 - 대용량 데이터 처리 최적화
"""

import asyncio
import time
from typing import Dict, Any, List, Optional, Callable, Union
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from dataclasses import dataclass
from enum import Enum
import multiprocessing

class WorkerType(Enum):
    """워커 타입"""
    THREAD = "thread"
    PROCESS = "process"
    ASYNC = "async"

@dataclass
class Task:
    """작업 정보"""
    task_id: str
    func: Callable
    args: tuple
    kwargs: dict
    priority: int = 0
    created_at: float = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()

class AsyncWorkerPool:
    """비동기 워커 풀"""
    
    def __init__(self, 
                 max_workers: int = None,
                 worker_type: WorkerType = WorkerType.THREAD):
        """
        비동기 워커 풀 초기화
        
        Args:
            max_workers: 최대 워커 수
            worker_type: 워커 타입
        """
        self.max_workers = max_workers or multiprocessing.cpu_count()
        self.worker_type = worker_type
        self.executor = None
        self.tasks = {}
        self.results = {}
        self.is_running = False
        
        self._initialize_executor()
    
    def _initialize_executor(self):
        """실행자 초기화"""
        if self.worker_type == WorkerType.THREAD:
            self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
        elif self.worker_type == WorkerType.PROCESS:
            self.executor = ProcessPoolExecutor(max_workers=self.max_workers)
    
    async def submit_task(self, 
                         task_id: str,
                         func: Callable,
                         *args,
                         priority: int = 0,
                         **kwargs) -> Any:
        """작업 제출"""
        task = Task(
            task_id=task_id,
            func=func,
            args=args,
            kwargs=kwargs,
            priority=priority
        )
        
        self.tasks[task_id] = task
        
        if self.worker_type == WorkerType.ASYNC:
            # 비동기 함수 직접 실행
            result = await func(*args, **kwargs)
            self.results[task_id] = result
            return result
        else:
            # 스레드/프로세스 풀에서 실행
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor,
                func,
                *args,
                **kwargs
            )
            self.results[task_id] = result
            return result
    
    async def submit_batch(self, 
                          tasks: List[Task],
                          max_concurrent: int = None) -> Dict[str, Any]:
        """배치 작업 제출"""
        max_concurrent = max_concurrent or self.max_workers
        
        # 우선순위별로 정렬
        sorted_tasks = sorted(tasks, key=lambda x: x.priority, reverse=True)
        
        # 동시 실행 제한
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def execute_task(task: Task):
            async with semaphore:
                return await self.submit_task(
                    task.task_id,
                    task.func,
                    *task.args,
                    priority=task.priority,
                    **task.kwargs
                )
        
        # 모든 작업 병렬 실행
        results = await asyncio.gather(
            *[execute_task(task) for task in sorted_tasks],
            return_exceptions=True
        )
        
        # 결과 매핑
        batch_results = {}
        for i, task in enumerate(sorted_tasks):
            if isinstance(results[i], Exception):
                batch_results[task.task_id] = {
                    'error': str(results[i]),
                    'success': False
                }
            else:
                batch_results[task.task_id] = {
                    'result': results[i],
                    'success': True
                }
        
        return batch_results
    
    async def map_async(self, 
                       func: Callable,
                       iterable: List[Any],
                       max_concurrent: int = None) -> List[Any]:
        """비동기 맵핑"""
        max_concurrent = max_concurrent or self.max_workers
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def process_item(item):
            async with semaphore:
                if self.worker_type == WorkerType.ASYNC:
                    return await func(item)
                else:
                    loop = asyncio.get_event_loop()
                    return await loop.run_in_executor(self.executor, func, item)
        
        return await asyncio.gather(*[process_item(item) for item in iterable])
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """작업 상태 조회"""
        if task_id not in self.tasks:
            return {'status': 'not_found'}
        
        task = self.tasks[task_id]
        
        if task_id in self.results:
            return {
                'status': 'completed',
                'result': self.results[task_id],
                'duration': time.time() - task.created_at
            }
        else:
            return {
                'status': 'running',
                'duration': time.time() - task.created_at
            }
    
    def get_pool_stats(self) -> Dict[str, Any]:
        """풀 통계 조회"""
        return {
            'max_workers': self.max_workers,
            'worker_type': self.worker_type.value,
            'active_tasks': len(self.tasks) - len(self.results),
            'completed_tasks': len(self.results),
            'total_tasks': len(self.tasks)
        }
    
    def cleanup(self):
        """리소스 정리"""
        if self.executor:
            self.executor.shutdown(wait=True)

class DataProcessor:
    """대용량 데이터 처리기"""
    
    def __init__(self, worker_pool: AsyncWorkerPool):
        self.worker_pool = worker_pool
    
    async def process_financial_data(self, 
                                   data_list: List[Dict[str, Any]],
                                   processing_func: Callable) -> List[Dict[str, Any]]:
        """금융 데이터 처리"""
        # 데이터를 청크로 분할
        chunk_size = max(1, len(data_list) // self.worker_pool.max_workers)
        chunks = [data_list[i:i + chunk_size] for i in range(0, len(data_list), chunk_size)]
        
        # 각 청크를 병렬 처리
        processed_chunks = await self.worker_pool.map_async(
            processing_func,
            chunks
        )
        
        # 결과 병합
        result = []
        for chunk in processed_chunks:
            result.extend(chunk)
        
        return result
    
    async def calculate_portfolio_metrics(self, 
                                        portfolios: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """포트폴리오 메트릭 계산"""
        def calculate_metrics(portfolio):
            # 샤프 비율, 변동성, 수익률 계산
            returns = portfolio.get('returns', [])
            if not returns:
                return {**portfolio, 'sharpe_ratio': 0, 'volatility': 0, 'return': 0}
            
            import numpy as np
            
            mean_return = np.mean(returns)
            volatility = np.std(returns)
            sharpe_ratio = mean_return / volatility if volatility > 0 else 0
            
            return {
                **portfolio,
                'sharpe_ratio': sharpe_ratio,
                'volatility': volatility,
                'return': mean_return
            }
        
        return await self.worker_pool.map_async(
            calculate_metrics,
            portfolios
        )
    
    async def optimize_asset_allocation(self, 
                                      scenarios: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """자산 배분 최적화"""
        def optimize_scenario(scenario):
            # 시나리오별 최적 자산 배분 계산
            risk_tolerance = scenario.get('risk_tolerance', 0.5)
            time_horizon = scenario.get('time_horizon', 10)
            
            # 간단한 최적화 로직 (실제로는 더 복잡한 알고리즘 사용)
            if risk_tolerance < 0.3:
                return {**scenario, 'stocks': 20, 'bonds': 60, 'cash': 20}
            elif risk_tolerance < 0.7:
                return {**scenario, 'stocks': 40, 'bonds': 40, 'cash': 20}
            else:
                return {**scenario, 'stocks': 60, 'bonds': 30, 'cash': 10}
        
        return await self.worker_pool.map_async(
            optimize_scenario,
            scenarios
        )

# 전역 워커 풀 인스턴스들
thread_pool = AsyncWorkerPool(worker_type=WorkerType.THREAD)
process_pool = AsyncWorkerPool(worker_type=WorkerType.PROCESS)
async_pool = AsyncWorkerPool(worker_type=WorkerType.ASYNC)

# 데이터 프로세서
data_processor = DataProcessor(thread_pool)
