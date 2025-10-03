#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Docker 컨테이너용 HTTP API 서버 엔트리포인트
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

# FastAPI 및 uvicorn 임포트
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import uvicorn

# 로거 설정
logger = setup_logger(__name__)

# FastAPI 앱 생성
app = FastAPI(
    title="은퇴 설계 AI 에이전트 API",
    description="은퇴 설계를 위한 종합 AI 에이전트 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 전역 서버 인스턴스들
accumulation_server = AccumulationServer()
investment_server = InvestmentServer()
withdrawal_server = WithdrawalServer()
data_server = DataServer()
external_api_server = ExternalAPIServer()

# Pydantic 모델들
class UserProfile(BaseModel):
    user_id: str
    age: int
    income: int
    current_assets: int
    retirement_age: int
    target_assets: int
    risk_tolerance: str

class InvestmentProfile(BaseModel):
    user_id: str
    age: int
    income: int
    assets: int
    investment_experience: str
    risk_tolerance: str
    time_horizon: int

class WithdrawalProfile(BaseModel):
    user_id: str
    total_assets: int
    monthly_income_needed: int
    retirement_years: int
    inflation_rate: float
    tax_rate: float
    risk_tolerance: str

# 서버 시작/종료 이벤트
@app.on_event("startup")
async def startup_event():
    """서버 시작 시 초기화"""
    logger.info("Docker HTTP API 서버 시작 중...")
    
    try:
        await accumulation_server.start()
        await investment_server.start()
        await withdrawal_server.start()
        await data_server.start()
        await external_api_server.start()
        
        logger.info("모든 MCP 서버가 성공적으로 시작되었습니다.")
    except Exception as e:
        logger.error(f"서버 시작 중 오류 발생: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """서버 종료 시 정리"""
    logger.info("Docker HTTP API 서버 종료 중...")
    
    try:
        await accumulation_server.stop()
        await investment_server.stop()
        await withdrawal_server.stop()
        await data_server.stop()
        await external_api_server.stop()
        
        logger.info("모든 MCP 서버가 성공적으로 중지되었습니다.")
    except Exception as e:
        logger.error(f"서버 중지 중 오류 발생: {e}")

# 적립메이트 API
@app.post("/api/accumulation/collect-profile")
async def collect_user_profile(profile: UserProfile):
    """사용자 프로필 수집"""
    try:
        result = await accumulation_server.collect_user_profile(
            user_id=profile.user_id,
            age=profile.age,
            income=profile.income,
            current_assets=profile.current_assets,
            retirement_age=profile.retirement_age,
            target_assets=profile.target_assets,
            risk_tolerance=profile.risk_tolerance
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/accumulation/calculate-retirement-goal/{user_id}")
async def calculate_retirement_goal(user_id: str):
    """은퇴 목표 자금 계산"""
    try:
        result = await accumulation_server.calculate_retirement_goal(user_id=user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 투자메이트 API
@app.post("/api/investment/evaluate-risk-profile")
async def evaluate_risk_profile(profile: InvestmentProfile):
    """리스크 프로파일 평가"""
    try:
        result = await investment_server.evaluate_risk_profile(
            user_id=profile.user_id,
            age=profile.age,
            income=profile.income,
            assets=profile.assets,
            investment_experience=profile.investment_experience,
            risk_tolerance=profile.risk_tolerance,
            time_horizon=profile.time_horizon
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/investment/analyze-market-volatility")
async def analyze_market_volatility():
    """시장 변동성 분석"""
    try:
        result = await investment_server.analyze_market_volatility()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 인출메이트 API
@app.post("/api/withdrawal/analyze-retirement-assets")
async def analyze_retirement_assets(profile: WithdrawalProfile):
    """은퇴 자산 구조 분석"""
    try:
        result = await withdrawal_server.analyze_retirement_assets(
            user_id=profile.user_id,
            total_assets=profile.total_assets,
            monthly_income_needed=profile.monthly_income_needed,
            retirement_years=profile.retirement_years,
            inflation_rate=profile.inflation_rate,
            tax_rate=profile.tax_rate,
            risk_tolerance=profile.risk_tolerance
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 데이터 관리 API
@app.post("/api/data/backup")
async def backup_user_data(user_id: str, backup_type: str = "full"):
    """사용자 데이터 백업"""
    try:
        result = await data_server.backup_user_data(
            user_id=user_id,
            backup_type=backup_type
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/data/backups/{user_id}")
async def list_backups(user_id: str):
    """백업 목록 조회"""
    try:
        result = await data_server.list_backups(user_id=user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 외부 API
@app.get("/api/external/market-data")
async def fetch_market_data(symbols: Optional[str] = None, period: str = "1mo"):
    """시장 데이터 수집"""
    try:
        symbol_list = symbols.split(",") if symbols else None
        result = await external_api_server.fetch_market_data(
            symbols=symbol_list,
            period=period
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/external/economic-indicators")
async def fetch_economic_indicators(country: str = "US"):
    """경제 지표 수집"""
    try:
        result = await external_api_server.fetch_economic_indicators(country=country)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 헬스 체크
@app.get("/api/health")
async def health_check():
    """헬스 체크"""
    return {
        "status": "healthy",
        "message": "은퇴 설계 AI 에이전트 API가 정상 작동 중입니다.",
        "timestamp": "2024-10-03T10:00:00Z",
        "services": {
            "accumulation": "running",
            "investment": "running", 
            "withdrawal": "running",
            "data": "running",
            "external_api": "running"
        }
    }

# API 문서
@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "은퇴 설계 AI 에이전트 API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    # 환경 변수 확인
    required_env_vars = ['SECRET_KEY', 'ENCRYPTION_KEY']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"필수 환경 변수가 설정되지 않았습니다: {missing_vars}")
        sys.exit(1)
    
    # uvicorn 서버 실행
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
