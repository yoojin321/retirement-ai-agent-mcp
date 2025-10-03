#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
은퇴 설계 AI 에이전트 모바일 API 서버
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import asyncio
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.servers.accumulation_server import AccumulationServer
from src.servers.investment_server import InvestmentServer
from src.servers.withdrawal_server import WithdrawalServer
from src.servers.data_server import DataServer
from src.servers.external_api_server import ExternalAPIServer

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

# 서버 인스턴스들
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

class BackupRequest(BaseModel):
    user_id: str
    backup_type: str = "full"

class RestoreRequest(BaseModel):
    user_id: str
    backup_id: str

# 서버 시작/종료 이벤트
@app.on_event("startup")
async def startup_event():
    """서버 시작 시 초기화"""
    await accumulation_server.start()
    await investment_server.start()
    await withdrawal_server.start()
    await data_server.start()
    await external_api_server.start()

@app.on_event("shutdown")
async def shutdown_event():
    """서버 종료 시 정리"""
    await accumulation_server.stop()
    await investment_server.stop()
    await withdrawal_server.stop()
    await data_server.stop()
    await external_api_server.stop()

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

@app.post("/api/accumulation/set-economic-assumptions")
async def set_economic_assumptions(
    user_id: str,
    scenario_type: str,
    inflation_rate: float,
    market_return: float,
    risk_free_rate: float
):
    """경제 가정 설정"""
    try:
        result = await accumulation_server.set_economic_assumptions(
            user_id=user_id,
            scenario_type=scenario_type,
            inflation_rate=inflation_rate,
            market_return=market_return,
            risk_free_rate=risk_free_rate
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

@app.get("/api/investment/optimize-account-usage/{user_id}")
async def optimize_account_usage(user_id: str):
    """계좌 활용 최적화"""
    try:
        result = await investment_server.optimize_account_usage(user_id=user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/investment/generate-portfolio-options")
async def generate_portfolio_options(
    user_id: str,
    risk_score: float,
    investment_amount: int
):
    """포트폴리오 옵션 생성"""
    try:
        result = await investment_server.generate_portfolio_options(
            user_id=user_id,
            risk_score=risk_score,
            investment_amount=investment_amount
        )
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

@app.get("/api/withdrawal/set-withdrawal-baseline/{user_id}")
async def set_withdrawal_baseline(
    user_id: str,
    target_monthly_income: int,
    withdrawal_period: int
):
    """인출 기본선 설정"""
    try:
        result = await withdrawal_server.set_withdrawal_baseline(
            user_id=user_id,
            target_monthly_income=target_monthly_income,
            withdrawal_period=withdrawal_period
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/withdrawal/manage-guardrail-system/{user_id}")
async def manage_guardrail_system(user_id: str):
    """가드레일 시스템 관리"""
    try:
        result = await withdrawal_server.manage_guardrail_system(user_id=user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 데이터 관리 API
@app.post("/api/data/backup")
async def backup_user_data(request: BackupRequest):
    """사용자 데이터 백업"""
    try:
        result = await data_server.backup_user_data(
            user_id=request.user_id,
            backup_type=request.backup_type
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/data/restore")
async def restore_user_data(request: RestoreRequest):
    """사용자 데이터 복원"""
    try:
        result = await data_server.restore_user_data(
            backup_id=request.backup_id,
            user_id=request.user_id
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

@app.post("/api/data/encrypt")
async def encrypt_sensitive_data(
    user_id: str,
    data: Dict[str, Any]
):
    """민감 데이터 암호화"""
    try:
        result = await data_server.encrypt_sensitive_data(
            data=data,
            user_id=user_id
        )
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
async def fetch_economic_indicators(country: str = "KR"):
    """경제 지표 수집"""
    try:
        result = await external_api_server.fetch_economic_indicators(country=country)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/external/pension-info")
async def fetch_pension_info(country: str = "KR"):
    """연금 정보 수집"""
    try:
        result = await external_api_server.fetch_pension_info(country=country)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/external/interest-rates")
async def fetch_interest_rates(country: str = "KR"):
    """금리 정보 수집"""
    try:
        result = await external_api_server.fetch_interest_rates(country=country)
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
        "timestamp": "2024-10-03T10:00:00Z"
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
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
