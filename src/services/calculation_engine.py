#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
금융 계산 엔진
"""

import math
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime, date
import numpy as np
from scipy import stats

class FinancialCalculator:
    """금융 계산기 기본 클래스"""
    
    @staticmethod
    def future_value(
        present_value: float,
        interest_rate: float,
        periods: int,
        payment: float = 0,
        payment_timing: str = "end"
    ) -> float:
        """
        미래가치 계산
        
        Args:
            present_value: 현재가치
            interest_rate: 이자율
            periods: 기간
            payment: 정기 납입액
            payment_timing: 납입 시점 ("begin" 또는 "end")
        
        Returns:
            미래가치
        """
        if interest_rate == 0:
            return present_value + (payment * periods)
        
        fv_pv = present_value * (1 + interest_rate) ** periods
        
        if payment == 0:
            return fv_pv
        
        if payment_timing == "begin":
            fv_payment = payment * ((1 + interest_rate) ** periods - 1) / interest_rate * (1 + interest_rate)
        else:  # end
            fv_payment = payment * ((1 + interest_rate) ** periods - 1) / interest_rate
        
        return fv_pv + fv_payment
    
    @staticmethod
    def present_value(
        future_value: float,
        interest_rate: float,
        periods: int,
        payment: float = 0,
        payment_timing: str = "end"
    ) -> float:
        """
        현재가치 계산
        
        Args:
            future_value: 미래가치
            interest_rate: 이자율
            periods: 기간
            payment: 정기 납입액
            payment_timing: 납입 시점 ("begin" 또는 "end")
        
        Returns:
            현재가치
        """
        if interest_rate == 0:
            return future_value - (payment * periods)
        
        pv_fv = future_value / (1 + interest_rate) ** periods
        
        if payment == 0:
            return pv_fv
        
        if payment_timing == "begin":
            pv_payment = payment * (1 - (1 + interest_rate) ** (-periods)) / interest_rate * (1 + interest_rate)
        else:  # end
            pv_payment = payment * (1 - (1 + interest_rate) ** (-periods)) / interest_rate
        
        return pv_fv + pv_payment
    
    @staticmethod
    def payment(
        present_value: float,
        future_value: float,
        interest_rate: float,
        periods: int,
        payment_timing: str = "end"
    ) -> float:
        """
        정기 납입액 계산
        
        Args:
            present_value: 현재가치
            future_value: 미래가치
            interest_rate: 이자율
            periods: 기간
            payment_timing: 납입 시점 ("begin" 또는 "end")
        
        Returns:
            정기 납입액
        """
        if interest_rate == 0:
            return (future_value - present_value) / periods
        
        if payment_timing == "begin":
            return (future_value - present_value * (1 + interest_rate) ** periods) / \
                   ((1 + interest_rate) * ((1 + interest_rate) ** periods - 1) / interest_rate)
        else:  # end
            return (future_value - present_value * (1 + interest_rate) ** periods) / \
                   ((1 + interest_rate) ** periods - 1) / interest_rate

class RetirementCalculator:
    """은퇴 계산기"""
    
    def __init__(self):
        self.financial_calc = FinancialCalculator()
    
    def calculate_retirement_goal(
        self,
        annual_income_needed: float,
        inflation_rate: float,
        years_to_retirement: int,
        retirement_period: int,
        post_retirement_return: float,
        safe_withdrawal_rate: float = 0.04
    ) -> Dict[str, float]:
        """
        은퇴 목표 자금 계산
        
        Args:
            annual_income_needed: 연간 필요 소득
            inflation_rate: 물가상승률
            years_to_retirement: 은퇴까지 년수
            retirement_period: 은퇴 기간
            post_retirement_return: 은퇴후 수익률
            safe_withdrawal_rate: 안전인출률
        
        Returns:
            계산 결과 딕셔너리
        """
        # 물가 반영한 은퇴시점 필요 소득
        real_income_at_retirement = annual_income_needed * (1 + inflation_rate) ** years_to_retirement
        
        # 안전인출률법
        swr_required = real_income_at_retirement / safe_withdrawal_rate
        
        # 연금현가법
        pv_required = self.financial_calc.present_value(
            future_value=0,
            interest_rate=post_retirement_return,
            periods=retirement_period,
            payment=real_income_at_retirement,
            payment_timing="end"
        )
        
        return {
            "real_income_at_retirement": real_income_at_retirement,
            "swr_required_capital": swr_required,
            "pv_required_capital": pv_required,
            "recommended_capital": (swr_required + pv_required) / 2
        }
    
    def project_retirement_assets(
        self,
        current_assets: float,
        annual_contribution: float,
        years_to_retirement: int,
        expected_return: float,
        contribution_growth_rate: float = 0.03
    ) -> Dict[str, float]:
        """
        은퇴시점 자산 프로젝션
        
        Args:
            current_assets: 현재 자산
            annual_contribution: 연간 저축액
            years_to_retirement: 은퇴까지 년수
            expected_return: 예상 수익률
            contribution_growth_rate: 저축액 증가율
        
        Returns:
            프로젝션 결과
        """
        # 현재 자산의 미래가치
        future_value_current = self.financial_calc.future_value(
            present_value=current_assets,
            interest_rate=expected_return,
            periods=years_to_retirement
        )
        
        # 정기 저축의 미래가치 (매년 증가하는 저축액)
        total_contribution_fv = 0
        for year in range(years_to_retirement):
            contribution = annual_contribution * (1 + contribution_growth_rate) ** year
            remaining_years = years_to_retirement - year
            contribution_fv = self.financial_calc.future_value(
                present_value=0,
                interest_rate=expected_return,
                periods=remaining_years,
                payment=contribution,
                payment_timing="end"
            )
            total_contribution_fv += contribution_fv
        
        total_projected_assets = future_value_current + total_contribution_fv
        
        return {
            "current_assets_fv": future_value_current,
            "contributions_fv": total_contribution_fv,
            "total_projected_assets": total_projected_assets
        }
    
    def calculate_funding_gap(
        self,
        required_capital: float,
        projected_assets: float
    ) -> Dict[str, float]:
        """
        자금 격차 계산
        
        Args:
            required_capital: 필요 자본
            projected_assets: 예상 자산
        
        Returns:
            자금 격차 분석
        """
        gap = projected_assets - required_capital
        gap_percentage = (gap / required_capital) * 100 if required_capital > 0 else 0
        
        return {
            "funding_gap": gap,
            "gap_percentage": gap_percentage,
            "is_sufficient": gap >= 0,
            "shortfall": abs(gap) if gap < 0 else 0
        }

class PortfolioCalculator:
    """포트폴리오 계산기"""
    
    def __init__(self):
        self.financial_calc = FinancialCalculator()
    
    def calculate_portfolio_metrics(
        self,
        returns: List[float],
        risk_free_rate: float = 0.02
    ) -> Dict[str, float]:
        """
        포트폴리오 성과 지표 계산
        
        Args:
            returns: 수익률 리스트
            risk_free_rate: 무위험 수익률
        
        Returns:
            성과 지표
        """
        if not returns:
            return {}
        
        returns_array = np.array(returns)
        
        # 기본 통계
        mean_return = np.mean(returns_array)
        volatility = np.std(returns_array)
        
        # 샤프 비율
        sharpe_ratio = (mean_return - risk_free_rate) / volatility if volatility > 0 else 0
        
        # 최대 낙폭 (MDD)
        cumulative_returns = np.cumprod(1 + returns_array)
        running_max = np.maximum.accumulate(cumulative_returns)
        drawdown = (cumulative_returns - running_max) / running_max
        max_drawdown = np.min(drawdown)
        
        # 소르티노 비율
        negative_returns = returns_array[returns_array < 0]
        downside_deviation = np.std(negative_returns) if len(negative_returns) > 0 else 0
        sortino_ratio = (mean_return - risk_free_rate) / downside_deviation if downside_deviation > 0 else 0
        
        return {
            "mean_return": mean_return,
            "volatility": volatility,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": max_drawdown,
            "sortino_ratio": sortino_ratio
        }
    
    def calculate_optimal_allocation(
        self,
        expected_returns: Dict[str, float],
        covariance_matrix: np.ndarray,
        risk_tolerance: float = 0.5
    ) -> Dict[str, float]:
        """
        최적 자산 배분 계산 (마코위츠 모델)
        
        Args:
            expected_returns: 자산별 기대 수익률
            covariance_matrix: 공분산 행렬
            risk_tolerance: 위험 허용도 (0-1)
        
        Returns:
            최적 배분 비중
        """
        try:
            # 자산 수
            n_assets = len(expected_returns)
            asset_names = list(expected_returns.keys())
            
            # 기대 수익률 벡터
            mu = np.array([expected_returns[name] for name in asset_names])
            
            # 제약조건: 합이 1, 각 자산 비중이 0 이상
            constraints = [
                {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
            ]
            bounds = [(0, 1) for _ in range(n_assets)]
            
            # 목적함수: 위험 조정 수익률 최대화
            def objective(x):
                portfolio_return = np.dot(x, mu)
                portfolio_variance = np.dot(x, np.dot(covariance_matrix, x))
                return -(portfolio_return - risk_tolerance * portfolio_variance)
            
            # 초기값
            x0 = np.array([1/n_assets] * n_assets)
            
            # 최적화
            from scipy.optimize import minimize
            result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)
            
            if result.success:
                allocation = {asset_names[i]: result.x[i] for i in range(n_assets)}
                return allocation
            else:
                # 최적화 실패 시 균등 배분
                return {name: 1/n_assets for name in asset_names}
                
        except Exception as e:
            # 오류 발생 시 균등 배분
            n_assets = len(expected_returns)
            return {name: 1/n_assets for name in expected_returns.keys()}

class WithdrawalCalculator:
    """인출 계산기"""
    
    def __init__(self):
        self.financial_calc = FinancialCalculator()
    
    def calculate_safe_withdrawal_rate(
        self,
        portfolio_value: float,
        annual_expenses: float,
        expected_return: float,
        inflation_rate: float,
        years: int
    ) -> Dict[str, float]:
        """
        안전인출률 계산
        
        Args:
            portfolio_value: 포트폴리오 가치
            annual_expenses: 연간 지출
            expected_return: 예상 수익률
            inflation_rate: 물가상승률
            years: 기간
        
        Returns:
            인출률 분석
        """
        # 기본 인출률
        base_withdrawal_rate = annual_expenses / portfolio_value
        
        # 물가 연동 인출
        real_return = (1 + expected_return) / (1 + inflation_rate) - 1
        
        # 지속 가능성 검증
        sustainable_rate = real_return if real_return > 0 else 0.03
        
        return {
            "current_withdrawal_rate": base_withdrawal_rate,
            "sustainable_rate": sustainable_rate,
            "is_sustainable": base_withdrawal_rate <= sustainable_rate,
            "recommended_rate": min(base_withdrawal_rate, sustainable_rate)
        }
    
    def calculate_bucket_strategy(
        self,
        total_portfolio: float,
        annual_expenses: float,
        years_to_cover: int = 5
    ) -> Dict[str, float]:
        """
        3버킷 전략 계산
        
        Args:
            total_portfolio: 총 포트폴리오 가치
            annual_expenses: 연간 지출
            years_to_cover: 커버할 년수
        
        Returns:
            버킷별 배분
        """
        # 버킷1: 현금 (2년분)
        bucket1_amount = annual_expenses * 2
        
        # 버킷2: 중기채권 (3년분)
        bucket2_amount = annual_expenses * 3
        
        # 버킷3: 나머지 (성장자산)
        bucket3_amount = total_portfolio - bucket1_amount - bucket2_amount
        
        return {
            "bucket1_cash": bucket1_amount,
            "bucket2_bonds": bucket2_amount,
            "bucket3_growth": bucket3_amount,
            "bucket1_ratio": bucket1_amount / total_portfolio,
            "bucket2_ratio": bucket2_amount / total_portfolio,
            "bucket3_ratio": bucket3_amount / total_portfolio
        }
