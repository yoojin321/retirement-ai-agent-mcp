#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
투자메이트 MCP 서버 - 은퇴 자산 투자 서비스
"""

from typing import Dict, Any
from .base_server import BaseMCPServer
from src.tools.investment_tools import InvestmentTools

class InvestmentServer(BaseMCPServer):
    """투자메이트 MCP 서버"""
    
    def __init__(self):
        super().__init__("InvestmentServer")
        self.tools_handler = InvestmentTools()
    
    def setup_tools(self):
        """투자메이트 도구들 설정"""
        
        # 분석 도구들
        self.register_tool(
            "assess_risk_profile",
            self.assess_risk_profile,
            "리스크 프로파일 평가"
        )
        
        self.register_tool(
            "analyze_market_volatility",
            self.analyze_market_volatility,
            "시장 변동성 분석"
        )
        
        self.register_tool(
            "optimize_account_utilization",
            self.optimize_account_utilization,
            "계좌 활용 최적화"
        )
        
        # 포트폴리오 도구들
        self.register_tool(
            "generate_portfolio_options",
            self.generate_portfolio_options,
            "포트폴리오 옵션 생성"
        )
        
        self.register_tool(
            "adjust_for_volatility",
            self.adjust_for_volatility,
            "변동성 조정"
        )
        
        self.register_tool(
            "create_implementation_plan",
            self.create_implementation_plan,
            "실행 계획 수립"
        )
        
        self.register_tool(
            "monitor_performance",
            self.monitor_performance,
            "성과 모니터링"
        )
    
    async def start(self):
        """서버 시작"""
        self.is_running = True
        self.logger.info("투자메이트 서버가 시작되었습니다.")
    
    async def stop(self):
        """서버 중지"""
        self.is_running = False
        self.logger.info("투자메이트 서버가 중지되었습니다.")
    
    # 도구 구현 메서드들
    async def assess_risk_profile(self, **kwargs) -> Dict[str, Any]:
        """리스크 프로파일 평가"""
        return await self.tools_handler.assess_risk_profile(**kwargs)
    
    async def analyze_market_volatility(self, **kwargs) -> Dict[str, Any]:
        """시장 변동성 분석"""
        return await self.tools_handler.analyze_market_volatility(**kwargs)
    
    async def optimize_account_utilization(self, **kwargs) -> Dict[str, Any]:
        """계좌 활용 최적화"""
        return await self.tools_handler.optimize_account_utilization(**kwargs)
    
    async def generate_portfolio_options(self, **kwargs) -> Dict[str, Any]:
        """포트폴리오 옵션 생성"""
        return await self.tools_handler.generate_portfolio_options(**kwargs)
    
    async def adjust_for_volatility(self, **kwargs) -> Dict[str, Any]:
        """변동성 조정"""
        return await self.tools_handler.adjust_for_volatility(**kwargs)
    
    async def create_implementation_plan(self, **kwargs) -> Dict[str, Any]:
        """실행 계획 수립"""
        return await self.tools_handler.create_implementation_plan(**kwargs)
    
    async def monitor_performance(self, **kwargs) -> Dict[str, Any]:
        """성과 모니터링"""
        return await self.tools_handler.monitor_performance(**kwargs)
