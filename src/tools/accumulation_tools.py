#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
적립메이트 도구 구현
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

from src.models.user_profile import UserProfile, PersonalInfo, IncomeStructure, ExpenseStructure, AssetPortfolio, DebtStructure, InvestmentPreferences
from src.models.retirement_plan import RetirementPlan, EconomicAssumptions, RetirementGoal, AssetProjection, PortfolioAllocation, WithdrawalStrategy, ScenarioType
from src.services.calculation_engine import RetirementCalculator, FinancialCalculator

class AccumulationTools:
    """적립메이트 도구 클래스"""
    
    def __init__(self):
        self.calculator = RetirementCalculator()
        self.financial_calc = FinancialCalculator()
        self.data_dir = Path("data/user_data")
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    async def collect_user_profile(
        self,
        personal_info: Dict[str, Any],
        income_info: Dict[str, Any],
        expense_info: Dict[str, Any],
        asset_info: Dict[str, Any],
        debt_info: Dict[str, Any],
        investment_preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        사용자 프로필 수집 및 저장
        
        Args:
            personal_info: 개인 정보
            income_info: 소득 정보
            expense_info: 지출 정보
            asset_info: 자산 정보
            debt_info: 부채 정보
            investment_preferences: 투자 성향
        
        Returns:
            수집 결과
        """
        try:
            # 사용자 프로필 생성
            user_profile = UserProfile(
                user_id=personal_info.get('user_id', f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"),
                personal_info=PersonalInfo(**personal_info),
                income_structure=IncomeStructure(**income_info),
                expense_structure=ExpenseStructure(**expense_info),
                asset_portfolio=AssetPortfolio(**asset_info),
                debt_structure=DebtStructure(**debt_info),
                investment_preferences=InvestmentPreferences(**investment_preferences)
            )
            
            # 파일로 저장
            profile_file = self.data_dir / f"{user_profile.user_id}_profile.json"
            with open(profile_file, 'w', encoding='utf-8') as f:
                json.dump(user_profile.to_dict(), f, ensure_ascii=False, indent=2, default=str)
            
            return {
                "status": "success",
                "message": "사용자 프로필이 성공적으로 수집되었습니다.",
                "user_id": user_profile.user_id,
                "profile_summary": {
                    "current_age": user_profile.personal_info.current_age,
                    "target_retirement_age": user_profile.personal_info.target_retirement_age,
                    "total_assets": user_profile.asset_portfolio.total_assets,
                    "total_debt": user_profile.debt_structure.total_debt,
                    "net_worth": user_profile.asset_portfolio.total_assets - user_profile.debt_structure.total_debt
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"사용자 프로필 수집 중 오류 발생: {str(e)}"
            }
    
    async def set_economic_assumptions(
        self,
        scenario_type: str = "moderate",
        custom_assumptions: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        경제 가정 설정
        
        Args:
            scenario_type: 시나리오 타입 (conservative, moderate, aggressive)
            custom_assumptions: 사용자 정의 가정값
        
        Returns:
            경제 가정 설정 결과
        """
        try:
            # 기본 시나리오 설정
            scenarios = {
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
            
            # 사용자 정의 가정값이 있으면 적용
            if custom_assumptions:
                base_scenario = scenarios.get(scenario_type, scenarios["moderate"])
                base_scenario.update(custom_assumptions)
                assumptions = base_scenario
            else:
                assumptions = scenarios.get(scenario_type, scenarios["moderate"])
            
            # 경제 가정 객체 생성
            economic_assumptions = EconomicAssumptions(
                scenario_type=ScenarioType(scenario_type),
                inflation_rate=assumptions["inflation_rate"],
                pre_retirement_return=assumptions["pre_retirement_return"],
                post_retirement_return=assumptions["post_retirement_return"],
                wage_growth_rate=assumptions["wage_growth_rate"]
            )
            
            # 파일로 저장
            assumptions_file = self.data_dir / f"economic_assumptions_{scenario_type}.json"
            with open(assumptions_file, 'w', encoding='utf-8') as f:
                json.dump(economic_assumptions.dict(), f, ensure_ascii=False, indent=2, default=str)
            
            return {
                "status": "success",
                "message": f"{scenario_type} 시나리오 경제 가정이 설정되었습니다.",
                "assumptions": assumptions
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"경제 가정 설정 중 오류 발생: {str(e)}"
            }
    
    async def calculate_retirement_goal(
        self,
        user_id: str,
        target_monthly_income: float,
        retirement_period: int = 30,
        medical_reserve: float = 0
    ) -> Dict[str, Any]:
        """
        은퇴 목표 자금 계산
        
        Args:
            user_id: 사용자 ID
            target_monthly_income: 목표 월 소득
            retirement_period: 은퇴 기간
            medical_reserve: 의료비 예비금
        
        Returns:
            은퇴 목표 계산 결과
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
            
            # 경제 가정 로드 (기본값 사용)
            assumptions_file = self.data_dir / "economic_assumptions_moderate.json"
            if assumptions_file.exists():
                with open(assumptions_file, 'r', encoding='utf-8') as f:
                    assumptions_data = json.load(f)
            else:
                # 기본 가정값 사용
                assumptions_data = {
                    "inflation_rate": 0.025,
                    "post_retirement_return": 0.025
                }
            
            # 은퇴 목표 계산
            years_to_retirement = user_profile.personal_info.target_retirement_age - user_profile.personal_info.current_age
            annual_income_needed = target_monthly_income * 12
            
            result = self.calculator.calculate_retirement_goal(
                annual_income_needed=annual_income_needed,
                inflation_rate=assumptions_data["inflation_rate"],
                years_to_retirement=years_to_retirement,
                retirement_period=retirement_period,
                post_retirement_return=assumptions_data["post_retirement_return"]
            )
            
            # 의료비 예비금 추가
            total_required = result["recommended_capital"] + medical_reserve
            
            return {
                "status": "success",
                "message": "은퇴 목표 자금이 계산되었습니다.",
                "calculation_result": {
                    "target_monthly_income": target_monthly_income,
                    "target_annual_income": annual_income_needed,
                    "years_to_retirement": years_to_retirement,
                    "retirement_period": retirement_period,
                    "required_capital": total_required,
                    "medical_reserve": medical_reserve,
                    "swr_required": result["swr_required_capital"],
                    "pv_required": result["pv_required_capital"]
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"은퇴 목표 계산 중 오류 발생: {str(e)}"
            }
    
    async def project_asset_values(
        self,
        user_id: str,
        annual_contribution: float,
        contribution_growth_rate: float = 0.03
    ) -> Dict[str, Any]:
        """
        자산 미래가치 계산
        
        Args:
            user_id: 사용자 ID
            annual_contribution: 연간 저축액
            contribution_growth_rate: 저축액 증가율
        
        Returns:
            자산 프로젝션 결과
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
            
            # 경제 가정 로드
            assumptions_file = self.data_dir / "economic_assumptions_moderate.json"
            if assumptions_file.exists():
                with open(assumptions_file, 'r', encoding='utf-8') as f:
                    assumptions_data = json.load(f)
            else:
                assumptions_data = {"pre_retirement_return": 0.040}
            
            # 자산 프로젝션 계산
            years_to_retirement = user_profile.personal_info.target_retirement_age - user_profile.personal_info.current_age
            
            result = self.calculator.project_retirement_assets(
                current_assets=user_profile.asset_portfolio.total_assets,
                annual_contribution=annual_contribution,
                years_to_retirement=years_to_retirement,
                expected_return=assumptions_data["pre_retirement_return"],
                contribution_growth_rate=contribution_growth_rate
            )
            
            return {
                "status": "success",
                "message": "자산 미래가치가 계산되었습니다.",
                "projection_result": {
                    "current_assets": user_profile.asset_portfolio.total_assets,
                    "years_to_retirement": years_to_retirement,
                    "annual_contribution": annual_contribution,
                    "expected_return": assumptions_data["pre_retirement_return"],
                    "current_assets_fv": result["current_assets_fv"],
                    "contributions_fv": result["contributions_fv"],
                    "total_projected_assets": result["total_projected_assets"]
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"자산 프로젝션 계산 중 오류 발생: {str(e)}"
            }
    
    async def analyze_funding_gap(
        self,
        user_id: str,
        required_capital: float,
        projected_assets: float
    ) -> Dict[str, Any]:
        """
        자금 격차 분석
        
        Args:
            user_id: 사용자 ID
            required_capital: 필요 자본
            projected_assets: 예상 자산
        
        Returns:
            자금 격차 분석 결과
        """
        try:
            result = self.calculator.calculate_funding_gap(
                required_capital=required_capital,
                projected_assets=projected_assets
            )
            
            # 분석 결과에 추가 정보 포함
            analysis = {
                "funding_gap": result["funding_gap"],
                "gap_percentage": result["gap_percentage"],
                "is_sufficient": result["is_sufficient"],
                "shortfall": result["shortfall"],
                "required_capital": required_capital,
                "projected_assets": projected_assets
            }
            
            # 권장사항 생성
            recommendations = []
            if not result["is_sufficient"]:
                recommendations.extend([
                    "목표 은퇴 연령을 1-2년 늦추는 것을 고려해보세요.",
                    "월 저축액을 늘리는 방안을 검토해보세요.",
                    "세제 혜택 계좌(연금저축, IRP)를 최대한 활용하세요.",
                    "고금리 부채를 우선 상환하세요."
                ])
            else:
                recommendations.append("현재 계획으로 목표 달성이 가능합니다.")
            
            return {
                "status": "success",
                "message": "자금 격차 분석이 완료되었습니다.",
                "analysis": analysis,
                "recommendations": recommendations
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"자금 격차 분석 중 오류 발생: {str(e)}"
            }
    
    async def optimize_savings_plan(
        self,
        user_id: str,
        target_contribution: float,
        current_contribution: float
    ) -> Dict[str, Any]:
        """
        저축 계획 최적화
        
        Args:
            user_id: 사용자 ID
            target_contribution: 목표 저축액
            current_contribution: 현재 저축액
        
        Returns:
            저축 계획 최적화 결과
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
            
            # 추가 필요 저축액 계산
            additional_contribution = target_contribution - current_contribution
            
            # 계좌별 최적 배분 제안
            account_allocation = {
                "연금저축": min(additional_contribution * 0.4, 7000000),  # 연간 한도
                "IRP": min(additional_contribution * 0.3, 3000000),  # 연간 한도
                "일반계좌": max(0, additional_contribution - 10000000)  # 나머지
            }
            
            # 월별 저축 계획
            monthly_plan = {
                "현재_월저축": current_contribution / 12,
                "목표_월저축": target_contribution / 12,
                "추가_월저축": additional_contribution / 12,
                "계좌별_월저축": {
                    "연금저축": account_allocation["연금저축"] / 12,
                    "IRP": account_allocation["IRP"] / 12,
                    "일반계좌": account_allocation["일반계좌"] / 12
                }
            }
            
            return {
                "status": "success",
                "message": "저축 계획이 최적화되었습니다.",
                "optimization_result": {
                    "current_annual_contribution": current_contribution,
                    "target_annual_contribution": target_contribution,
                    "additional_contribution_needed": additional_contribution,
                    "account_allocation": account_allocation,
                    "monthly_plan": monthly_plan
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"저축 계획 최적화 중 오류 발생: {str(e)}"
            }
