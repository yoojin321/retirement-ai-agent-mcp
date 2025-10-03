#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
인출메이트 MCP 서버 - 은퇴 후 절세 인출 서비스
"""

from typing import Dict, Any
from .base_server import BaseMCPServer
from src.tools.withdrawal_tools import WithdrawalTools

class WithdrawalServer(BaseMCPServer):
    """인출메이트 MCP 서버"""
    
    def __init__(self):
        super().__init__("WithdrawalServer")
        self.tools_handler = WithdrawalTools()
    
    def setup_tools(self):
        """인출메이트 도구들 설정"""
        
        # 분석 도구들
        self.register_tool(
            "analyze_retirement_assets",
            self.analyze_retirement_assets,
            "은퇴 자산 구조 분석"
        )
        
        self.register_tool(
            "set_withdrawal_baseline",
            self.set_withdrawal_baseline,
            "인출 기본선 설정"
        )
        
        self.register_tool(
            "manage_guardrail_system",
            self.manage_guardrail_system,
            "가드레일 시스템 관리"
        )
        
        # 최적화 도구들
        self.register_tool(
            "optimize_withdrawal_sequence",
            self.optimize_withdrawal_sequence,
            "인출 순서 최적화"
        )
        
        self.register_tool(
            "manage_bucket_strategy",
            self.manage_bucket_strategy,
            "3버킷 전략 관리"
        )
        
        self.register_tool(
            "create_execution_plan",
            self.create_execution_plan,
            "실행 계획 생성"
        )
        
        self.register_tool(
            "compare_scenarios",
            self.compare_scenarios,
            "시나리오 비교"
        )
    
    async def start(self):
        """서버 시작"""
        self.is_running = True
        self.logger.info("인출메이트 서버가 시작되었습니다.")
    
    async def stop(self):
        """서버 중지"""
        self.is_running = False
        self.logger.info("인출메이트 서버가 중지되었습니다.")
    
    # 도구 구현 메서드들
    async def analyze_retirement_assets(self, **kwargs) -> Dict[str, Any]:
        """은퇴 자산 구조 분석"""
        return await self.tools_handler.analyze_retirement_assets(**kwargs)
    
    async def set_withdrawal_baseline(self, **kwargs) -> Dict[str, Any]:
        """인출 기본선 설정"""
        return await self.tools_handler.set_withdrawal_baseline(**kwargs)
    
    async def manage_guardrail_system(self, **kwargs) -> Dict[str, Any]:
        """가드레일 시스템 관리"""
        return await self.tools_handler.manage_guardrail_system(**kwargs)
    
    async def optimize_withdrawal_sequence(self, **kwargs) -> Dict[str, Any]:
        """인출 순서 최적화"""
        return await self.tools_handler.optimize_withdrawal_sequence(**kwargs)
    
    async def manage_bucket_strategy(self, **kwargs) -> Dict[str, Any]:
        """3버킷 전략 관리"""
        return await self.tools_handler.manage_bucket_strategy(**kwargs)
    
    async def create_execution_plan(self, **kwargs) -> Dict[str, Any]:
        """실행 계획 생성"""
        return await self.tools_handler.create_execution_plan(**kwargs)
    
    async def compare_scenarios(self, **kwargs) -> Dict[str, Any]:
        """시나리오 비교"""
        return await self.tools_handler.compare_scenarios(**kwargs)
