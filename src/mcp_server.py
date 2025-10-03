#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude Desktop용 표준 MCP 서버
"""

import asyncio
import json
import sys
import os
from pathlib import Path
from typing import Dict, Any, List

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.servers.accumulation_server import AccumulationServer
from src.servers.investment_server import InvestmentServer
from src.servers.withdrawal_server import WithdrawalServer
from src.servers.data_server import DataServer
from src.servers.external_api_server import ExternalAPIServer

class RetirementAIMCPServer:
    """Claude Desktop용 MCP 서버"""
    
    def __init__(self):
        self.servers = {}
        self.setup_servers()
    
    def setup_servers(self):
        """모든 MCP 서버 초기화"""
        self.servers['accumulation'] = AccumulationServer()
        self.servers['investment'] = InvestmentServer()
        self.servers['withdrawal'] = WithdrawalServer()
        self.servers['data'] = DataServer()
        self.servers['external_api'] = ExternalAPIServer()
    
    async def start(self):
        """모든 서버 시작"""
        for server in self.servers.values():
            await server.start()
    
    async def stop(self):
        """모든 서버 중지"""
        for server in self.servers.values():
            await server.stop()
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """사용 가능한 도구 목록 반환"""
        tools = []
        
        for server_name, server in self.servers.items():
            for tool_name, tool_func in server.tools.items():
                tools.append({
                    "name": f"{server_name}_{tool_name}",
                    "description": f"{server_name} 서버의 {tool_name} 도구",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "사용자 ID"},
                            "age": {"type": "integer", "description": "나이"},
                            "income": {"type": "integer", "description": "연봉"},
                            "assets": {"type": "integer", "description": "자산"},
                            "risk_tolerance": {"type": "string", "description": "리스크 성향"},
                            "target_assets": {"type": "integer", "description": "목표 자산"}
                        }
                    }
                })
        
        return tools
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """도구 호출"""
        try:
            # 도구 이름에서 서버와 도구 분리
            if '_' in tool_name:
                server_name, actual_tool_name = tool_name.split('_', 1)
            else:
                server_name = 'accumulation'
                actual_tool_name = tool_name
            
            if server_name in self.servers:
                server = self.servers[server_name]
                if actual_tool_name in server.tools:
                    result = await server.tools[actual_tool_name](**arguments)
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, ensure_ascii=False, indent=2)
                            }
                        ]
                    }
                else:
                    return {"error": f"도구 {actual_tool_name}을 찾을 수 없습니다."}
            else:
                return {"error": f"서버 {server_name}을 찾을 수 없습니다."}
        
        except Exception as e:
            return {"error": f"도구 실행 중 오류 발생: {str(e)}"}

# 전역 서버 인스턴스
mcp_server = RetirementAIMCPServer()

async def main():
    """MCP 서버 메인 함수"""
    try:
        await mcp_server.start()
        
        # MCP 프로토콜 메시지 처리
        while True:
            try:
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                if not line:
                    break
                
                message = json.loads(line.strip())
                
                if message.get("method") == "tools/list":
                    response = {
                        "jsonrpc": "2.0",
                        "id": message.get("id"),
                        "result": {
                            "tools": mcp_server.get_available_tools()
                        }
                    }
                    print(json.dumps(response, ensure_ascii=False))
                    sys.stdout.flush()
                
                elif message.get("method") == "tools/call":
                    tool_name = message["params"]["name"]
                    arguments = message["params"]["arguments"]
                    
                    result = await mcp_server.call_tool(tool_name, arguments)
                    
                    response = {
                        "jsonrpc": "2.0",
                        "id": message.get("id"),
                        "result": result
                    }
                    print(json.dumps(response, ensure_ascii=False))
                    sys.stdout.flush()
                
                elif message.get("method") == "initialize":
                    response = {
                        "jsonrpc": "2.0",
                        "id": message.get("id"),
                        "result": {
                            "protocolVersion": "2024-11-05",
                            "capabilities": {
                                "tools": {}
                            },
                            "serverInfo": {
                                "name": "retirement-ai-agent",
                                "version": "1.0.0"
                            }
                        }
                    }
                    print(json.dumps(response, ensure_ascii=False))
                    sys.stdout.flush()
                
            except json.JSONDecodeError:
                continue
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": message.get("id") if 'message' in locals() else None,
                    "error": {
                        "code": -32603,
                        "message": str(e)
                    }
                }
                print(json.dumps(error_response, ensure_ascii=False))
                sys.stdout.flush()
    
    except KeyboardInterrupt:
        pass
    finally:
        await mcp_server.stop()

if __name__ == "__main__":
    asyncio.run(main())
