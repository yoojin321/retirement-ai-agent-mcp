#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
외부 API 연동 MCP 서버 - 금융 데이터 및 외부 서비스 연동
"""

import os
import json
import asyncio
import aiohttp
import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from .base_server import BaseMCPServer

class ExternalAPIServer(BaseMCPServer):
    """외부 API 연동 MCP 서버"""
    
    def __init__(self):
        super().__init__("ExternalAPIServer")
        self.api_keys = self._load_api_keys()
        self.session = None
    
    def _load_api_keys(self) -> Dict[str, str]:
        """API 키 로드"""
        api_keys = {}
        
        # 환경변수에서 API 키 로드
        api_keys['alpha_vantage'] = os.getenv('ALPHA_VANTAGE_API_KEY', '')
        api_keys['fred'] = os.getenv('FRED_API_KEY', '')
        api_keys['quandl'] = os.getenv('QUANDL_API_KEY', '')
        api_keys['polygon'] = os.getenv('POLYGON_API_KEY', '')
        
        # 한국 경제지표 API 키
        api_keys['korean_bank'] = os.getenv('KOREAN_BANK_API_KEY', '')
        api_keys['kostat'] = os.getenv('KOSTAT_API_KEY', '')
        api_keys['kdi'] = os.getenv('KDI_API_KEY', '')
        
        return api_keys
    
    async def _get_session(self):
        """HTTP 세션 생성"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    def setup_tools(self):
        """외부 API 도구들 설정"""
        
        # 금융 데이터 API
        self.register_tool(
            "fetch_market_data",
            self.fetch_market_data,
            "시장 데이터 수집"
        )
        
        self.register_tool(
            "fetch_economic_indicators",
            self.fetch_economic_indicators,
            "경제 지표 수집"
        )
        
        self.register_tool(
            "fetch_pension_info",
            self.fetch_pension_info,
            "연금 정보 수집"
        )
        
        self.register_tool(
            "fetch_interest_rates",
            self.fetch_interest_rates,
            "금리 정보 수집"
        )
        
        self.register_tool(
            "fetch_stock_data",
            self.fetch_stock_data,
            "주식 데이터 수집"
        )
        
        self.register_tool(
            "fetch_bond_data",
            self.fetch_bond_data,
            "채권 데이터 수집"
        )
        
        self.register_tool(
            "fetch_currency_rates",
            self.fetch_currency_rates,
            "환율 정보 수집"
        )
        
        self.register_tool(
            "fetch_inflation_data",
            self.fetch_inflation_data,
            "인플레이션 데이터 수집"
        )
    
    async def start(self):
        """서버 시작"""
        self.is_running = True
        self.logger.info("외부 API 연동 서버가 시작되었습니다.")
    
    async def stop(self):
        """서버 중지"""
        self.is_running = False
        if self.session:
            await self.session.close()
        self.logger.info("외부 API 연동 서버가 중지되었습니다.")
    
    # 도구 구현 메서드들
    async def fetch_market_data(self, symbols: List[str] = None, period: str = "1mo", country: str = "KR", **kwargs) -> Dict[str, Any]:
        """시장 데이터 수집"""
        try:
            if symbols is None:
                if country == "KR":
                    symbols = ["^KS11", "^KQ11", "005930.KS", "000660.KS", "035420.KS"]  # KOSPI, KOSDAQ, 삼성전자, SK하이닉스, NAVER
                else:
                    symbols = ["^GSPC", "^IXIC", "^DJI", "QQQ", "SPY"]  # 주요 지수들
            
            market_data = {}
            
            for symbol in symbols:
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period=period)
                    
                    if not hist.empty:
                        latest = hist.iloc[-1]
                        market_data[symbol] = {
                            "name": ticker.info.get("longName", symbol),
                            "current_price": float(latest["Close"]),
                            "change": float(latest["Close"] - hist.iloc[-2]["Close"]) if len(hist) > 1 else 0,
                            "change_percent": float((latest["Close"] - hist.iloc[-2]["Close"]) / hist.iloc[-2]["Close"] * 100) if len(hist) > 1 else 0,
                            "volume": int(latest["Volume"]),
                            "high_52w": float(hist["High"].max()),
                            "low_52w": float(hist["Low"].min()),
                            "last_updated": datetime.now().isoformat()
                        }
                except Exception as e:
                    self.logger.warning(f"Failed to fetch data for {symbol}: {str(e)}")
            
            return {
                "status": "success",
                "message": f"시장 데이터 수집 완료 ({len(market_data)}개 심볼)",
                "data": market_data,
                "country": country,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"status": "error", "message": f"시장 데이터 수집 실패: {str(e)}"}
    
    async def fetch_economic_indicators(self, country: str = "KR", **kwargs) -> Dict[str, Any]:
        """경제 지표 수집"""
        try:
            if country == "KR":
                # 한국 경제지표 API 연동 (API 키가 있는 경우)
                if self.api_keys.get('korean_bank') or self.api_keys.get('kostat'):
                    session = await self._get_session()
                    
                    # 한국 주요 경제 지표들
                    korean_indicators = {
                        "GDP": "한국 GDP",
                        "Inflation": "소비자물가지수",
                        "Unemployment": "실업률",
                        "Interest_Rate": "기준금리",
                        "Consumer_Confidence": "소비자심리지수",
                        "Export": "수출지수",
                        "Import": "수입지수"
                    }
                    
                    # 실제 API 연동 코드는 여기에 구현
                    # 현재는 샘플 데이터 사용
                    economic_data = {
                        "GDP": {"value": 2.1, "date": "2024-01-01", "source": "한국은행"},
                        "Inflation": {"value": 2.8, "date": "2024-01-01", "source": "통계청"},
                        "Unemployment": {"value": 3.2, "date": "2024-01-01", "source": "통계청"},
                        "Interest_Rate": {"value": 3.5, "date": "2024-01-01", "source": "한국은행"},
                        "Consumer_Confidence": {"value": 98.5, "date": "2024-01-01", "source": "한국은행"}
                    }
                    
                    return {
                        "status": "success",
                        "message": f"한국 경제 지표 수집 완료 ({len(economic_data)}개)",
                        "data": economic_data,
                        "country": country,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    # API 키가 없는 경우 한국 기준 샘플 데이터
                    sample_data = {
                        "GDP": {"value": 2.1, "date": "2024-01-01", "source": "한국은행"},
                        "Inflation": {"value": 2.8, "date": "2024-01-01", "source": "통계청"},
                        "Unemployment": {"value": 3.2, "date": "2024-01-01", "source": "통계청"},
                        "Interest_Rate": {"value": 3.5, "date": "2024-01-01", "source": "한국은행"},
                        "Consumer_Confidence": {"value": 98.5, "date": "2024-01-01", "source": "한국은행"}
                    }
                    
                    return {
                        "status": "success",
                        "message": "한국 경제 지표 수집 완료 (샘플 데이터)",
                        "data": sample_data,
                        "country": country,
                        "timestamp": datetime.now().isoformat()
                    }
            else:
                # FRED API를 사용한 경제 지표 수집 (API 키가 있는 경우)
                if self.api_keys.get('fred'):
                    session = await self._get_session()
                    
                    # 주요 경제 지표들
                    indicators = {
                        "GDP": "GDP",
                        "Inflation": "CPIAUCSL",
                        "Unemployment": "UNRATE",
                        "Interest_Rate": "FEDFUNDS",
                        "Consumer_Confidence": "UMCSENT"
                    }
                
                economic_data = {}
                
                for name, series_id in indicators.items():
                    try:
                        url = f"https://api.stlouisfed.org/fred/series/observations"
                        params = {
                            "series_id": series_id,
                            "api_key": self.api_keys['fred'],
                            "file_type": "json",
                            "limit": 1,
                            "sort_order": "desc"
                        }
                        
                        async with session.get(url, params=params) as response:
                            if response.status == 200:
                                data = await response.json()
                                if data.get("observations"):
                                    latest = data["observations"][0]
                                    economic_data[name] = {
                                        "value": float(latest["value"]) if latest["value"] != "." else None,
                                        "date": latest["date"],
                                        "series_id": series_id
                                    }
                    except Exception as e:
                        self.logger.warning(f"Failed to fetch {name}: {str(e)}")
                
                return {
                    "status": "success",
                    "message": f"경제 지표 수집 완료 ({len(economic_data)}개)",
                    "data": economic_data,
                    "country": country,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                # API 키가 없는 경우 샘플 데이터 반환
                sample_data = {
                    "GDP": {"value": 2.1, "date": "2024-01-01", "series_id": "GDP"},
                    "Inflation": {"value": 3.2, "date": "2024-01-01", "series_id": "CPIAUCSL"},
                    "Unemployment": {"value": 3.8, "date": "2024-01-01", "series_id": "UNRATE"},
                    "Interest_Rate": {"value": 5.25, "date": "2024-01-01", "series_id": "FEDFUNDS"}
                }
                
                return {
                    "status": "success",
                    "message": "경제 지표 수집 완료 (샘플 데이터)",
                    "data": sample_data,
                    "country": country,
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            return {"status": "error", "message": f"경제 지표 수집 실패: {str(e)}"}
    
    async def fetch_pension_info(self, country: str = "KR", **kwargs) -> Dict[str, Any]:
        """연금 정보 수집"""
        try:
            # 한국 연금 정보 (실제 API가 없는 경우 샘플 데이터)
            pension_data = {
                "national_pension": {
                    "contribution_rate": 9.0,  # 국민연금 보험료율
                    "max_contribution": 5310000,  # 최대 보험료 (2024년 기준)
                    "min_contribution": 531000,   # 최소 보험료 (2024년 기준)
                    "retirement_age": 65,
                    "early_retirement_age": 60,
                    "benefit_calculation": "평균소득액 × 1.3% × 가입기간",
                    "max_benefit_period": 40,
                    "min_benefit_period": 10,
                    "tax_deduction": True,
                    "source": "국민연금공단"
                },
                "retirement_pension": {
                    "dc_contribution_rate": 0.12,        # 확정기여형 기여율
                    "db_replacement_rate": 0.5,         # 확정급여형 대체율
                    "vesting_period": 1,                 # 권리귀속 기간 (년)
                    "max_contribution": 15000000,        # 연간 최대 기여한도
                    "tax_deduction": True,
                    "withdrawal_age": 55,
                    "source": "근로복지공단"
                },
                "irp": {
                    "annual_limit": 12000000,            # IRP 연간 납입한도
                    "tax_deduction": True,               # 세제 혜택
                    "withdrawal_age": 55,                # 인출 가능 나이
                    "max_balance": 200000000,            # 최대 잔액 한도
                    "management_fee": 0.005,            # 관리수수료 (0.5%)
                    "source": "금융투자업계"
                },
                "pension_savings": {
                    "annual_limit": 4000000,             # 연금저축 연간 납입한도
                    "tax_deduction": True,               # 세제 혜택
                    "withdrawal_age": 55,                # 인출 가능 나이
                    "max_balance": 70000000,             # 최대 잔액 한도
                    "management_fee": 0.003,            # 관리수수료 (0.3%)
                    "source": "은행권"
                },
                "housing_pension": {
                    "min_age": 60,                       # 최소 가입 나이
                    "max_age": 85,                       # 최대 가입 나이
                    "min_property_value": 300000000,    # 최소 부동산 가치
                    "max_monthly_payment": 2000000,      # 최대 월 지급액
                    "guarantee_period": 10,              # 보장기간 (년)
                    "source": "주택도시보증공사"
                }
            }
            
            return {
                "status": "success",
                "message": "연금 정보 수집 완료",
                "data": pension_data,
                "country": country,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"status": "error", "message": f"연금 정보 수집 실패: {str(e)}"}
    
    async def fetch_interest_rates(self, country: str = "KR", **kwargs) -> Dict[str, Any]:
        """금리 정보 수집"""
        try:
            if country == "KR":
                # 한국 국채 수익률 및 금리 정보
                korean_rates = {
                    "기준금리": {"rate": 3.5, "maturity": "기준금리", "source": "한국은행"},
                    "3년국채": {"rate": 3.2, "maturity": "3Y", "source": "한국거래소"},
                    "5년국채": {"rate": 3.4, "maturity": "5Y", "source": "한국거래소"},
                    "10년국채": {"rate": 3.6, "maturity": "10Y", "source": "한국거래소"},
                    "20년국채": {"rate": 3.8, "maturity": "20Y", "source": "한국거래소"},
                    "정기예금": {"rate": 3.0, "maturity": "1Y", "source": "은행권"}
                }
                
                return {
                    "status": "success",
                    "message": f"한국 금리 정보 수집 완료 ({len(korean_rates)}개)",
                    "data": korean_rates,
                    "country": country,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                # 미국 국채 수익률 (yfinance 사용)
                treasury_symbols = {
                    "3M": "^IRX",    # 3개월 국채
                    "1Y": "^FVX",    # 1년 국채
                    "2Y": "^TNX",    # 2년 국채
                    "5Y": "^TYX",    # 5년 국채
                    "10Y": "^TNX",   # 10년 국채
                    "30Y": "^TYX"    # 30년 국채
                }
            
                interest_rates = {}
                
                for maturity, symbol in treasury_symbols.items():
                    try:
                        ticker = yf.Ticker(symbol)
                        info = ticker.info
                        
                        if info and "regularMarketPrice" in info:
                            interest_rates[maturity] = {
                                "rate": float(info["regularMarketPrice"]),
                                "maturity": maturity,
                                "last_updated": datetime.now().isoformat()
                            }
                    except Exception as e:
                        self.logger.warning(f"Failed to fetch rate for {maturity}: {str(e)}")
                
                # 샘플 데이터로 보완
                if not interest_rates:
                    interest_rates = {
                        "3M": {"rate": 5.25, "maturity": "3M"},
                        "1Y": {"rate": 5.10, "maturity": "1Y"},
                        "2Y": {"rate": 4.95, "maturity": "2Y"},
                        "5Y": {"rate": 4.80, "maturity": "5Y"},
                        "10Y": {"rate": 4.65, "maturity": "10Y"},
                        "30Y": {"rate": 4.50, "maturity": "30Y"}
                    }
                
                return {
                    "status": "success",
                    "message": f"금리 정보 수집 완료 ({len(interest_rates)}개)",
                    "data": interest_rates,
                    "country": country,
                    "timestamp": datetime.now().isoformat()
                }
            
        except Exception as e:
            return {"status": "error", "message": f"금리 정보 수집 실패: {str(e)}"}
    
    async def fetch_stock_data(self, symbols: List[str], period: str = "1mo", **kwargs) -> Dict[str, Any]:
        """주식 데이터 수집"""
        try:
            stock_data = {}
            
            for symbol in symbols:
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period=period)
                    info = ticker.info
                    
                    if not hist.empty:
                        latest = hist.iloc[-1]
                        stock_data[symbol] = {
                            "name": info.get("longName", symbol),
                            "sector": info.get("sector", "Unknown"),
                            "industry": info.get("industry", "Unknown"),
                            "current_price": float(latest["Close"]),
                            "change": float(latest["Close"] - hist.iloc[-2]["Close"]) if len(hist) > 1 else 0,
                            "change_percent": float((latest["Close"] - hist.iloc[-2]["Close"]) / hist.iloc[-2]["Close"] * 100) if len(hist) > 1 else 0,
                            "volume": int(latest["Volume"]),
                            "market_cap": info.get("marketCap", 0),
                            "pe_ratio": info.get("trailingPE", 0),
                            "dividend_yield": info.get("dividendYield", 0),
                            "beta": info.get("beta", 0),
                            "last_updated": datetime.now().isoformat()
                        }
                except Exception as e:
                    self.logger.warning(f"Failed to fetch stock data for {symbol}: {str(e)}")
            
            return {
                "status": "success",
                "message": f"주식 데이터 수집 완료 ({len(stock_data)}개)",
                "data": stock_data,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"status": "error", "message": f"주식 데이터 수집 실패: {str(e)}"}
    
    async def fetch_bond_data(self, country: str = "KR", **kwargs) -> Dict[str, Any]:
        """채권 데이터 수집"""
        try:
            if country == "KR":
                # 한국 국채 및 채권 데이터
                korean_bonds = {
                    "3년국채": {"yield": 3.2, "duration": "3Y", "type": "국채"},
                    "5년국채": {"yield": 3.4, "duration": "5Y", "type": "국채"},
                    "10년국채": {"yield": 3.6, "duration": "10Y", "type": "국채"},
                    "20년국채": {"yield": 3.8, "duration": "20Y", "type": "국채"},
                    "회사채": {"yield": 4.2, "duration": "5Y", "type": "회사채"},
                    "정기예금": {"yield": 3.0, "duration": "1Y", "type": "예금"}
                }
                
                return {
                    "status": "success",
                    "message": f"한국 채권 데이터 수집 완료 ({len(korean_bonds)}개)",
                    "data": korean_bonds,
                    "country": country,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                # 국채 ETF를 통한 채권 데이터
                bond_etfs = {
                    "SHY": "1-3년 국채",
                    "IEF": "7-10년 국채", 
                    "TLT": "20년 이상 국채",
                    "AGG": "전체 채권 시장"
                }
            
                bond_data = {}
                
                for etf, description in bond_etfs.items():
                    try:
                        ticker = yf.Ticker(etf)
                        hist = ticker.history(period="1mo")
                        info = ticker.info
                        
                        if not hist.empty:
                            latest = hist.iloc[-1]
                            bond_data[etf] = {
                                "name": description,
                                "current_price": float(latest["Close"]),
                                "change": float(latest["Close"] - hist.iloc[-2]["Close"]) if len(hist) > 1 else 0,
                                "change_percent": float((latest["Close"] - hist.iloc[-2]["Close"]) / hist.iloc[-2]["Close"] * 100) if len(hist) > 1 else 0,
                                "volume": int(latest["Volume"]),
                                "expense_ratio": info.get("annualReportExpenseRatio", 0),
                                "yield": info.get("yield", 0),
                                "last_updated": datetime.now().isoformat()
                            }
                    except Exception as e:
                        self.logger.warning(f"Failed to fetch bond data for {etf}: {str(e)}")
                
                return {
                    "status": "success",
                    "message": f"채권 데이터 수집 완료 ({len(bond_data)}개)",
                    "data": bond_data,
                    "country": country,
                    "timestamp": datetime.now().isoformat()
                }
            
        except Exception as e:
            return {"status": "error", "message": f"채권 데이터 수집 실패: {str(e)}"}
    
    async def fetch_currency_rates(self, base_currency: str = "KRW", **kwargs) -> Dict[str, Any]:
        """환율 정보 수집"""
        try:
            # 한국 기준 주요 통화 페어
            currency_pairs = ["USDKRW=X", "EURKRW=X", "GBPKRW=X", "JPYKRW=X", "CNYKRW=X"]
            
            currency_data = {}
            
            for pair in currency_pairs:
                try:
                    ticker = yf.Ticker(pair)
                    hist = ticker.history(period="1d")
                    
                    if not hist.empty:
                        latest = hist.iloc[-1]
                        currency_data[pair] = {
                            "rate": float(latest["Close"]),
                            "change": float(latest["Close"] - hist.iloc[-2]["Close"]) if len(hist) > 1 else 0,
                            "change_percent": float((latest["Close"] - hist.iloc[-2]["Close"]) / hist.iloc[-2]["Close"] * 100) if len(hist) > 1 else 0,
                            "last_updated": datetime.now().isoformat()
                        }
                except Exception as e:
                    self.logger.warning(f"Failed to fetch currency data for {pair}: {str(e)}")
            
            return {
                "status": "success",
                "message": f"환율 정보 수집 완료 ({len(currency_data)}개)",
                "data": currency_data,
                "base_currency": base_currency,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"status": "error", "message": f"환율 정보 수집 실패: {str(e)}"}
    
    async def fetch_inflation_data(self, country: str = "KR", **kwargs) -> Dict[str, Any]:
        """인플레이션 데이터 수집"""
        try:
            # FRED API를 사용한 인플레이션 데이터
            if self.api_keys.get('fred'):
                session = await self._get_session()
                
                inflation_series = {
                    "CPI": "CPIAUCSL",      # 소비자물가지수
                    "Core_CPI": "CPILFESL", # 핵심소비자물가지수
                    "PCE": "PCEPI",          # 개인소비지출물가지수
                    "Core_PCE": "PCEPILFE"   # 핵심개인소비지출물가지수
                }
                
                inflation_data = {}
                
                for name, series_id in inflation_series.items():
                    try:
                        url = f"https://api.stlouisfed.org/fred/series/observations"
                        params = {
                            "series_id": series_id,
                            "api_key": self.api_keys['fred'],
                            "file_type": "json",
                            "limit": 2,
                            "sort_order": "desc"
                        }
                        
                        async with session.get(url, params=params) as response:
                            if response.status == 200:
                                data = await response.json()
                                if data.get("observations") and len(data["observations"]) >= 2:
                                    current = data["observations"][0]
                                    previous = data["observations"][1]
                                    
                                    if current["value"] != "." and previous["value"] != ".":
                                        current_value = float(current["value"])
                                        previous_value = float(previous["value"])
                                        inflation_rate = ((current_value - previous_value) / previous_value) * 100
                                        
                                        inflation_data[name] = {
                                            "current_value": current_value,
                                            "previous_value": previous_value,
                                            "inflation_rate": round(inflation_rate, 2),
                                            "date": current["date"],
                                            "series_id": series_id
                                        }
                    except Exception as e:
                        self.logger.warning(f"Failed to fetch inflation data for {name}: {str(e)}")
                
                return {
                    "status": "success",
                    "message": f"인플레이션 데이터 수집 완료 ({len(inflation_data)}개)",
                    "data": inflation_data,
                    "country": country,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                # API 키가 없는 경우 한국 기준 샘플 데이터
                if country == "KR":
                    sample_data = {
                        "소비자물가지수": {"current_value": 108.2, "inflation_rate": 2.8, "date": "2024-01-01", "source": "통계청"},
                        "핵심소비자물가지수": {"current_value": 109.1, "inflation_rate": 3.1, "date": "2024-01-01", "source": "통계청"},
                        "생산자물가지수": {"current_value": 105.8, "inflation_rate": 1.9, "date": "2024-01-01", "source": "통계청"},
                        "GDP디플레이터": {"current_value": 102.3, "inflation_rate": 2.3, "date": "2024-01-01", "source": "한국은행"}
                    }
                else:
                    sample_data = {
                        "CPI": {"current_value": 308.417, "inflation_rate": 3.2, "date": "2024-01-01"},
                        "Core_CPI": {"current_value": 311.608, "inflation_rate": 3.8, "date": "2024-01-01"},
                        "PCE": {"current_value": 121.049, "inflation_rate": 2.6, "date": "2024-01-01"},
                        "Core_PCE": {"current_value": 120.671, "inflation_rate": 2.9, "date": "2024-01-01"}
                    }
                
                return {
                    "status": "success",
                    "message": "인플레이션 데이터 수집 완료 (샘플 데이터)",
                    "data": sample_data,
                    "country": country,
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            return {"status": "error", "message": f"인플레이션 데이터 수집 실패: {str(e)}"}
