#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
사용자 프로필 데이터 모델
"""

from datetime import datetime, date
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, validator

class PersonalInfo(BaseModel):
    """개인 정보"""
    current_age: int = Field(..., ge=18, le=100, description="현재 나이")
    target_retirement_age: int = Field(..., ge=50, le=80, description="목표 은퇴 연령")
    life_expectancy: int = Field(default=85, ge=60, le=120, description="기대 수명")
    health_status: str = Field(default="good", description="건강 상태")
    family_dependents: int = Field(default=0, ge=0, description="부양 가족 수")
    
    @validator('target_retirement_age')
    def validate_retirement_age(cls, v, values):
        if 'current_age' in values and v <= values['current_age']:
            raise ValueError('목표 은퇴 연령은 현재 나이보다 커야 합니다.')
        return v

class IncomeStructure(BaseModel):
    """소득 구조"""
    monthly_income: float = Field(..., gt=0, description="월 소득 (세후)")
    annual_bonus: float = Field(default=0, ge=0, description="연간 보너스")
    rental_income: float = Field(default=0, ge=0, description="임대 수입")
    other_income: float = Field(default=0, ge=0, description="기타 수입")
    income_growth_rate: float = Field(default=0.03, ge=0, le=0.2, description="소득 증가율")
    
    @property
    def total_annual_income(self) -> float:
        """연간 총 소득"""
        return (self.monthly_income * 12) + self.annual_bonus + self.rental_income + self.other_income

class ExpenseStructure(BaseModel):
    """지출 구조"""
    essential_expenses: float = Field(..., gt=0, description="필수 지출 (월)")
    discretionary_expenses: float = Field(default=0, ge=0, description="선택 지출 (월)")
    retirement_expenses: float = Field(..., gt=0, description="은퇴 후 희망 생활비 (월)")
    major_expenses: List[Dict[str, Any]] = Field(default=[], description="대형 지출 계획")
    
    @property
    def total_monthly_expenses(self) -> float:
        """월간 총 지출"""
        return self.essential_expenses + self.discretionary_expenses

class AssetPortfolio(BaseModel):
    """자산 포트폴리오"""
    # 현금성 자산
    cash_savings: float = Field(default=0, ge=0, description="현금 및 예적금")
    money_market_funds: float = Field(default=0, ge=0, description="머니마켓펀드")
    
    # 투자 자산
    stocks: float = Field(default=0, ge=0, description="주식")
    bonds: float = Field(default=0, ge=0, description="채권")
    mutual_funds: float = Field(default=0, ge=0, description="펀드")
    etfs: float = Field(default=0, ge=0, description="ETF")
    
    # 연금 자산
    national_pension: float = Field(default=0, ge=0, description="국민연금 예상 수급액")
    occupational_pension: float = Field(default=0, ge=0, description="퇴직연금")
    personal_pension: float = Field(default=0, ge=0, description="개인연금")
    
    # 부동산
    primary_residence: float = Field(default=0, ge=0, description="주거용 부동산")
    investment_property: float = Field(default=0, ge=0, description="투자용 부동산")
    
    # 기타 자산
    insurance_cash_value: float = Field(default=0, ge=0, description="보험 해지환급금")
    other_assets: float = Field(default=0, ge=0, description="기타 자산")
    
    @property
    def total_liquid_assets(self) -> float:
        """총 유동 자산"""
        return (self.cash_savings + self.money_market_funds + 
                self.stocks + self.bonds + self.mutual_funds + self.etfs)
    
    @property
    def total_pension_assets(self) -> float:
        """총 연금 자산"""
        return self.national_pension + self.occupational_pension + self.personal_pension
    
    @property
    def total_real_estate(self) -> float:
        """총 부동산 자산"""
        return self.primary_residence + self.investment_property
    
    @property
    def total_assets(self) -> float:
        """총 자산"""
        return (self.total_liquid_assets + self.total_pension_assets + 
                self.total_real_estate + self.insurance_cash_value + self.other_assets)

class DebtStructure(BaseModel):
    """부채 구조"""
    mortgage_balance: float = Field(default=0, ge=0, description="주택담보대출 잔액")
    mortgage_rate: float = Field(default=0.04, ge=0, le=0.2, description="주택담보대출 금리")
    credit_card_debt: float = Field(default=0, ge=0, description="신용카드 부채")
    personal_loans: float = Field(default=0, ge=0, description="개인 대출")
    other_debts: float = Field(default=0, ge=0, description="기타 부채")
    
    @property
    def total_debt(self) -> float:
        """총 부채"""
        return (self.mortgage_balance + self.credit_card_debt + 
                self.personal_loans + self.other_debts)

class InvestmentPreferences(BaseModel):
    """투자 성향"""
    risk_tolerance: str = Field(default="moderate", description="위험 성향")
    investment_horizon: int = Field(default=20, ge=1, le=50, description="투자 기간")
    liquidity_needs: List[Dict[str, Any]] = Field(default=[], description="유동성 필요 시점")
    preferred_assets: List[str] = Field(default=[], description="선호 자산군")
    
    @validator('risk_tolerance')
    def validate_risk_tolerance(cls, v):
        allowed_values = ['conservative', 'moderate', 'aggressive']
        if v not in allowed_values:
            raise ValueError(f'위험 성향은 {allowed_values} 중 하나여야 합니다.')
        return v

class UserProfile(BaseModel):
    """사용자 프로필 통합 모델"""
    user_id: str = Field(..., description="사용자 ID")
    personal_info: PersonalInfo
    income_structure: IncomeStructure
    expense_structure: ExpenseStructure
    asset_portfolio: AssetPortfolio
    debt_structure: DebtStructure
    investment_preferences: InvestmentPreferences
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
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return self.dict()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserProfile':
        """딕셔너리에서 생성"""
        return cls(**data)
