#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
투자메이트 도구 구현
"""

import json
import numpy as np
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

from src.models.user_profile import UserProfile
from src.models.financial_data import Portfolio, AssetHolding, AssetType
from src.services.calculation_engine import PortfolioCalculator, FinancialCalculator

class InvestmentTools:
    """투자메이트 도구 클래스"""
    
    def __init__(self):
        self.portfolio_calc = PortfolioCalculator()
        self.financial_calc = FinancialCalculator()
        self.data_dir = Path("data/user_data")
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    async def assess_risk_profile(
        self,
        user_id: str,
        risk_questionnaire: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        리스크 프로파일 평가
        
        Args:
            user_id: 사용자 ID
            risk_questionnaire: 위험 성향 설문 결과
        
        Returns:
            리스크 프로파일 평가 결과
        """
        try:
            # 사용자 프로필 로드
            profile_file = self.data_dir / f"{user_id}_profile.json"
            if not profile_file.exists():
                return {
                    "status": "error",
                    "message": "사용자 프로필을 찾을 수 없습니다."
                }
            
            with open(profile_file, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
            
            user_profile = UserProfile.from_dict(profile_data)
            
            # 기본 리스크 평가
            age_factor = max(0, (65 - user_profile.personal_info.current_age) / 30)
            income_stability = 1.0 if user_profile.income_structure.monthly_income > 3000000 else 0.7
            asset_ratio = user_profile.asset_portfolio.total_assets / max(user_profile.income_structure.total_annual_income, 1)
            
            # 리스크 점수 계산 (0-100)
            risk_score = (
                age_factor * 40 +  # 나이 요소 (40점)
                income_stability * 30 +  # 소득 안정성 (30점)
                min(asset_ratio / 10, 1) * 30  # 자산 비율 (30점)
            )
            
            # 설문 결과가 있으면 반영
            if risk_questionnaire:
                questionnaire_score = risk_questionnaire.get('risk_tolerance_score', 50)
                risk_score = (risk_score + questionnaire_score) / 2
            
            # 리스크 프로파일 분류
            if risk_score >= 70:
                risk_profile = "aggressive"
                max_stock_ratio = 0.60
            elif risk_score >= 40:
                risk_profile = "moderate"
                max_stock_ratio = 0.40
            else:
                risk_profile = "conservative"
                max_stock_ratio = 0.25
            
            return {
                "status": "success",
                "message": "리스크 프로파일이 평가되었습니다.",
                "risk_assessment": {
                    "risk_score": risk_score,
                    "risk_profile": risk_profile,
                    "max_stock_ratio": max_stock_ratio,
                    "age_factor": age_factor,
                    "income_stability": income_stability,
                    "asset_ratio": asset_ratio
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"리스크 프로파일 평가 중 오류 발생: {str(e)}"
            }
    
    async def analyze_market_volatility(
        self,
        market_data: Optional[Dict[str, List[float]]] = None,
        lookback_period: int = 252  # 1년 (252 거래일)
    ) -> Dict[str, Any]:
        """
        시장 변동성 분석
        
        Args:
            market_data: 시장 데이터 (종목별 수익률)
            lookback_period: 분석 기간
        
        Returns:
            시장 변동성 분석 결과
        """
        try:
            # 샘플 시장 데이터 생성 (실제로는 외부 API에서 가져옴)
            if market_data is None:
                # KOSPI, KOSDAQ, 채권, 금 등 주요 자산군의 수익률 시뮬레이션
                np.random.seed(42)  # 재현 가능한 결과를 위해
                market_data = {
                    "kospi": np.random.normal(0.0008, 0.015, lookback_period).tolist(),  # 일일 수익률
                    "kosdaq": np.random.normal(0.0012, 0.020, lookback_period).tolist(),
                    "bonds": np.random.normal(0.0003, 0.005, lookback_period).tolist(),
                    "gold": np.random.normal(0.0005, 0.010, lookback_period).tolist()
                }
            
            # 각 자산군의 변동성 계산
            volatility_analysis = {}
            for asset, returns in market_data.items():
                returns_array = np.array(returns)
                volatility_analysis[asset] = {
                    "mean_return": np.mean(returns_array),
                    "volatility": np.std(returns_array),
                    "sharpe_ratio": np.mean(returns_array) / np.std(returns_array) if np.std(returns_array) > 0 else 0,
                    "max_drawdown": np.min(np.cumsum(returns_array))
                }
            
            # 전체 시장 변동성 평가
            overall_volatility = np.mean([data["volatility"] for data in volatility_analysis.values()])
            market_regime = "high_volatility" if overall_volatility > 0.02 else "normal_volatility"
            
            return {
                "status": "success",
                "message": "시장 변동성 분석이 완료되었습니다.",
                "volatility_analysis": {
                    "overall_volatility": overall_volatility,
                    "market_regime": market_regime,
                    "asset_volatilities": volatility_analysis,
                    "recommendation": self._get_volatility_recommendation(market_regime)
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"시장 변동성 분석 중 오류 발생: {str(e)}"
            }
    
    def _get_volatility_recommendation(self, market_regime: str) -> str:
        """변동성 체제에 따른 권장사항"""
        if market_regime == "high_volatility":
            return "고변동성 시장입니다. 보수적 포트폴리오를 권장합니다."
        else:
            return "정상 변동성 시장입니다. 균형 잡힌 포트폴리오를 권장합니다."
    
    async def optimize_account_utilization(
        self,
        user_id: str,
        irp_limit: float = 7000000,  # IRP 연간 한도
        pension_savings_limit: float = 7000000  # 연금저축 연간 한도
    ) -> Dict[str, Any]:
        """
        계좌 활용 최적화
        
        Args:
            user_id: 사용자 ID
            irp_limit: IRP 연간 한도
            pension_savings_limit: 연금저축 연간 한도
        
        Returns:
            계좌 활용 최적화 결과
        """
        try:
            # 사용자 프로필 로드
            profile_file = self.data_dir / f"{user_id}_profile.json"
            if not profile_file.exists():
                return {
                    "status": "error",
                    "message": "사용자 프로필을 찾을 수 없습니다."
                }
            
            with open(profile_file, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
            
            user_profile = UserProfile.from_dict(profile_data)
            
            # 연간 저축 가능 금액 계산
            annual_savings_capacity = user_profile.income_structure.total_annual_income - user_profile.expense_structure.total_monthly_expenses * 12
            
            # 세제 혜택 계좌 우선 활용
            tax_advantaged_allocation = {
                "IRP": min(annual_savings_capacity * 0.4, irp_limit),
                "연금저축": min(annual_savings_capacity * 0.3, pension_savings_limit),
                "일반계좌": max(0, annual_savings_capacity - irp_limit - pension_savings_limit)
            }
            
            # 세제 혜택 계산
            tax_benefits = {
                "IRP_세액공제": tax_advantaged_allocation["IRP"] * 0.15,  # 15% 세액공제
                "연금저축_세액공제": tax_advantaged_allocation["연금저축"] * 0.15,
                "총_세제혜택": (tax_advantaged_allocation["IRP"] + tax_advantaged_allocation["연금저축"]) * 0.15
            }
            
            return {
                "status": "success",
                "message": "계좌 활용이 최적화되었습니다.",
                "optimization_result": {
                    "annual_savings_capacity": annual_savings_capacity,
                    "tax_advantaged_allocation": tax_advantaged_allocation,
                    "tax_benefits": tax_benefits,
                    "recommendations": [
                        "IRP와 연금저축을 최대한 활용하여 세제 혜택을 극대화하세요.",
                        "일반계좌는 세제 혜택 계좌를 모두 활용한 후 사용하세요.",
                        "연간 한도를 초과하지 않도록 주의하세요."
                    ]
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"계좌 활용 최적화 중 오류 발생: {str(e)}"
            }
    
    async def generate_portfolio_options(
        self,
        user_id: str,
        risk_profile: str = "moderate"
    ) -> Dict[str, Any]:
        """
        포트폴리오 옵션 생성
        
        Args:
            user_id: 사용자 ID
            risk_profile: 위험 성향
        
        Returns:
            포트폴리오 옵션 생성 결과
        """
        try:
            # 포트폴리오 옵션 정의
            portfolio_options = {
                "conservative": {
                    "stocks": 0.20,
                    "bonds": 0.55,
                    "cash": 0.10,
                    "alternatives": 0.15,
                    "expected_return": 0.045,
                    "expected_volatility": 0.08,
                    "description": "안정성 중심의 보수적 포트폴리오"
                },
                "moderate": {
                    "stocks": 0.35,
                    "bonds": 0.40,
                    "cash": 0.10,
                    "alternatives": 0.15,
                    "expected_return": 0.065,
                    "expected_volatility": 0.12,
                    "description": "균형 잡힌 중립형 포트폴리오"
                },
                "aggressive": {
                    "stocks": 0.50,
                    "bonds": 0.30,
                    "cash": 0.05,
                    "alternatives": 0.15,
                    "expected_return": 0.085,
                    "expected_volatility": 0.18,
                    "description": "성장 중심의 공격적 포트폴리오"
                }
            }
            
            # 선택된 포트폴리오
            selected_portfolio = portfolio_options.get(risk_profile, portfolio_options["moderate"])
            
            # 계좌별 배분 제안
            account_allocation = {
                "IRP": {
                    "stocks": selected_portfolio["stocks"] * 0.6,
                    "bonds": selected_portfolio["bonds"] * 0.4
                },
                "연금저축": {
                    "stocks": selected_portfolio["stocks"] * 0.4,
                    "bonds": selected_portfolio["bonds"] * 0.6
                },
                "일반계좌": {
                    "stocks": selected_portfolio["stocks"],
                    "bonds": selected_portfolio["bonds"],
                    "cash": selected_portfolio["cash"],
                    "alternatives": selected_portfolio["alternatives"]
                }
            }
            
            return {
                "status": "success",
                "message": f"{risk_profile} 포트폴리오 옵션이 생성되었습니다.",
                "portfolio_options": {
                    "selected_portfolio": selected_portfolio,
                    "all_portfolios": portfolio_options,
                    "account_allocation": account_allocation,
                    "implementation_guide": [
                        "IRP와 연금저축에는 주로 주식형 ETF와 채권형 ETF를 배치하세요.",
                        "일반계좌에는 현금성 자산과 대체투자를 포함하세요.",
                        "연 1회 리밸런싱을 통해 목표 비중을 유지하세요."
                    ]
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"포트폴리오 옵션 생성 중 오류 발생: {str(e)}"
            }
    
    async def adjust_for_volatility(
        self,
        base_portfolio: Dict[str, float],
        market_volatility: float,
        volatility_threshold: float = 0.02
    ) -> Dict[str, Any]:
        """
        변동성 조정
        
        Args:
            base_portfolio: 기본 포트폴리오
            market_volatility: 시장 변동성
            volatility_threshold: 변동성 임계값
        
        Returns:
            변동성 조정 결과
        """
        try:
            adjusted_portfolio = base_portfolio.copy()
            
            # 고변동성 시장 조정
            if market_volatility > volatility_threshold:
                # 주식 비중 감소, 채권/현금 비중 증가
                stock_reduction = min(0.05, base_portfolio.get("stocks", 0) * 0.1)
                adjusted_portfolio["stocks"] = base_portfolio.get("stocks", 0) - stock_reduction
                adjusted_portfolio["bonds"] = base_portfolio.get("bonds", 0) + stock_reduction * 0.6
                adjusted_portfolio["cash"] = base_portfolio.get("cash", 0) + stock_reduction * 0.4
                
                adjustment_type = "보수적 조정"
                adjustment_reason = f"고변동성 시장({market_volatility:.1%})으로 인한 주식 비중 감소"
            else:
                # 정상 변동성 시장에서는 기본 포트폴리오 유지
                adjustment_type = "조정 없음"
                adjustment_reason = f"정상 변동성 시장({market_volatility:.1%})으로 기본 포트폴리오 유지"
            
            return {
                "status": "success",
                "message": "변동성 조정이 완료되었습니다.",
                "adjustment_result": {
                    "original_portfolio": base_portfolio,
                    "adjusted_portfolio": adjusted_portfolio,
                    "adjustment_type": adjustment_type,
                    "adjustment_reason": adjustment_reason,
                    "market_volatility": market_volatility,
                    "changes": {
                        "stocks_change": adjusted_portfolio.get("stocks", 0) - base_portfolio.get("stocks", 0),
                        "bonds_change": adjusted_portfolio.get("bonds", 0) - base_portfolio.get("bonds", 0),
                        "cash_change": adjusted_portfolio.get("cash", 0) - base_portfolio.get("cash", 0)
                    }
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"변동성 조정 중 오류 발생: {str(e)}"
            }
    
    async def create_implementation_plan(
        self,
        user_id: str,
        target_portfolio: Dict[str, float],
        current_assets: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        실행 계획 수립
        
        Args:
            user_id: 사용자 ID
            target_portfolio: 목표 포트폴리오
            current_assets: 현재 자산 현황
        
        Returns:
            실행 계획 수립 결과
        """
        try:
            # 사용자 프로필 로드
            profile_file = self.data_dir / f"{user_id}_profile.json"
            if not profile_file.exists():
                return {
                    "status": "error",
                    "message": "사용자 프로필을 찾을 수 없습니다."
                }
            
            with open(profile_file, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
            
            user_profile = UserProfile.from_dict(profile_data)
            
            # 현재 자산 현황 (기본값)
            if current_assets is None:
                current_assets = {
                    "stocks": user_profile.asset_portfolio.stocks,
                    "bonds": user_profile.asset_portfolio.bonds,
                    "cash": user_profile.asset_portfolio.cash_savings + user_profile.asset_portfolio.money_market_funds,
                    "alternatives": user_profile.asset_portfolio.other_assets
                }
            
            total_assets = sum(current_assets.values())
            
            # 목표 자산 금액 계산
            target_assets = {
                asset: total_assets * ratio 
                for asset, ratio in target_portfolio.items()
            }
            
            # 조정 필요 금액 계산
            rebalancing_needs = {
                asset: target_assets[asset] - current_assets.get(asset, 0)
                for asset in target_portfolio.keys()
            }
            
            # 실행 계획 생성
            implementation_steps = []
            
            # 1단계: 현금 확보
            if rebalancing_needs.get("cash", 0) < 0:
                implementation_steps.append({
                    "step": 1,
                    "action": "현금 확보",
                    "description": f"현금 {abs(rebalancing_needs['cash']):,.0f}원 확보 필요",
                    "priority": "high"
                })
            
            # 2단계: 주식 조정
            if rebalancing_needs.get("stocks", 0) != 0:
                action = "주식 매수" if rebalancing_needs["stocks"] > 0 else "주식 매도"
                implementation_steps.append({
                    "step": 2,
                    "action": action,
                    "description": f"주식 {abs(rebalancing_needs['stocks']):,.0f}원 조정",
                    "priority": "medium"
                })
            
            # 3단계: 채권 조정
            if rebalancing_needs.get("bonds", 0) != 0:
                action = "채권 매수" if rebalancing_needs["bonds"] > 0 else "채권 매도"
                implementation_steps.append({
                    "step": 3,
                    "action": action,
                    "description": f"채권 {abs(rebalancing_needs['bonds']):,.0f}원 조정",
                    "priority": "medium"
                })
            
            return {
                "status": "success",
                "message": "실행 계획이 수립되었습니다.",
                "implementation_plan": {
                    "current_assets": current_assets,
                    "target_portfolio": target_portfolio,
                    "target_assets": target_assets,
                    "rebalancing_needs": rebalancing_needs,
                    "implementation_steps": implementation_steps,
                    "total_investment": total_assets,
                    "rebalancing_cost": sum(abs(need) for need in rebalancing_needs.values()) * 0.001  # 0.1% 거래비용 가정
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"실행 계획 수립 중 오류 발생: {str(e)}"
            }
    
    async def monitor_performance(
        self,
        portfolio_returns: List[float],
        benchmark_returns: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        """
        성과 모니터링
        
        Args:
            portfolio_returns: 포트폴리오 수익률 리스트
            benchmark_returns: 벤치마크 수익률 리스트
        
        Returns:
            성과 모니터링 결과
        """
        try:
            if not portfolio_returns:
                return {
                    "status": "error",
                    "message": "포트폴리오 수익률 데이터가 없습니다."
                }
            
            # 포트폴리오 성과 지표 계산
            portfolio_metrics = self.portfolio_calc.calculate_portfolio_metrics(portfolio_returns)
            
            # 벤치마크 비교 (있는 경우)
            benchmark_comparison = None
            if benchmark_returns and len(benchmark_returns) == len(portfolio_returns):
                benchmark_metrics = self.portfolio_calc.calculate_portfolio_metrics(benchmark_returns)
                benchmark_comparison = {
                    "portfolio_return": portfolio_metrics["mean_return"],
                    "benchmark_return": benchmark_metrics["mean_return"],
                    "excess_return": portfolio_metrics["mean_return"] - benchmark_metrics["mean_return"],
                    "portfolio_volatility": portfolio_metrics["volatility"],
                    "benchmark_volatility": benchmark_metrics["volatility"],
                    "tracking_error": abs(portfolio_metrics["volatility"] - benchmark_metrics["volatility"])
                }
            
            # 성과 평가
            performance_rating = self._evaluate_performance(portfolio_metrics)
            
            return {
                "status": "success",
                "message": "성과 모니터링이 완료되었습니다.",
                "performance_analysis": {
                    "portfolio_metrics": portfolio_metrics,
                    "benchmark_comparison": benchmark_comparison,
                    "performance_rating": performance_rating,
                    "recommendations": self._get_performance_recommendations(portfolio_metrics)
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"성과 모니터링 중 오류 발생: {str(e)}"
            }
    
    def _evaluate_performance(self, metrics: Dict[str, float]) -> str:
        """성과 평가"""
        sharpe_ratio = metrics.get("sharpe_ratio", 0)
        max_drawdown = abs(metrics.get("max_drawdown", 0))
        
        if sharpe_ratio > 1.0 and max_drawdown < 0.1:
            return "우수"
        elif sharpe_ratio > 0.5 and max_drawdown < 0.2:
            return "양호"
        elif sharpe_ratio > 0 and max_drawdown < 0.3:
            return "보통"
        else:
            return "개선 필요"
    
    def _get_performance_recommendations(self, metrics: Dict[str, float]) -> List[str]:
        """성과 기반 권장사항"""
        recommendations = []
        
        if metrics.get("sharpe_ratio", 0) < 0.5:
            recommendations.append("샤프 비율이 낮습니다. 리스크 대비 수익률을 개선하세요.")
        
        if abs(metrics.get("max_drawdown", 0)) > 0.2:
            recommendations.append("최대 낙폭이 큽니다. 변동성을 줄이는 자산을 추가하세요.")
        
        if metrics.get("volatility", 0) > 0.2:
            recommendations.append("변동성이 높습니다. 안정 자산 비중을 늘리세요.")
        
        if not recommendations:
            recommendations.append("현재 포트폴리오 성과가 양호합니다. 정기적인 모니터링을 계속하세요.")
        
        return recommendations
