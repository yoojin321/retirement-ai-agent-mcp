#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
성능 모니터링 - 시스템 성능 추적 및 최적화
"""

import time
import asyncio
import psutil
import threading
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict, deque
import json

class PerformanceMonitor:
    """성능 모니터링 클래스"""
    
    def __init__(self, max_history: int = 1000):
        """
        성능 모니터 초기화
        
        Args:
            max_history: 최대 히스토리 저장 개수
        """
        self.max_history = max_history
        self.metrics = defaultdict(lambda: deque(maxlen=max_history))
        self.active_requests = {}
        self.system_metrics = {}
        self.is_monitoring = False
        self.monitor_thread = None
    
    def start_monitoring(self, interval: float = 5.0):
        """성능 모니터링 시작"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(interval,),
            daemon=True
        )
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """성능 모니터링 중지"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
    
    def _monitor_loop(self, interval: float):
        """모니터링 루프"""
        while self.is_monitoring:
            try:
                self._collect_system_metrics()
                time.sleep(interval)
            except Exception as e:
                print(f"모니터링 오류: {e}")
    
    def _collect_system_metrics(self):
        """시스템 메트릭 수집"""
        try:
            # CPU 사용률
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # 메모리 사용률
            memory = psutil.virtual_memory()
            
            # 디스크 사용률
            disk = psutil.disk_usage('/')
            
            # 네트워크 I/O
            network = psutil.net_io_counters()
            
            # 프로세스 정보
            process = psutil.Process()
            
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'cpu_percent': cpu_percent,
                'memory': {
                    'total': memory.total,
                    'available': memory.available,
                    'percent': memory.percent,
                    'used': memory.used,
                    'free': memory.free
                },
                'disk': {
                    'total': disk.total,
                    'used': disk.used,
                    'free': disk.free,
                    'percent': (disk.used / disk.total) * 100
                },
                'network': {
                    'bytes_sent': network.bytes_sent,
                    'bytes_recv': network.bytes_recv,
                    'packets_sent': network.packets_sent,
                    'packets_recv': network.packets_recv
                },
                'process': {
                    'pid': process.pid,
                    'cpu_percent': process.cpu_percent(),
                    'memory_info': process.memory_info()._asdict(),
                    'num_threads': process.num_threads(),
                    'create_time': process.create_time()
                }
            }
            
            self.system_metrics = metrics
            self.metrics['system'].append(metrics)
            
        except Exception as e:
            print(f"시스템 메트릭 수집 오류: {e}")
    
    def start_request_tracking(self, request_id: str, endpoint: str, user_id: Optional[str] = None):
        """요청 추적 시작"""
        self.active_requests[request_id] = {
            'endpoint': endpoint,
            'user_id': user_id,
            'start_time': time.time(),
            'start_datetime': datetime.now().isoformat()
        }
    
    def end_request_tracking(self, request_id: str, status: str = "success", error: Optional[str] = None):
        """요청 추적 종료"""
        if request_id not in self.active_requests:
            return
        
        request_info = self.active_requests[request_id]
        end_time = time.time()
        duration = end_time - request_info['start_time']
        
        # 요청 메트릭 저장
        request_metric = {
            'request_id': request_id,
            'endpoint': request_info['endpoint'],
            'user_id': request_info['user_id'],
            'start_time': request_info['start_datetime'],
            'end_time': datetime.now().isoformat(),
            'duration': duration,
            'status': status,
            'error': error
        }
        
        self.metrics['requests'].append(request_metric)
        
        # 활성 요청에서 제거
        del self.active_requests[request_id]
    
    def record_metric(self, metric_name: str, value: float, tags: Optional[Dict[str, str]] = None):
        """메트릭 기록"""
        metric_data = {
            'timestamp': datetime.now().isoformat(),
            'value': value,
            'tags': tags or {}
        }
        
        self.metrics[metric_name].append(metric_data)
    
    def get_performance_summary(self, hours: int = 1) -> Dict[str, Any]:
        """성능 요약 조회"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        # 요청 통계
        recent_requests = [
            req for req in self.metrics['requests']
            if datetime.fromisoformat(req['end_time']) > cutoff_time
        ]
        
        if recent_requests:
            durations = [req['duration'] for req in recent_requests]
            success_count = len([req for req in recent_requests if req['status'] == 'success'])
            
            request_stats = {
                'total_requests': len(recent_requests),
                'success_rate': (success_count / len(recent_requests)) * 100,
                'avg_duration': sum(durations) / len(durations),
                'min_duration': min(durations),
                'max_duration': max(durations),
                'p95_duration': sorted(durations)[int(len(durations) * 0.95)] if durations else 0
            }
        else:
            request_stats = {
                'total_requests': 0,
                'success_rate': 0,
                'avg_duration': 0,
                'min_duration': 0,
                'max_duration': 0,
                'p95_duration': 0
            }
        
        # 시스템 통계
        recent_system = [
            sys for sys in self.metrics['system']
            if datetime.fromisoformat(sys['timestamp']) > cutoff_time
        ]
        
        if recent_system:
            cpu_values = [sys['cpu_percent'] for sys in recent_system]
            memory_values = [sys['memory']['percent'] for sys in recent_system]
            
            system_stats = {
                'avg_cpu': sum(cpu_values) / len(cpu_values),
                'max_cpu': max(cpu_values),
                'avg_memory': sum(memory_values) / len(memory_values),
                'max_memory': max(memory_values)
            }
        else:
            system_stats = {
                'avg_cpu': 0,
                'max_cpu': 0,
                'avg_memory': 0,
                'max_memory': 0
            }
        
        return {
            'period_hours': hours,
            'request_stats': request_stats,
            'system_stats': system_stats,
            'active_requests': len(self.active_requests),
            'current_system': self.system_metrics
        }
    
    def get_endpoint_performance(self, endpoint: str, hours: int = 1) -> Dict[str, Any]:
        """특정 엔드포인트 성능 조회"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        endpoint_requests = [
            req for req in self.metrics['requests']
            if req['endpoint'] == endpoint and 
            datetime.fromisoformat(req['end_time']) > cutoff_time
        ]
        
        if not endpoint_requests:
            return {
                'endpoint': endpoint,
                'total_requests': 0,
                'avg_duration': 0,
                'success_rate': 0
            }
        
        durations = [req['duration'] for req in endpoint_requests]
        success_count = len([req for req in endpoint_requests if req['status'] == 'success'])
        
        return {
            'endpoint': endpoint,
            'total_requests': len(endpoint_requests),
            'avg_duration': sum(durations) / len(durations),
            'min_duration': min(durations),
            'max_duration': max(durations),
            'success_rate': (success_count / len(endpoint_requests)) * 100,
            'recent_requests': endpoint_requests[-10:]  # 최근 10개 요청
        }
    
    def get_slow_requests(self, threshold: float = 1.0, hours: int = 1) -> List[Dict[str, Any]]:
        """느린 요청 조회"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        slow_requests = [
            req for req in self.metrics['requests']
            if req['duration'] > threshold and 
            datetime.fromisoformat(req['end_time']) > cutoff_time
        ]
        
        return sorted(slow_requests, key=lambda x: x['duration'], reverse=True)
    
    def export_metrics(self, filepath: str):
        """메트릭 데이터 내보내기"""
        export_data = {
            'export_time': datetime.now().isoformat(),
            'metrics': dict(self.metrics),
            'active_requests': self.active_requests,
            'system_metrics': self.system_metrics
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

# 전역 성능 모니터 인스턴스
performance_monitor = PerformanceMonitor()

# 성능 추적 데코레이터
def track_performance(endpoint: str):
    """성능 추적 데코레이터"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            request_id = f"{endpoint}_{int(time.time() * 1000)}"
            
            # 요청 추적 시작
            performance_monitor.start_request_tracking(
                request_id=request_id,
                endpoint=endpoint,
                user_id=kwargs.get('user_id')
            )
            
            try:
                result = await func(*args, **kwargs)
                performance_monitor.end_request_tracking(request_id, "success")
                return result
            except Exception as e:
                performance_monitor.end_request_tracking(request_id, "error", str(e))
                raise
        
        return wrapper
    return decorator
