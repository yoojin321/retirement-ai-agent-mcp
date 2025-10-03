#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
은퇴 계획 데이터 모델
"""

from datetime import datetime, date
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, validator
from enum import Enum

class ScenarioType(str, Enum):
    """경제 시나리오 타입"""
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"

class EconomicAssumptions(BaseModel):
    """경제 가정"""
    scenario_type: ScenarioType = Field(..., description="시나리오 타입")
    inflation_rate: float = Field(..., ge=0, le=0.2, description="물가상승률")
    pre_retirement_return: float = Field(..., ge=0, le=0.3, description="은퇴전 수익률")
    post_retirement_return: float = Field(..., ge=0, le=0.3, description="은퇴후 수익률")
    wage_growth_rate: float = Field(..., ge=0, le=0.2, description="임금상승률")
    
    @validator('post_retirement_return')
    def validate_post_retirement_return(cls, v, values):
        if 'pre_retirement_return' in values and v > values['pre_retirement_return']:
            raise ValueError('은퇴후 수익률은 은퇴전 수익률보다 낮아야 합니다.')
        return v

class RetirementGoal(BaseModel):
    """은퇴 목표"""
    target_retirement_age: int = Field(..., ge=50, le=80, description="목표 은퇴 연령")
    target_monthly_income: float = Field(..., gt=0, description="목표 월 소득")
    target_annual_income: float = Field(..., gt=0, description="목표 연 소득")
    retirement_period: int = Field(..., ge=10, le=50, description="은퇴 기간")
    required_capital: float = Field(..., gt=0, description="필요 자본")
    medical_reserve: float = Field(default=0, ge=0, description="의료비 예비금")
    
    @property
    def total_required_capital(self) -> float:
        """총 필요 자본"""
        return self.required_capital + self.medical_reserve

class AssetProjection(BaseModel):
    """자산 프로젝션"""
    current_assets: float = Field(..., ge=0, description="현재 자산")
    projected_assets: float = Field(..., ge=0, description="예상 자산")
    annual_contribution: float = Field(..., ge=0, description="연간 저축액")
    years_to_retirement: int = Field(..., ge=0, description="은퇴까지 년수")
    expected_return: float = Field(..., ge=0, le=0.3, description="예상 수익률")
    
    @property
    def funding_gap(self) -> float:
        """자금 격차"""
        return self.projected_assets - self.current_assets

class PortfolioAllocation(BaseModel):
    """포트폴리오 배분"""
    stocks: float = Field(..., ge=0, le=1, description="주식 비중")
    bonds: float = Field(..., ge=0, le=1, description="채권 비중")
    cash: float = Field(..., ge=0, le=1, description="현금 비중")
    alternatives: float = Field(default=0, ge=0, le=1, description="대체투자 비중")
    
    @validator('stocks', 'bonds', 'cash', 'alternatives')
    def validate_allocation(cls, v):
        if v < 0 or v > 1:
            raise ValueError('배분 비중은 0과 1 사이여야 합니다.')
        return v
    
    @validator('alternatives')
    def validate_total_allocation(cls, v, values):
        total = sum(values.values()) + v
        if abs(total - 1.0) > 0.01:  # 1% 오차 허용
            raise ValueError(f'총 배분 비중은 100%여야 합니다. 현재: {total*100:.1f}%')
        return v

class WithdrawalStrategy(BaseModel):
    """인출 전략"""
    withdrawal_rate: float = Field(..., ge=0.01, le=0.1, description="인출률")
    withdrawal_method: str = Field(default="fixed", description="인출 방법")
    tax_optimization: bool = Field(default=True, description="세금 최적화")
    bucket_strategy: bool = Field(default=True, description="버킷 전략 사용")
    
    @validator('withdrawal_method')
    def validate_withdrawal_method(cls, v):
        allowed_methods = ['fixed', 'variable', 'inflation_adjusted']
        if v not in allowed_methods:
            raise ValueError(f'인출 방법은 {allowed_methods} 중 하나여야 합니다.')
        return v

class RetirementPlan(BaseModel):
    """은퇴 계획 통합 모델"""
    plan_id: str = Field(..., description="계획 ID")
    user_id: str = Field(..., description="사용자 ID")
    economic_assumptions: EconomicAssumptions
    retirement_goal: RetirementGoal
    asset_projection: AssetProjection
    portfolio_allocation: PortfolioAllocation
    withdrawal_strategy: WithdrawalStrategy
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat()
        }
    
    def update_timestamp(self):
        """업데이트 시간 갱신"""
        self.updated_at = datetime.now()
    
    def calculate_success_probability(self) -> float:
        """성공 확률 계산 (간단한 예시)"""
        # 실제로는 몬테카를로 시뮬레이션 등을 사용
        if self.asset_projection.funding_gap > 0:
            return 0.8  # 자금이 충분한 경우
        else:
            return 0.3  # 자금이 부족한 경우
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return self.dict()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RetirementPlan':
        """딕셔너리에서 생성"""
        return cls(**data)
