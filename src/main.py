#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
은퇴 설계 AI 에이전트 MCP 서버 메인 엔트리포인트
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.servers.accumulation_server import AccumulationServer
from src.servers.investment_server import InvestmentServer
from src.servers.withdrawal_server import WithdrawalServer
from src.servers.data_server import DataServer
from src.servers.external_api_server import ExternalAPIServer
from src.utils.logger import setup_logger

# 로거 설정
logger = setup_logger(__name__)

class RetirementAIAgentServer:
    """은퇴 설계 AI 에이전트 메인 MCP 서버"""
    
    def __init__(self):
        self.servers = {}
        self.setup_servers()
    
    def setup_servers(self):
        """모든 MCP 서버 초기화"""
        try:
            # 각 서비스별 MCP 서버 생성
            self.servers['accumulation'] = AccumulationServer()
            self.servers['investment'] = InvestmentServer()
            self.servers['withdrawal'] = WithdrawalServer()
            self.servers['data'] = DataServer()
            self.servers['external_api'] = ExternalAPIServer()
            
            logger.info("모든 MCP 서버가 성공적으로 초기화되었습니다.")
            
        except Exception as e:
            logger.error(f"MCP 서버 초기화 중 오류 발생: {e}")
            raise
    
    async def start(self):
        """모든 서버 시작"""
        try:
            # 모든 서버를 병렬로 시작
            tasks = []
            for name, server in self.servers.items():
                task = asyncio.create_task(server.start(), name=f"server_{name}")
                tasks.append(task)
                logger.info(f"{name} 서버 시작 중...")
            
            # 모든 서버가 시작될 때까지 대기
            await asyncio.gather(*tasks)
            logger.info("모든 MCP 서버가 성공적으로 시작되었습니다.")
            
        except Exception as e:
            logger.error(f"서버 시작 중 오류 발생: {e}")
            raise
    
    async def stop(self):
        """모든 서버 중지"""
        try:
            for name, server in self.servers.items():
                await server.stop()
                logger.info(f"{name} 서버가 중지되었습니다.")
            
            logger.info("모든 MCP 서버가 성공적으로 중지되었습니다.")
            
        except Exception as e:
            logger.error(f"서버 중지 중 오류 발생: {e}")
            raise

async def main():
    """메인 함수"""
    try:
        # 환경 변수 확인
        required_env_vars = ['SECRET_KEY', 'ENCRYPTION_KEY']
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        
        if missing_vars:
            logger.error(f"필수 환경 변수가 설정되지 않았습니다: {missing_vars}")
            sys.exit(1)
        
        # 서버 인스턴스 생성
        server = RetirementAIAgentServer()
        
        # 서버 시작
        await server.start()
        
        # 서버가 계속 실행되도록 대기
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("서버 종료 신호를 받았습니다.")
        finally:
            await server.stop()
            
    except Exception as e:
        logger.error(f"애플리케이션 실행 중 오류 발생: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # 이벤트 루프 실행
    asyncio.run(main())
