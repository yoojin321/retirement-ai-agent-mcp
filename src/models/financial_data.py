#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
금융 데이터 모델
"""

from datetime import datetime, date
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from enum import Enum

class AssetType(str, Enum):
    """자산 타입"""
    CASH = "cash"
    STOCK = "stock"
    BOND = "bond"
    FUND = "fund"
    ETF = "etf"
    REAL_ESTATE = "real_estate"
    PENSION = "pension"
    INSURANCE = "insurance"

class TransactionType(str, Enum):
    """거래 타입"""
    BUY = "buy"
    SELL = "sell"
    DIVIDEND = "dividend"
    INTEREST = "interest"
    CONTRIBUTION = "contribution"
    WITHDRAWAL = "withdrawal"

class MarketData(BaseModel):
    """시장 데이터"""
    symbol: str = Field(..., description="종목 심볼")
    price: float = Field(..., gt=0, description="가격")
    volume: int = Field(default=0, ge=0, description="거래량")
    market_cap: Optional[float] = Field(None, gt=0, description="시가총액")
    pe_ratio: Optional[float] = Field(None, gt=0, description="PER")
    dividend_yield: Optional[float] = Field(None, ge=0, description="배당수익률")
    timestamp: datetime = Field(default_factory=datetime.now, description="시점")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class AssetHolding(BaseModel):
    """자산 보유"""
    asset_id: str = Field(..., description="자산 ID")
    asset_type: AssetType = Field(..., description="자산 타입")
    symbol: str = Field(..., description="종목 심볼")
    quantity: float = Field(..., gt=0, description="수량")
    average_cost: float = Field(..., gt=0, description="평균 단가")
    current_price: float = Field(..., gt=0, description="현재 가격")
    market_value: float = Field(..., ge=0, description="시장 가치")
    unrealized_pnl: float = Field(default=0, description="미실현 손익")
    
    @property
    def total_cost(self) -> float:
        """총 매수금액"""
        return self.quantity * self.average_cost
    
    @property
    def pnl_percentage(self) -> float:
        """손익률"""
        if self.total_cost == 0:
            return 0
        return (self.unrealized_pnl / self.total_cost) * 100

class Transaction(BaseModel):
    """거래 내역"""
    transaction_id: str = Field(..., description="거래 ID")
    asset_id: str = Field(..., description="자산 ID")
    transaction_type: TransactionType = Field(..., description="거래 타입")
    quantity: float = Field(..., gt=0, description="수량")
    price: float = Field(..., gt=0, description="가격")
    amount: float = Field(..., gt=0, description="거래 금액")
    fees: float = Field(default=0, ge=0, description="수수료")
    tax: float = Field(default=0, ge=0, description="세금")
    transaction_date: datetime = Field(default_factory=datetime.now, description="거래일")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class Portfolio(BaseModel):
    """포트폴리오"""
    portfolio_id: str = Field(..., description="포트폴리오 ID")
    user_id: str = Field(..., description="사용자 ID")
    name: str = Field(..., description="포트폴리오 이름")
    assets: List[AssetHolding] = Field(default=[], description="보유 자산")
    target_allocation: Dict[str, float] = Field(default={}, description="목표 배분")
    rebalancing_threshold: float = Field(default=0.05, ge=0, le=0.2, description="리밸런싱 임계값")
    created_at: datetime = Field(default_factory=datetime.now, description="생성일")
    updated_at: datetime = Field(default_factory=datetime.now, description="수정일")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    @property
    def total_value(self) -> float:
        """총 가치"""
        return sum(asset.market_value for asset in self.assets)
    
    @property
    def total_cost(self) -> float:
        """총 매수금액"""
        return sum(asset.total_cost for asset in self.assets)
    
    @property
    def total_pnl(self) -> float:
        """총 손익"""
        return sum(asset.unrealized_pnl for asset in self.assets)
    
    @property
    def total_pnl_percentage(self) -> float:
        """총 손익률"""
        if self.total_cost == 0:
            return 0
        return (self.total_pnl / self.total_cost) * 100
    
    def get_asset_allocation(self) -> Dict[str, float]:
        """현재 자산 배분"""
        if self.total_value == 0:
            return {}
        
        allocation = {}
        for asset in self.assets:
            allocation[asset.symbol] = asset.market_value / self.total_value
        
        return allocation
    
    def needs_rebalancing(self) -> bool:
        """리밸런싱 필요 여부"""
        if not self.target_allocation:
            return False
        
        current_allocation = self.get_asset_allocation()
        
        for symbol, target_ratio in self.target_allocation.items():
            current_ratio = current_allocation.get(symbol, 0)
            if abs(current_ratio - target_ratio) > self.rebalancing_threshold:
                return True
        
        return False

class EconomicIndicator(BaseModel):
    """경제 지표"""
    indicator_name: str = Field(..., description="지표명")
    value: float = Field(..., description="값")
    unit: str = Field(..., description="단위")
    country: str = Field(..., description="국가")
    indicator_date: date = Field(..., description="날짜")
    source: str = Field(..., description="출처")
    
    class Config:
        json_encoders = {
            date: lambda v: v.isoformat()
        }

class InterestRate(BaseModel):
    """금리 정보"""
    rate_type: str = Field(..., description="금리 타입")
    rate: float = Field(..., ge=0, le=1, description="금리")
    term: str = Field(..., description="기간")
    bank: str = Field(..., description="은행")
    rate_date: date = Field(..., description="날짜")
    
    class Config:
        json_encoders = {
            date: lambda v: v.isoformat()
        }
