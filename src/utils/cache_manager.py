#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
캐시 관리자 - 성능 최적화를 위한 캐싱 시스템
"""

import asyncio
import json
import hashlib
import time
from typing import Dict, Any, Optional, Callable
from datetime import datetime, timedelta
import redis
import pickle

class CacheManager:
    """캐시 관리자"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379", default_ttl: int = 3600):
        """
        캐시 관리자 초기화
        
        Args:
            redis_url: Redis 서버 URL
            default_ttl: 기본 TTL (초)
        """
        self.redis_url = redis_url
        self.default_ttl = default_ttl
        self.redis_client = None
        self.local_cache = {}  # 로컬 메모리 캐시
        self._initialize_redis()
    
    def _initialize_redis(self):
        """Redis 클라이언트 초기화"""
        try:
            self.redis_client = redis.from_url(self.redis_url, decode_responses=False)
            # 연결 테스트
            self.redis_client.ping()
        except Exception as e:
            print(f"Redis 연결 실패, 로컬 캐시만 사용: {e}")
            self.redis_client = None
    
    def _generate_cache_key(self, prefix: str, *args, **kwargs) -> str:
        """캐시 키 생성"""
        key_data = {
            "prefix": prefix,
            "args": args,
            "kwargs": sorted(kwargs.items())
        }
        key_string = json.dumps(key_data, sort_keys=True)
        return f"{prefix}:{hashlib.md5(key_string.encode()).hexdigest()}"
    
    async def get(self, key: str) -> Optional[Any]:
        """캐시에서 데이터 조회"""
        # 1. 로컬 캐시 확인
        if key in self.local_cache:
            cached_item = self.local_cache[key]
            if cached_item['expires_at'] > time.time():
                return cached_item['data']
            else:
                del self.local_cache[key]
        
        # 2. Redis 캐시 확인
        if self.redis_client:
            try:
                cached_data = self.redis_client.get(key)
                if cached_data:
                    return pickle.loads(cached_data)
            except Exception as e:
                print(f"Redis 조회 실패: {e}")
        
        return None
    
    async def set(self, key: str, data: Any, ttl: Optional[int] = None) -> bool:
        """캐시에 데이터 저장"""
        ttl = ttl or self.default_ttl
        
        # 1. 로컬 캐시 저장
        self.local_cache[key] = {
            'data': data,
            'expires_at': time.time() + ttl
        }
        
        # 2. Redis 캐시 저장
        if self.redis_client:
            try:
                serialized_data = pickle.dumps(data)
                self.redis_client.setex(key, ttl, serialized_data)
            except Exception as e:
                print(f"Redis 저장 실패: {e}")
        
        return True
    
    async def delete(self, key: str) -> bool:
        """캐시에서 데이터 삭제"""
        # 로컬 캐시에서 삭제
        if key in self.local_cache:
            del self.local_cache[key]
        
        # Redis 캐시에서 삭제
        if self.redis_client:
            try:
                self.redis_client.delete(key)
            except Exception as e:
                print(f"Redis 삭제 실패: {e}")
        
        return True
    
    async def clear_pattern(self, pattern: str) -> int:
        """패턴에 맞는 캐시 삭제"""
        deleted_count = 0
        
        # 로컬 캐시에서 삭제
        keys_to_delete = [key for key in self.local_cache.keys() if pattern in key]
        for key in keys_to_delete:
            del self.local_cache[key]
            deleted_count += 1
        
        # Redis 캐시에서 삭제
        if self.redis_client:
            try:
                keys = self.redis_client.keys(pattern)
                if keys:
                    self.redis_client.delete(*keys)
                    deleted_count += len(keys)
            except Exception as e:
                print(f"Redis 패턴 삭제 실패: {e}")
        
        return deleted_count
    
    async def cached_function(self, 
                            prefix: str, 
                            ttl: Optional[int] = None,
                            key_func: Optional[Callable] = None):
        """함수 캐싱 데코레이터"""
        def decorator(func):
            async def wrapper(*args, **kwargs):
                # 캐시 키 생성
                if key_func:
                    cache_key = key_func(*args, **kwargs)
                else:
                    cache_key = self._generate_cache_key(prefix, *args, **kwargs)
                
                # 캐시에서 조회
                cached_result = await self.get(cache_key)
                if cached_result is not None:
                    return cached_result
                
                # 함수 실행
                result = await func(*args, **kwargs)
                
                # 결과 캐싱
                await self.set(cache_key, result, ttl)
                
                return result
            
            return wrapper
        return decorator
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """캐시 통계 조회"""
        stats = {
            "local_cache_size": len(self.local_cache),
            "redis_connected": self.redis_client is not None,
            "local_cache_keys": list(self.local_cache.keys())
        }
        
        if self.redis_client:
            try:
                stats["redis_info"] = self.redis_client.info()
            except Exception as e:
                stats["redis_error"] = str(e)
        
        return stats

# 전역 캐시 관리자 인스턴스
cache_manager = CacheManager()

# 캐시 데코레이터
def cached(prefix: str, ttl: Optional[int] = None, key_func: Optional[Callable] = None):
    """캐시 데코레이터"""
    return cache_manager.cached_function(prefix, ttl, key_func)
