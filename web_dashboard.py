#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
은퇴 설계 AI 에이전트 웹 대시보드
"""

import streamlit as st
import asyncio
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.servers.accumulation_server import AccumulationServer
from src.servers.investment_server import InvestmentServer
from src.servers.withdrawal_server import WithdrawalServer
from src.servers.data_server import DataServer
from src.servers.external_api_server import ExternalAPIServer

# 페이지 설정
st.set_page_config(
    page_title="은퇴 설계 AI 에이전트",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
    .warning-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ffeaa7;
    }
</style>
""", unsafe_allow_html=True)

class RetirementDashboard:
    """은퇴 설계 대시보드"""
    
    def __init__(self):
        self.accumulation_server = AccumulationServer()
        self.investment_server = InvestmentServer()
        self.withdrawal_server = WithdrawalServer()
        self.data_server = DataServer()
        self.external_api_server = ExternalAPIServer()
        
    async def initialize_servers(self):
        """서버들 초기화"""
        await self.accumulation_server.start()
        await self.investment_server.start()
        await self.withdrawal_server.start()
        await self.data_server.start()
        await self.external_api_server.start()
    
    async def cleanup_servers(self):
        """서버들 정리"""
        await self.accumulation_server.stop()
        await self.investment_server.stop()
        await self.withdrawal_server.stop()
        await self.data_server.stop()
        await self.external_api_server.stop()
    
    def render_header(self):
        """헤더 렌더링"""
        st.markdown('<div class="main-header">🏦 은퇴 설계 AI 에이전트</div>', unsafe_allow_html=True)
        st.markdown("---")
    
    def render_sidebar(self):
        """사이드바 렌더링"""
        st.sidebar.title("📊 메뉴")
        
        menu = st.sidebar.selectbox(
            "선택하세요",
            ["🏠 대시보드", "💰 적립메이트", "📈 투자메이트", "💸 인출메이트", "🔧 데이터 관리", "🌐 시장 정보"]
        )
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 👤 사용자 정보")
        
        # 사용자 ID 입력
        user_id = st.sidebar.text_input("사용자 ID", value="user_001")
        
        return menu, user_id
    
    def render_dashboard(self, user_id):
        """메인 대시보드"""
        st.header("📊 은퇴 설계 대시보드")
        
        # 메트릭 카드들
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="목표 은퇴 자산",
                value="7억 5천만원",
                delta="목표 달성률: 85%"
            )
        
        with col2:
            st.metric(
                label="현재 투자 수익률",
                value="6.7%",
                delta="연간"
            )
        
        with col3:
            st.metric(
                label="예상 월 인출액",
                value="400만원",
                delta="물가 연동"
            )
        
        with col4:
            st.metric(
                label="포트폴리오 리스크",
                value="중간",
                delta="샤프 비율: -1.33"
            )
        
        st.markdown("---")
        
        # 차트 섹션
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 자산 배분 현황")
            
            # 자산 배분 파이 차트
            asset_data = {
                '주식': 40,
                '채권': 35,
                '현금': 15,
                '대체투자': 10
            }
            
            fig = px.pie(
                values=list(asset_data.values()),
                names=list(asset_data.keys()),
                title="포트폴리오 자산 배분"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📊 연도별 자산 성장")
            
            # 자산 성장 라인 차트
            years = list(range(2024, 2050))
            assets = [500000000]  # 5억 시작
            
            for i in range(1, len(years)):
                growth_rate = 0.067  # 6.7% 성장률
                new_asset = assets[-1] * (1 + growth_rate)
                assets.append(new_asset)
            
            fig = px.line(
                x=years,
                y=assets,
                title="예상 자산 성장",
                labels={'x': '연도', 'y': '자산 (원)'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # 최근 활동
        st.subheader("📋 최근 활동")
        
        activities = [
            {"date": "2024-10-03", "action": "포트폴리오 리밸런싱", "status": "완료"},
            {"date": "2024-10-02", "action": "경제 가정 업데이트", "status": "완료"},
            {"date": "2024-10-01", "action": "월간 성과 검토", "status": "완료"},
            {"date": "2024-09-30", "action": "자산 배분 조정", "status": "완료"}
        ]
        
        for activity in activities:
            st.write(f"📅 {activity['date']} - {activity['action']} ({activity['status']})")
    
    def render_accumulation_mate(self, user_id):
        """적립메이트 페이지"""
        st.header("💰 적립메이트 - 은퇴 전 자산 적립")
        
        # 사용자 프로필 입력
        st.subheader("👤 사용자 프로필")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("나이", min_value=20, max_value=70, value=35)
            income = st.number_input("연봉 (원)", min_value=0, value=80000000, step=1000000)
            current_assets = st.number_input("현재 자산 (원)", min_value=0, value=500000000, step=10000000)
        
        with col2:
            retirement_age = st.number_input("은퇴 예정 나이", min_value=50, max_value=80, value=65)
            target_assets = st.number_input("목표 은퇴 자산 (원)", min_value=0, value=750000000, step=10000000)
            risk_tolerance = st.selectbox("리스크 성향", ["보수적", "중립적", "공격적"])
        
        if st.button("📊 적립 계획 분석"):
            with st.spinner("적립 계획을 분석하고 있습니다..."):
                # 적립메이트 서버 호출
                result = asyncio.run(self.accumulation_server.collect_user_profile(
                    user_id=user_id,
                    age=age,
                    income=income,
                    current_assets=current_assets,
                    retirement_age=retirement_age,
                    target_assets=target_assets,
                    risk_tolerance=risk_tolerance
                ))
                
                if result['status'] == 'success':
                    st.success("✅ 적립 계획 분석이 완료되었습니다!")
                    
                    # 결과 표시
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("목표 달성률", f"{result['data']['achievement_rate']:.1f}%")
                    
                    with col2:
                        st.metric("필요 월 저축액", f"{result['data']['required_monthly_savings']:,.0f}원")
                    
                    with col3:
                        st.metric("예상 은퇴 자산", f"{result['data']['projected_retirement_assets']:,.0f}원")
                    
                    # 상세 분석
                    st.subheader("📈 상세 분석")
                    
                    analysis_data = result['data']['analysis']
                    
                    st.write(f"**자금 격차**: {analysis_data['funding_gap']:,.0f}원")
                    st.write(f"**저축 기간**: {analysis_data['savings_period']}년")
                    st.write(f"**연간 저축률**: {analysis_data['annual_savings_rate']:.1f}%")
                    
                    # 권장사항
                    st.subheader("💡 권장사항")
                    for recommendation in analysis_data['recommendations']:
                        st.write(f"• {recommendation}")
                else:
                    st.error(f"❌ 분석 실패: {result['message']}")
    
    def render_investment_mate(self, user_id):
        """투자메이트 페이지"""
        st.header("📈 투자메이트 - 은퇴 자산 투자 전략")
        
        # 리스크 프로파일 평가
        st.subheader("🎯 리스크 프로파일 평가")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("나이", min_value=20, max_value=70, value=35, key="inv_age")
            income = st.number_input("연봉 (원)", min_value=0, value=80000000, step=1000000, key="inv_income")
            assets = st.number_input("현재 자산 (원)", min_value=0, value=500000000, step=10000000, key="inv_assets")
        
        with col2:
            investment_experience = st.selectbox("투자 경험", ["초보", "중급", "고급"], key="inv_exp")
            risk_tolerance = st.selectbox("리스크 성향", ["보수적", "중립적", "공격적"], key="inv_risk")
            time_horizon = st.number_input("투자 기간 (년)", min_value=1, max_value=50, value=30, key="inv_time")
        
        if st.button("📊 투자 전략 수립"):
            with st.spinner("투자 전략을 수립하고 있습니다..."):
                # 투자메이트 서버 호출
                result = asyncio.run(self.investment_server.evaluate_risk_profile(
                    user_id=user_id,
                    age=age,
                    income=income,
                    assets=assets,
                    investment_experience=investment_experience,
                    risk_tolerance=risk_tolerance,
                    time_horizon=time_horizon
                ))
                
                if result['status'] == 'success':
                    st.success("✅ 투자 전략이 수립되었습니다!")
                    
                    # 리스크 점수 표시
                    risk_score = result['data']['risk_score']
                    st.metric("리스크 점수", f"{risk_score:.1f}/100")
                    
                    # 포트폴리오 추천
                    st.subheader("💼 추천 포트폴리오")
                    
                    portfolio = result['data']['recommended_portfolio']
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("주식 비중", f"{portfolio['stocks']:.1f}%")
                    
                    with col2:
                        st.metric("채권 비중", f"{portfolio['bonds']:.1f}%")
                    
                    with col3:
                        st.metric("현금 비중", f"{portfolio['cash']:.1f}%")
                    
                    # 예상 수익률
                    st.subheader("📊 예상 성과")
                    
                    performance = result['data']['expected_performance']
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("예상 수익률", f"{performance['expected_return']:.1f}%")
                    
                    with col2:
                        st.metric("예상 변동성", f"{performance['volatility']:.1f}%")
                    
                    with col3:
                        st.metric("샤프 비율", f"{performance['sharpe_ratio']:.2f}")
                else:
                    st.error(f"❌ 전략 수립 실패: {result['message']}")
    
    def render_withdrawal_mate(self, user_id):
        """인출메이트 페이지"""
        st.header("💸 인출메이트 - 은퇴 후 절세 인출")
        
        # 은퇴 자산 정보
        st.subheader("🏦 은퇴 자산 정보")
        
        col1, col2 = st.columns(2)
        
        with col1:
            total_assets = st.number_input("총 은퇴 자산 (원)", min_value=0, value=750000000, step=10000000, key="with_assets")
            monthly_income_needed = st.number_input("필요 월 소득 (원)", min_value=0, value=4000000, step=100000, key="with_income")
            retirement_years = st.number_input("은퇴 기간 (년)", min_value=1, max_value=50, value=25, key="with_years")
        
        with col2:
            inflation_rate = st.number_input("예상 인플레이션률 (%)", min_value=0.0, max_value=10.0, value=2.8, step=0.1, key="with_inflation")
            tax_rate = st.number_input("예상 세율 (%)", min_value=0.0, max_value=50.0, value=20.0, step=1.0, key="with_tax")
            risk_tolerance = st.selectbox("리스크 성향", ["보수적", "중립적", "공격적"], key="with_risk")
        
        if st.button("📊 인출 전략 수립"):
            with st.spinner("인출 전략을 수립하고 있습니다..."):
                # 인출메이트 서버 호출
                result = asyncio.run(self.withdrawal_server.analyze_retirement_assets(
                    user_id=user_id,
                    total_assets=total_assets,
                    monthly_income_needed=monthly_income_needed,
                    retirement_years=retirement_years,
                    inflation_rate=inflation_rate,
                    tax_rate=tax_rate,
                    risk_tolerance=risk_tolerance
                ))
                
                if result['status'] == 'success':
                    st.success("✅ 인출 전략이 수립되었습니다!")
                    
                    # 안전 인출률
                    safe_withdrawal_rate = result['data']['safe_withdrawal_rate']
                    st.metric("안전 인출률", f"{safe_withdrawal_rate:.2f}%")
                    
                    # 3버킷 전략
                    st.subheader("🪣 3버킷 전략")
                    
                    buckets = result['data']['three_bucket_strategy']
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("현금 버킷", f"{buckets['cash_bucket']:,.0f}원")
                    
                    with col2:
                        st.metric("중기 버킷", f"{buckets['intermediate_bucket']:,.0f}원")
                    
                    with col3:
                        st.metric("성장 버킷", f"{buckets['growth_bucket']:,.0f}원")
                    
                    # 인출 순서
                    st.subheader("📋 인출 순서")
                    
                    withdrawal_order = result['data']['withdrawal_order']
                    
                    for i, account in enumerate(withdrawal_order, 1):
                        st.write(f"{i}. {account['account_type']} - {account['amount']:,.0f}원 ({account['tax_efficiency']:.1f}% 세금 효율성)")
                else:
                    st.error(f"❌ 전략 수립 실패: {result['message']}")
    
    def render_data_management(self, user_id):
        """데이터 관리 페이지"""
        st.header("🔧 데이터 관리")
        
        # 백업 관리
        st.subheader("💾 백업 관리")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📦 데이터 백업"):
                with st.spinner("데이터를 백업하고 있습니다..."):
                    result = asyncio.run(self.data_server.backup_user_data(
                        user_id=user_id,
                        backup_type="full"
                    ))
                    
                    if result['status'] == 'success':
                        st.success(f"✅ 백업 완료: {result['backup_id']}")
                        st.write(f"파일 크기: {result['file_size']:,} bytes")
                    else:
                        st.error(f"❌ 백업 실패: {result['message']}")
        
        with col2:
            if st.button("📋 백업 목록 조회"):
                with st.spinner("백업 목록을 조회하고 있습니다..."):
                    result = asyncio.run(self.data_server.list_backups(user_id=user_id))
                    
                    if result['status'] == 'success':
                        st.success(f"✅ 백업 목록 조회 완료 ({len(result['backups'])}개)")
                        
                        for backup in result['backups']:
                            st.write(f"📅 {backup['created_at']} - {backup['backup_id']} ({backup['file_size']:,} bytes)")
                    else:
                        st.error(f"❌ 조회 실패: {result['message']}")
        
        # 데이터 암호화
        st.subheader("🔐 데이터 보안")
        
        if st.button("🔒 민감 데이터 암호화"):
            sample_data = {
                "name": "홍길동",
                "ssn": "123456-1234567",
                "phone": "010-1234-5678",
                "email": "hong@example.com"
            }
            
            with st.spinner("데이터를 암호화하고 있습니다..."):
                result = asyncio.run(self.data_server.encrypt_sensitive_data(
                    data=sample_data,
                    user_id=user_id
                ))
                
                if result['status'] == 'success':
                    st.success("✅ 데이터 암호화 완료")
                    st.write("암호화된 데이터:")
                    st.json(result['encrypted_data'])
                else:
                    st.error(f"❌ 암호화 실패: {result['message']}")
    
    def render_market_info(self, user_id):
        """시장 정보 페이지"""
        st.header("🌐 시장 정보")
        
        # 시장 데이터
        st.subheader("📈 시장 현황")
        
        if st.button("📊 시장 데이터 수집"):
            with st.spinner("시장 데이터를 수집하고 있습니다..."):
                result = asyncio.run(self.external_api_server.fetch_market_data(
                    symbols=["^GSPC", "QQQ", "SPY"],
                    period="1mo"
                ))
                
                if result['status'] == 'success':
                    st.success("✅ 시장 데이터 수집 완료")
                    
                    # 시장 데이터 표시
                    market_data = result['data']
                    
                    for symbol, data in market_data.items():
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric(f"{symbol} 현재가", f"${data['current_price']:,.2f}")
                        
                        with col2:
                            st.metric("변동률", f"{data['change_percent']:.2f}%")
                        
                        with col3:
                            st.metric("거래량", f"{data['volume']:,}")
                        
                        with col4:
                            st.metric("52주 고점", f"${data['high_52w']:,.2f}")
                else:
                    st.error(f"❌ 데이터 수집 실패: {result['message']}")
        
        # 경제 지표
        st.subheader("📊 경제 지표")
        
        if st.button("📈 경제 지표 수집"):
            with st.spinner("경제 지표를 수집하고 있습니다..."):
                result = asyncio.run(self.external_api_server.fetch_economic_indicators(country="US"))
                
                if result['status'] == 'success':
                    st.success("✅ 경제 지표 수집 완료")
                    
                    # 경제 지표 표시
                    economic_data = result['data']
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("GDP 성장률", f"{economic_data['GDP']['value']:.1f}%")
                    
                    with col2:
                        st.metric("인플레이션", f"{economic_data['Inflation']['value']:.1f}%")
                    
                    with col3:
                        st.metric("실업률", f"{economic_data['Unemployment']['value']:.1f}%")
                    
                    with col4:
                        st.metric("기준금리", f"{economic_data['Interest_Rate']['value']:.2f}%")
                else:
                    st.error(f"❌ 지표 수집 실패: {result['message']}")
    
    def run(self):
        """대시보드 실행"""
        # 헤더 렌더링
        self.render_header()
        
        # 사이드바 렌더링
        menu, user_id = self.render_sidebar()
        
        # 서버 초기화
        asyncio.run(self.initialize_servers())
        
        try:
            # 메뉴에 따른 페이지 렌더링
            if menu == "🏠 대시보드":
                self.render_dashboard(user_id)
            elif menu == "💰 적립메이트":
                self.render_accumulation_mate(user_id)
            elif menu == "📈 투자메이트":
                self.render_investment_mate(user_id)
            elif menu == "💸 인출메이트":
                self.render_withdrawal_mate(user_id)
            elif menu == "🔧 데이터 관리":
                self.render_data_management(user_id)
            elif menu == "🌐 시장 정보":
                self.render_market_info(user_id)
        
        finally:
            # 서버 정리
            asyncio.run(self.cleanup_servers())

def main():
    """메인 함수"""
    dashboard = RetirementDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()
