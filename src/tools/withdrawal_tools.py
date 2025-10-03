#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
인출메이트 도구 구현
"""

import json
import numpy as np
from datetime import datetime, date
from typing import Dict, Any, List, Optional
from pathlib import Path

from src.models.user_profile import UserProfile
from src.services.calculation_engine import WithdrawalCalculator, FinancialCalculator

class WithdrawalTools:
    """인출메이트 도구 클래스"""
    
    def __init__(self):
        self.withdrawal_calc = WithdrawalCalculator()
        self.financial_calc = FinancialCalculator()
        self.data_dir = Path("data/user_data")
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    async def analyze_retirement_assets(
        self,
        user_id: str,
        retirement_assets: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        은퇴 자산 구조 분석
        
        Args:
            user_id: 사용자 ID
            retirement_assets: 은퇴 자산 현황
        
        Returns:
            은퇴 자산 구조 분석 결과
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
            
            # 은퇴 자산 현황 (기본값 또는 입력값)
            if retirement_assets is None:
                retirement_assets = {
                    "liquid_assets": user_profile.asset_portfolio.total_liquid_assets,
                    "pension_assets": user_profile.asset_portfolio.total_pension_assets,
                    "real_estate": user_profile.asset_portfolio.total_real_estate,
                    "total_assets": user_profile.asset_portfolio.total_assets
                }
            
            # 자산 유형별 분류
            asset_analysis = {
                "liquid_assets": {
                    "amount": retirement_assets["liquid_assets"],
                    "percentage": retirement_assets["liquid_assets"] / retirement_assets["total_assets"] * 100,
                    "liquidity": "high",
                    "tax_treatment": "taxable"
                },
                "pension_assets": {
                    "amount": retirement_assets["pension_assets"],
                    "percentage": retirement_assets["pension_assets"] / retirement_assets["total_assets"] * 100,
                    "liquidity": "medium",
                    "tax_treatment": "tax_deferred"
                },
                "real_estate": {
                    "amount": retirement_assets["real_estate"],
                    "percentage": retirement_assets["real_estate"] / retirement_assets["total_assets"] * 100,
                    "liquidity": "low",
                    "tax_treatment": "capital_gains"
                }
            }
            
            # 자산 구조 평가
            liquidity_ratio = asset_analysis["liquid_assets"]["percentage"]
            diversification_score = self._calculate_diversification_score(asset_analysis)
            
            return {
                "status": "success",
                "message": "은퇴 자산 구조 분석이 완료되었습니다.",
                "asset_analysis": {
                    "total_assets": retirement_assets["total_assets"],
                    "asset_breakdown": asset_analysis,
                    "liquidity_ratio": liquidity_ratio,
                    "diversification_score": diversification_score,
                    "recommendations": self._get_asset_recommendations(asset_analysis, liquidity_ratio)
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"은퇴 자산 구조 분석 중 오류 발생: {str(e)}"
            }
    
    def _calculate_diversification_score(self, asset_analysis: Dict[str, Any]) -> float:
        """다각화 점수 계산"""
        percentages = [asset["percentage"] for asset in asset_analysis.values()]
        # 균등 분산일수록 높은 점수
        max_percentage = max(percentages)
        diversification_score = 100 - (max_percentage - 33.33) * 2
        return max(0, min(100, diversification_score))
    
    def _get_asset_recommendations(self, asset_analysis: Dict[str, Any], liquidity_ratio: float) -> List[str]:
        """자산 구조 기반 권장사항"""
        recommendations = []
        
        if liquidity_ratio < 20:
            recommendations.append("유동성 자산 비중이 낮습니다. 현금성 자산을 늘리세요.")
        elif liquidity_ratio > 50:
            recommendations.append("유동성 자산 비중이 높습니다. 수익률 개선을 위해 투자 자산을 늘리세요.")
        
        if asset_analysis["pension_assets"]["percentage"] < 10:
            recommendations.append("연금 자산 비중이 낮습니다. 세제 혜택을 위해 연금 계좌를 활용하세요.")
        
        if asset_analysis["real_estate"]["percentage"] > 70:
            recommendations.append("부동산 비중이 높습니다. 리스크 분산을 위해 다른 자산을 고려하세요.")
        
        return recommendations
    
    async def set_withdrawal_baseline(
        self,
        user_id: str,
        target_monthly_income: float,
        inflation_rate: float = 0.025,
        withdrawal_period: int = 30
    ) -> Dict[str, Any]:
        """
        인출 기본선 설정
        
        Args:
            user_id: 사용자 ID
            target_monthly_income: 목표 월 소득
            inflation_rate: 물가상승률
            withdrawal_period: 인출 기간
        
        Returns:
            인출 기본선 설정 결과
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
            
            # 연간 목표 소득
            target_annual_income = target_monthly_income * 12
            
            # 물가 연동 인출 계산
            real_withdrawal_schedule = []
            nominal_withdrawal_schedule = []
            
            for year in range(withdrawal_period):
                # 실질 인출액 (물가 반영)
                real_amount = target_annual_income
                # 명목 인출액 (물가상승률 반영)
                nominal_amount = target_annual_income * ((1 + inflation_rate) ** year)
                
                real_withdrawal_schedule.append({
                    "year": year + 1,
                    "real_amount": real_amount,
                    "nominal_amount": nominal_amount
                })
                nominal_withdrawal_schedule.append(nominal_amount)
            
            # 안전인출률 계산
            safe_withdrawal_rate = self.withdrawal_calc.calculate_safe_withdrawal_rate(
                portfolio_value=user_profile.asset_portfolio.total_assets,
                annual_expenses=target_annual_income,
                expected_return=0.04,  # 4% 예상 수익률
                inflation_rate=inflation_rate,
                years=withdrawal_period
            )
            
            return {
                "status": "success",
                "message": "인출 기본선이 설정되었습니다.",
                "withdrawal_baseline": {
                    "target_monthly_income": target_monthly_income,
                    "target_annual_income": target_annual_income,
                    "withdrawal_period": withdrawal_period,
                    "inflation_rate": inflation_rate,
                    "real_withdrawal_schedule": real_withdrawal_schedule,
                    "safe_withdrawal_rate": safe_withdrawal_rate,
                    "recommendations": [
                        "물가 연동 인출을 통해 구매력을 유지하세요.",
                        "안전인출률을 초과하지 않도록 주의하세요.",
                        "연 1회 인출 계획을 재검토하세요."
                    ]
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"인출 기본선 설정 중 오류 발생: {str(e)}"
            }
    
    async def manage_guardrail_system(
        self,
        current_portfolio_value: float,
        target_portfolio_value: float,
        current_withdrawal_rate: float,
        guardrail_threshold: float = 0.2
    ) -> Dict[str, Any]:
        """
        가드레일 시스템 관리
        
        Args:
            current_portfolio_value: 현재 포트폴리오 가치
            target_portfolio_value: 목표 포트폴리오 가치
            current_withdrawal_rate: 현재 인출률
            guardrail_threshold: 가드레일 임계값
        
        Returns:
            가드레일 시스템 관리 결과
        """
        try:
            # 포트폴리오 성과 계산
            portfolio_performance = (current_portfolio_value - target_portfolio_value) / target_portfolio_value
            
            # 가드레일 규칙 적용
            if portfolio_performance > guardrail_threshold:
                # 포트폴리오가 목표보다 20% 이상 좋음 → 인출률 증가
                adjustment_factor = 1.1
                action = "인출률 증가"
                reason = f"포트폴리오 성과가 목표 대비 {portfolio_performance*100:.1f}% 초과"
            elif portfolio_performance < -guardrail_threshold:
                # 포트폴리오가 목표보다 20% 이상 나쁨 → 인출률 감소
                adjustment_factor = 0.9
                action = "인출률 감소"
                reason = f"포트폴리오 성과가 목표 대비 {portfolio_performance*100:.1f}% 미달"
            else:
                # 정상 범위 → 인출률 유지
                adjustment_factor = 1.0
                action = "인출률 유지"
                reason = f"포트폴리오 성과가 정상 범위 ({portfolio_performance*100:.1f}%)"
            
            # 조정된 인출률 계산
            adjusted_withdrawal_rate = current_withdrawal_rate * adjustment_factor
            
            return {
                "status": "success",
                "message": "가드레일 시스템이 적용되었습니다.",
                "guardrail_result": {
                    "portfolio_performance": portfolio_performance,
                    "current_withdrawal_rate": current_withdrawal_rate,
                    "adjusted_withdrawal_rate": adjusted_withdrawal_rate,
                    "adjustment_factor": adjustment_factor,
                    "action": action,
                    "reason": reason,
                    "guardrail_status": "active" if abs(portfolio_performance) > guardrail_threshold else "normal"
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"가드레일 시스템 관리 중 오류 발생: {str(e)}"
            }
    
    async def optimize_withdrawal_sequence(
        self,
        user_id: str,
        annual_withdrawal_needed: float,
        tax_brackets: Optional[List[Dict[str, float]]] = None
    ) -> Dict[str, Any]:
        """
        인출 순서 최적화
        
        Args:
            user_id: 사용자 ID
            annual_withdrawal_needed: 연간 필요 인출액
            tax_brackets: 세율 구간 정보
        
        Returns:
            인출 순서 최적화 결과
        """
        try:
            # 기본 세율 구간 (2024년 기준)
            if tax_brackets is None:
                tax_brackets = [
                    {"min_income": 0, "max_income": 14000000, "rate": 0.06},
                    {"min_income": 14000000, "max_income": 50000000, "rate": 0.15},
                    {"min_income": 50000000, "max_income": 88000000, "rate": 0.24},
                    {"min_income": 88000000, "max_income": 150000000, "rate": 0.35},
                    {"min_income": 150000000, "max_income": float('inf'), "rate": 0.38}
                ]
            
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
            
            # 계좌별 인출 순서 최적화
            withdrawal_sequence = []
            remaining_withdrawal = annual_withdrawal_needed
            
            # 1단계: 확정소득 활용 (국민연금, 퇴직연금 등)
            guaranteed_income = user_profile.asset_portfolio.national_pension
            if guaranteed_income > 0 and remaining_withdrawal > 0:
                used_income = min(guaranteed_income, remaining_withdrawal)
                withdrawal_sequence.append({
                    "step": 1,
                    "account_type": "확정소득",
                    "amount": used_income,
                    "tax_rate": 0.0,
                    "after_tax_amount": used_income
                })
                remaining_withdrawal -= used_income
            
            # 2단계: 일반과세계좌 (저세율 구간까지)
            if remaining_withdrawal > 0:
                taxable_amount = min(remaining_withdrawal, 14000000)  # 1,400만원까지 6% 세율
                tax_amount = taxable_amount * 0.06
                withdrawal_sequence.append({
                    "step": 2,
                    "account_type": "일반과세계좌",
                    "amount": taxable_amount,
                    "tax_rate": 0.06,
                    "after_tax_amount": taxable_amount - tax_amount
                })
                remaining_withdrawal -= taxable_amount
            
            # 3단계: 연금계좌 (세제 혜택 활용)
            if remaining_withdrawal > 0:
                pension_amount = min(remaining_withdrawal, 12000000)  # 연금소득 1,200만원까지 세액공제
                tax_amount = pension_amount * 0.06  # 연금소득세
                withdrawal_sequence.append({
                    "step": 3,
                    "account_type": "연금계좌",
                    "amount": pension_amount,
                    "tax_rate": 0.06,
                    "after_tax_amount": pension_amount - tax_amount
                })
                remaining_withdrawal -= pension_amount
            
            # 총 세금 계산
            total_tax = sum(step["amount"] * step["tax_rate"] for step in withdrawal_sequence)
            total_after_tax = sum(step["after_tax_amount"] for step in withdrawal_sequence)
            
            return {
                "status": "success",
                "message": "인출 순서가 최적화되었습니다.",
                "withdrawal_optimization": {
                    "annual_withdrawal_needed": annual_withdrawal_needed,
                    "withdrawal_sequence": withdrawal_sequence,
                    "total_tax": total_tax,
                    "total_after_tax": total_after_tax,
                    "tax_efficiency": (total_after_tax / annual_withdrawal_needed) * 100,
                    "recommendations": [
                        "저세율 구간을 최대한 활용하세요.",
                        "연금계좌는 세제 혜택을 고려하여 활용하세요.",
                        "세율 급등을 방지하기 위해 소득을 평준화하세요."
                    ]
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"인출 순서 최적화 중 오류 발생: {str(e)}"
            }
    
    async def manage_bucket_strategy(
        self,
        total_portfolio: float,
        annual_expenses: float,
        bucket1_years: int = 2,
        bucket2_years: int = 3
    ) -> Dict[str, Any]:
        """
        3버킷 전략 관리
        
        Args:
            total_portfolio: 총 포트폴리오 가치
            annual_expenses: 연간 지출
            bucket1_years: 버킷1 커버 년수
            bucket2_years: 버킷2 커버 년수
        
        Returns:
            3버킷 전략 관리 결과
        """
        try:
            # 3버킷 전략 계산
            bucket_strategy = self.withdrawal_calc.calculate_bucket_strategy(
                total_portfolio=total_portfolio,
                annual_expenses=annual_expenses,
                years_to_cover=bucket1_years + bucket2_years
            )
            
            # 버킷별 상세 전략
            bucket_details = {
                "bucket1": {
                    "name": "현금 버킷",
                    "amount": bucket_strategy["bucket1_cash"],
                    "percentage": bucket_strategy["bucket1_ratio"] * 100,
                    "purpose": "생활비 2년분",
                    "assets": ["현금", "단기예금", "CMA", "MMF"],
                    "risk_level": "매우 낮음",
                    "expected_return": 0.03
                },
                "bucket2": {
                    "name": "중기 버킷",
                    "amount": bucket_strategy["bucket2_bonds"],
                    "percentage": bucket_strategy["bucket2_ratio"] * 100,
                    "purpose": "생활비 3년분",
                    "assets": ["중기채권", "배당주", "안정형 펀드"],
                    "risk_level": "낮음",
                    "expected_return": 0.05
                },
                "bucket3": {
                    "name": "성장 버킷",
                    "amount": bucket_strategy["bucket3_growth"],
                    "percentage": bucket_strategy["bucket3_ratio"] * 100,
                    "purpose": "장기 성장",
                    "assets": ["주식", "주식형 펀드", "ETF"],
                    "risk_level": "높음",
                    "expected_return": 0.08
                }
            }
            
            # 버킷 운영 전략
            operation_strategy = {
                "normal_market": "버킷1에서 인출, 버킷2,3에서 정기 리밸런싱",
                "bear_market": "버킷1,2에서 인출, 버킷3 매도 지연",
                "bull_market": "버킷3에서 수익 실현, 버킷1,2 보충",
                "rebalancing_frequency": "연 1회 또는 버킷1 소진 시"
            }
            
            return {
                "status": "success",
                "message": "3버킷 전략이 수립되었습니다.",
                "bucket_strategy": {
                    "total_portfolio": total_portfolio,
                    "annual_expenses": annual_expenses,
                    "bucket_details": bucket_details,
                    "operation_strategy": operation_strategy,
                    "expected_portfolio_return": sum(
                        bucket["expected_return"] * bucket["percentage"] / 100 
                        for bucket in bucket_details.values()
                    ),
                    "recommendations": [
                        "버킷1이 소진되기 전에 미리 보충하세요.",
                        "시장 상황에 따라 버킷 간 자금 이동을 조절하세요.",
                        "정기적인 리밸런싱을 통해 목표 비중을 유지하세요."
                    ]
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"3버킷 전략 관리 중 오류 발생: {str(e)}"
            }
    
    async def create_execution_plan(
        self,
        user_id: str,
        withdrawal_strategy: Dict[str, Any],
        automation_level: str = "semi_auto"
    ) -> Dict[str, Any]:
        """
        실행 계획 생성
        
        Args:
            user_id: 사용자 ID
            withdrawal_strategy: 인출 전략
            automation_level: 자동화 수준
        
        Returns:
            실행 계획 생성 결과
        """
        try:
            # 월별 인출 계획 생성
            monthly_plan = []
            for month in range(1, 13):
                monthly_plan.append({
                    "month": month,
                    "withdrawal_amount": withdrawal_strategy.get("monthly_withdrawal", 0),
                    "source_accounts": withdrawal_strategy.get("source_accounts", []),
                    "tax_withholding": withdrawal_strategy.get("tax_withholding", 0),
                    "net_amount": withdrawal_strategy.get("net_amount", 0)
                })
            
            # 자동화 설정
            automation_config = {
                "semi_auto": {
                    "auto_transfer": True,
                    "auto_tax_calculation": True,
                    "manual_approval": True,
                    "notification": True
                },
                "full_auto": {
                    "auto_transfer": True,
                    "auto_tax_calculation": True,
                    "manual_approval": False,
                    "notification": True
                },
                "manual": {
                    "auto_transfer": False,
                    "auto_tax_calculation": False,
                    "manual_approval": True,
                    "notification": True
                }
            }
            
            # 체크리스트 생성
            checklist = [
                "월별 인출액 확인",
                "세금 계산 및 원천징수",
                "계좌 잔액 확인",
                "리밸런싱 필요성 검토",
                "가드레일 규칙 적용 확인"
            ]
            
            return {
                "status": "success",
                "message": "실행 계획이 생성되었습니다.",
                "execution_plan": {
                    "monthly_plan": monthly_plan,
                    "automation_config": automation_config.get(automation_level, automation_config["semi_auto"]),
                    "checklist": checklist,
                    "monitoring_schedule": {
                        "daily": ["계좌 잔액 확인"],
                        "monthly": ["인출 실행", "세금 계산"],
                        "quarterly": ["성과 검토", "전략 조정"],
                        "annually": ["전체 재검토", "목표 수정"]
                    }
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"실행 계획 생성 중 오류 발생: {str(e)}"
            }
    
    async def compare_scenarios(
        self,
        base_scenario: Dict[str, Any],
        alternative_scenarios: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        시나리오 비교
        
        Args:
            base_scenario: 기본 시나리오
            alternative_scenarios: 대안 시나리오들
        
        Returns:
            시나리오 비교 결과
        """
        try:
            comparison_results = []
            
            # 기본 시나리오 분석
            base_analysis = self._analyze_scenario(base_scenario)
            comparison_results.append({
                "scenario_name": "기본 시나리오",
                "analysis": base_analysis
            })
            
            # 대안 시나리오들 분석
            for i, scenario in enumerate(alternative_scenarios):
                scenario_analysis = self._analyze_scenario(scenario)
                comparison_results.append({
                    "scenario_name": f"대안 {i+1}",
                    "analysis": scenario_analysis
                })
            
            # 시나리오별 비교 요약
            comparison_summary = {
                "best_return": max(comparison_results, key=lambda x: x["analysis"]["expected_return"]),
                "lowest_risk": min(comparison_results, key=lambda x: x["analysis"]["risk_level"]),
                "most_tax_efficient": max(comparison_results, key=lambda x: x["analysis"]["tax_efficiency"])
            }
            
            return {
                "status": "success",
                "message": "시나리오 비교가 완료되었습니다.",
                "comparison_results": {
                    "scenarios": comparison_results,
                    "summary": comparison_summary,
                    "recommendations": self._get_scenario_recommendations(comparison_results)
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"시나리오 비교 중 오류 발생: {str(e)}"
            }
    
    def _analyze_scenario(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """시나리오 분석"""
        return {
            "expected_return": scenario.get("expected_return", 0.05),
            "risk_level": scenario.get("risk_level", "medium"),
            "tax_efficiency": scenario.get("tax_efficiency", 0.8),
            "liquidity": scenario.get("liquidity", "medium"),
            "complexity": scenario.get("complexity", "medium")
        }
    
    def _get_scenario_recommendations(self, comparison_results: List[Dict[str, Any]]) -> List[str]:
        """시나리오 비교 기반 권장사항"""
        recommendations = []
        
        # 최고 수익률 시나리오
        best_return = max(comparison_results, key=lambda x: x["analysis"]["expected_return"])
        recommendations.append(f"최고 수익률: {best_return['scenario_name']}")
        
        # 최저 리스크 시나리오
        lowest_risk = min(comparison_results, key=lambda x: x["analysis"]["risk_level"])
        recommendations.append(f"최저 리스크: {lowest_risk['scenario_name']}")
        
        # 세금 효율성
        most_tax_efficient = max(comparison_results, key=lambda x: x["analysis"]["tax_efficiency"])
        recommendations.append(f"세금 효율성: {most_tax_efficient['scenario_name']}")
        
        return recommendations
