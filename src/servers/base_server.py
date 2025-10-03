#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP 서버 기본 클래스
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class BaseMCPServer(ABC):
    """MCP 서버 기본 클래스"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"{__name__}.{name}")
        self.is_running = False
        self.tools = {}
        self.setup_tools()
    
    @abstractmethod
    def setup_tools(self):
        """서버별 도구 설정 (하위 클래스에서 구현)"""
        pass
    
    @abstractmethod
    async def start(self):
        """서버 시작 (하위 클래스에서 구현)"""
        pass
    
    @abstractmethod
    async def stop(self):
        """서버 중지 (하위 클래스에서 구현)"""
        pass
    
    def register_tool(self, name: str, tool_func, description: str = ""):
        """도구 등록"""
        self.tools[name] = {
            'function': tool_func,
            'description': description
        }
        self.logger.info(f"도구 '{name}'이 등록되었습니다.")
    
    async def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """도구 실행"""
        if tool_name not in self.tools:
            raise ValueError(f"도구 '{tool_name}'을 찾을 수 없습니다.")
        
        try:
            self.logger.info(f"도구 '{tool_name}' 실행 중...")
            result = await self.tools[tool_name]['function'](**kwargs)
            self.logger.info(f"도구 '{tool_name}' 실행 완료")
            return result
            
        except Exception as e:
            self.logger.error(f"도구 '{tool_name}' 실행 중 오류: {e}")
            raise
    
    def get_available_tools(self) -> List[Dict[str, str]]:
        """사용 가능한 도구 목록 반환"""
        return [
            {
                'name': name,
                'description': tool['description']
            }
            for name, tool in self.tools.items()
        ]
