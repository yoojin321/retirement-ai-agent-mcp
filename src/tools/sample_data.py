#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
샘플 데이터 생성 도구
"""

from typing import Dict, Any

def get_sample_user_data() -> Dict[str, Any]:
    """샘플 사용자 데이터 반환"""
    return {
        "personal_info": {
            "user_id": "sample_user_001",
            "current_age": 35,
            "target_retirement_age": 65,
            "life_expectancy": 85,
            "health_status": "good",
            "family_dependents": 2
        },
        "income_info": {
            "monthly_income": 5000000,  # 500만원
            "annual_bonus": 10000000,   # 1000만원
            "rental_income": 0,
            "other_income": 0,
            "income_growth_rate": 0.03
        },
        "expense_info": {
            "essential_expenses": 3000000,  # 300만원
            "discretionary_expenses": 1000000,  # 100만원
            "retirement_expenses": 4000000,  # 400만원
            "major_expenses": [
                {"name": "자녀 교육비", "amount": 20000000, "year": 5},
                {"name": "주택 보수", "amount": 10000000, "year": 3}
            ]
        },
        "asset_info": {
            "cash_savings": 50000000,      # 5000만원
            "money_market_funds": 10000000, # 1000만원
            "stocks": 30000000,            # 3000만원
            "bonds": 20000000,             # 2000만원
            "mutual_funds": 15000000,      # 1500만원
            "etfs": 10000000,              # 1000만원
            "national_pension": 2000000,   # 200만원 (연간)
            "occupational_pension": 0,
            "personal_pension": 5000000,   # 500만원
            "primary_residence": 500000000, # 5억원
            "investment_property": 0,
            "insurance_cash_value": 5000000, # 500만원
            "other_assets": 0
        },
        "debt_info": {
            "mortgage_balance": 200000000,  # 2억원
            "mortgage_rate": 0.04,
            "credit_card_debt": 0,
            "personal_loans": 0,
            "other_debts": 0
        },
        "investment_preferences": {
            "risk_tolerance": "moderate",
            "investment_horizon": 30,
            "liquidity_needs": [
                {"name": "자녀 교육비", "amount": 20000000, "year": 5}
            ],
            "preferred_assets": ["stocks", "bonds", "etfs"]
        }
    }

def get_sample_economic_scenarios() -> Dict[str, Dict[str, float]]:
    """샘플 경제 시나리오 반환"""
    return {
        "conservative": {
            "inflation_rate": 0.020,
            "pre_retirement_return": 0.025,
            "post_retirement_return": 0.015,
            "wage_growth_rate": 0.030
        },
        "moderate": {
            "inflation_rate": 0.025,
            "pre_retirement_return": 0.040,
            "post_retirement_return": 0.025,
            "wage_growth_rate": 0.040
        },
        "aggressive": {
            "inflation_rate": 0.030,
            "pre_retirement_return": 0.055,
            "post_retirement_return": 0.035,
            "wage_growth_rate": 0.050
        }
    }

def get_sample_portfolio_allocations() -> Dict[str, Dict[str, float]]:
    """샘플 포트폴리오 배분 반환"""
    return {
        "conservative": {
            "stocks": 0.20,
            "bonds": 0.55,
            "cash": 0.10,
            "alternatives": 0.15
        },
        "moderate": {
            "stocks": 0.35,
            "bonds": 0.40,
            "cash": 0.10,
            "alternatives": 0.15
        },
        "aggressive": {
            "stocks": 0.50,
            "bonds": 0.30,
            "cash": 0.05,
            "alternatives": 0.15
        }
    }
