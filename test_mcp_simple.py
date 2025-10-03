#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
간단한 MCP 서버 테스트
"""

import asyncio
import sys
import os
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.servers.accumulation_server import AccumulationServer
from src.servers.investment_server import InvestmentServer
from src.servers.withdrawal_server import WithdrawalServer
from src.servers.data_server import DataServer
from src.servers.external_api_server import ExternalAPIServer

async def test_simple():
    """간단한 MCP 서버 테스트"""
    print("🔧 간단한 MCP 서버 테스트")
    print("=" * 40)
    
    # 서버들 초기화
    servers = {
        'accumulation': AccumulationServer(),
        'investment': InvestmentServer(),
        'withdrawal': WithdrawalServer(),
        'data': DataServer(),
        'external_api': ExternalAPIServer()
    }
    
    try:
        # 모든 서버 시작
        for name, server in servers.items():
            await server.start()
            print(f"✅ {name} 서버 시작됨")
        
        print("\n📊 서버 상태:")
        for name, server in servers.items():
            status = "실행 중" if server.is_running else "중지됨"
            print(f"- {name}: {status}")
        
        # 간단한 도구 테스트
        print("\n🔧 도구 테스트:")
        
        # 적립메이트 도구 목록
        accumulation_tools = list(servers['accumulation'].tools.keys())
        print(f"- 적립메이트 도구: {len(accumulation_tools)}개")
        
        # 투자메이트 도구 목록
        investment_tools = list(servers['investment'].tools.keys())
        print(f"- 투자메이트 도구: {len(investment_tools)}개")
        
        # 인출메이트 도구 목록
        withdrawal_tools = list(servers['withdrawal'].tools.keys())
        print(f"- 인출메이트 도구: {len(withdrawal_tools)}개")
        
        # 데이터 관리 도구 목록
        data_tools = list(servers['data'].tools.keys())
        print(f"- 데이터 관리 도구: {len(data_tools)}개")
        
        # 외부 API 도구 목록
        external_tools = list(servers['external_api'].tools.keys())
        print(f"- 외부 API 도구: {len(external_tools)}개")
        
        print(f"\n🎉 총 {sum([len(server.tools) for server in servers.values()])}개의 도구가 사용 가능합니다!")
        
    except Exception as e:
        print(f"❌ 테스트 실패: {str(e)}")
    
    finally:
        # 모든 서버 중지
        for name, server in servers.items():
            await server.stop()
            print(f"🛑 {name} 서버 중지됨")

if __name__ == "__main__":
    asyncio.run(test_simple())
