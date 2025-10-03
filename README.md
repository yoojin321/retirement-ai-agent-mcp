# 은퇴 설계 AI 에이전트 MCP 서버 - 한국 기준

은퇴 설계를 위한 AI 에이전트 MCP(Model Context Protocol) 서버입니다. 
**한국 기준**으로 사용자의 개인 맞춤형 은퇴 계획 수립을 도와주는 종합 솔루션을 제공합니다.

## 🇰🇷 한국 특화 기능
- **한국 연금제도**: 국민연금, 퇴직연금, IRP, 연금저축, 주택연금
- **한국 세제**: 소득세, 자본이득세, 연금세 등 한국 세법 반영  
- **한국 금융시장**: KOSPI, KOSDAQ, 한국 국채, 한국 기준금리
- **한국 경제지표**: 한국은행, 통계청 데이터 연동
- **한국 통화**: 원화(KRW) 기준 계산

## 🚀 주요 기능

### 1. 적립메이트 (Accumulation Server) - 8개 도구
- **자산 적립 최적화**: 은퇴 전 자산 적립 전략 수립
- **목표 자금 계산**: 연금현가법과 안전인출률법을 통한 정확한 계산
- **자금 격차 분석**: 필요 자금과 예상 자산 비교 분석
- **저축 계획 최적화**: 현실적이고 실행 가능한 저축 계획 제시
- **사용자 프로필 수집**: 개인 맞춤형 정보 수집
- **경제 가정 설정**: 물가상승률, 수익률 등 경제 변수 설정
- **자산 프로젝션**: 미래 자산 가치 예측
- **시나리오 분석**: 다양한 경제 상황별 시나리오 분석

### 2. 투자메이트 (Investment Server) - 7개 도구
- **포트폴리오 생성**: 보수/중립/성장형 3단계 포트폴리오 제안
- **동적 변동성 조정**: 시장 상황에 따른 자동 포트폴리오 조정
- **리스크 관리**: 개인별 위험 성향에 맞는 투자 전략
- **성과 모니터링**: 실시간 포트폴리오 성과 추적
- **리스크 프로파일 평가**: 개인별 위험 성향 분석
- **포트폴리오 최적화**: 효율적 프론티어 기반 최적화
- **성과 벤치마킹**: 시장 대비 성과 비교

### 3. 인출메이트 (Withdrawal Server) - 7개 도구
- **절세 인출 전략**: 세금을 최소화하는 인출 순서 최적화
- **3버킷 전략**: 현금/채권/성장자산의 체계적 관리
- **가드레일 시스템**: 안전한 인출을 위한 자동 조정
- **시나리오 비교**: 다양한 인출 전략의 효과 비교
- **자산 구조 분석**: 은퇴 자산의 구조적 분석
- **인출 시뮬레이션**: 다양한 인출 전략 시뮬레이션
- **세금 최적화**: 세금 효율적인 인출 순서 제안

### 4. 데이터 관리 서버 (Data Server) - 7개 도구
- **로컬 데이터베이스 관리**: SQLite 기반 로컬 데이터 저장
- **데이터 암호화**: 민감한 개인정보 암호화 저장
- **백업 및 복원**: 사용자 데이터 백업 및 복원 기능
- **데이터 무결성**: 데이터 일관성 및 무결성 보장
- **사용자 프로필 관리**: 개인별 프로필 데이터 관리
- **경제 가정 관리**: 경제 변수 설정 및 관리
- **투자 포트폴리오 관리**: 포트폴리오 데이터 저장 및 관리

### 5. 외부 API 서버 (External API Server) - 8개 도구
- **시장 데이터 수집**: 주식, 채권, 통화 등 실시간 시장 데이터
- **경제 지표 수집**: GDP, 인플레이션, 실업률 등 경제 지표
- **연금 정보 수집**: 국민연금, 퇴직연금 등 연금 정보
- **금리 정보 수집**: 기준금리, 국채 수익률 등 금리 정보
- **주식 데이터 수집**: 개별 주식의 가격 및 성과 데이터
- **채권 데이터 수집**: 채권 수익률 및 등급 정보
- **환율 정보 수집**: 주요 통화 환율 정보
- **인플레이션 데이터**: 소비자물가, 생산자물가 등 물가 정보

## 🏗️ 시스템 아키텍처

```
은퇴 설계 AI 에이전트 MCP 서버
├── 적립메이트 서버 (Accumulation Server) - 8개 도구
├── 투자메이트 서버 (Investment Server) - 7개 도구
├── 인출메이트 서버 (Withdrawal Server) - 7개 도구
├── 데이터 관리 서버 (Data Server) - 7개 도구
├── 외부 API 서버 (External API Server) - 8개 도구
├── 웹 대시보드 (Streamlit) - 사용자 인터페이스
├── 모바일 API (FastAPI) - RESTful API
└── Docker 환경 - 컨테이너화된 배포
```

**총 37개의 MCP 도구**를 통해 종합적인 은퇴 설계 솔루션을 제공합니다.

## 🛠️ 기술 스택

- **Backend**: Python 3.11, FastAPI, MCP (Model Context Protocol)
- **Database**: PostgreSQL, Redis, SQLite (로컬)
- **Container**: Docker, Docker Compose
- **AI/ML**: scikit-learn, numpy, pandas, scipy
- **Web UI**: Streamlit (웹 대시보드)
- **Mobile API**: FastAPI (RESTful API)
- **External APIs**: yfinance, FRED API, aiohttp
- **Security**: Fernet 암호화, 로컬 데이터 저장
- **Performance**: Redis 캐싱, 비동기 처리, 성능 모니터링

## 📦 설치 및 실행

### 1. 저장소 클론
```bash
git clone <repository-url>
cd retirement-ai-agent-mcp
```

### 2. 환경 변수 설정
```bash
cp env.example .env
# .env 파일을 편집하여 필요한 환경 변수 설정
# 💡 API 키 없이도 기본 기능 사용 가능 (샘플 데이터 사용)
# 🔑 실시간 데이터를 원한다면 한국은행, 통계청 API 키 발급 권장
```

### 3. Docker로 실행 (권장)
```bash
# Docker Compose로 모든 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 서비스 상태 확인
docker ps
```

### 4. Claude Desktop 연결 (MCP 클라이언트)

> 📋 **상세 설정 가이드**: [setup_claude_desktop.md](setup_claude_desktop.md) 파일을 참조하세요.

#### 빠른 설정 방법
1. **예시 설정 파일 복사**:
   ```bash
   # Windows
   copy claude_desktop_config_example.json "%APPDATA%\Claude\claude_desktop_config.json"
   
   # macOS/Linux
   cp claude_desktop_config_example.json ~/.config/claude/claude_desktop_config.json
   ```

2. **경로 수정**: 설정 파일에서 `{PROJECT_ROOT}` 부분을 실제 프로젝트 경로로 교체

3. **Claude Desktop 재시작**

#### 설정 파일 위치
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS/Linux**: `~/.config/claude/claude_desktop_config.json`

#### 예시 설정 파일
프로젝트에 포함된 `claude_desktop_config_example.json` 파일을 참조하여 설정하세요.

### 5. 웹 대시보드 실행
```bash
# Streamlit 웹 대시보드
streamlit run web_dashboard.py --server.port 8501
# 브라우저에서 http://localhost:8501 접속
```

### 6. 모바일 API 실행
```bash
# FastAPI 모바일 API 서버
python mobile_api.py
# API 문서: http://localhost:8001/docs
```

### 7. 개발 환경 설정
```bash
# Python 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# MCP 서버 직접 실행
python src/mcp_server.py

# 또는 HTTP API 서버 실행
python src/docker_main.py
```

## 🔧 MCP 도구 개요

**총 37개의 MCP 도구**를 통해 종합적인 은퇴 설계 솔루션을 제공합니다.

### 📊 주요 도구 카테고리
- **적립메이트 (8개)**: 자산 적립 계획, 목표 자금 계산, 시나리오 분석
- **투자메이트 (7개)**: 포트폴리오 구성, 리스크 관리, 성과 모니터링  
- **인출메이트 (7개)**: 안전인출률 계산, 3버킷 전략, 세금 최적화
- **데이터 관리 (7개)**: 개인 데이터 암호화, 백업, 복원
- **외부 API (8개)**: 실시간 시장 데이터, 경제지표, 연금 정보

## 💬 질문과 답변 예시

### 🏦 적립메이트 (자산 적립)
**Q: "35세 직장인입니다. 65세 은퇴을 목표로 월 200만원씩 저축하고 있는데, 은퇴 시점에 얼마나 모을 수 있을까요?"**

**A: 적립메이트가 분석해드리겠습니다:**
- 현재 자산: 5,000만원
- 월 저축액: 200만원
- 예상 수익률: 5% (연간)
- 30년 후 예상 자산: **약 15억원**
- 권장사항: IRP와 연금저축을 활용한 세제 혜택 최대화

### 📈 투자메이트 (포트폴리오 구성)
**Q: "보수적인 성향인데, 안전하면서도 적절한 수익을 낼 수 있는 포트폴리오를 추천해주세요."**

**A: 투자메이트가 보수형 포트폴리오를 제안합니다:**
- **채권 55%**: 한국 국채, 회사채
- **주식 20%**: KOSPI 대형주, 배당주
- **현금 10%**: 정기예금, MMF
- **대체투자 10%**: 금, REITs
- **기타 5%**: 해외 채권
- 예상 수익률: 4-5% (연간)

### 💰 인출메이트 (은퇴 후 인출)
**Q: "65세에 10억원 자산으로 은퇴했는데, 매월 얼마씩 인출해야 안전할까요?"**

**A: 인출메이트가 안전인출 전략을 제안합니다:**
- **안전인출률**: 월 250만원 (연 3,000만원, 3% 인출률)
- **3버킷 전략**:
  - 버킷1 (현금): 2년분 6,000만원
  - 버킷2 (채권): 3년분 9,000만원  
  - 버킷3 (주식): 나머지 8.5억원
- **인플레이션 대응**: 매년 2.8% 인출액 증가

### 📊 데이터메이트 (개인 데이터 관리)
**Q: "여러 금융사에 분산된 자산을 통합 관리하고 싶어요."**

**A: 데이터메이트가 통합 관리 솔루션을 제공합니다:**
- **자산 통합**: 모든 계좌 정보를 하나의 대시보드에서 관리
- **자동 분류**: 현금, 주식, 채권, 부동산별 자동 분류
- **성과 추적**: 계좌별 수익률 및 전체 포트폴리오 성과 분석
- **보안**: 모든 데이터는 로컬에 암호화 저장

### 🌐 외부 API (실시간 데이터)
**Q: "현재 시장 상황이 은퇴 계획에 어떤 영향을 미칠까요?"**

**A: 외부 API가 실시간 시장 데이터를 분석해드립니다:**
- **KOSPI**: 2,450 (-1.2%)
- **한국 10년 국채**: 3.6%
- **기준금리**: 3.5%
- **인플레이션**: 2.8%
- **권장사항**: 현재 금리 상승기에 채권 비중 확대 고려

## 🔒 보안 및 개인정보보호

- **로컬 데이터 저장**: 모든 개인 데이터는 로컬에 암호화 저장
- **데이터 익명화**: 외부 API 호출 시 개인정보 제거
- **접근 제어**: 사용자별 데이터 격리
- **암호화**: 민감한 데이터의 AES 암호화

## 📊 데이터 모델

### 사용자 프로필 (UserProfile)
- 개인 정보 (나이, 은퇴 목표 등)
- 소득 구조 (월 소득, 보너스 등)
- 지출 구조 (필수/선택 지출)
- 자산 포트폴리오 (현금, 투자, 부동산 등)
- 부채 구조 (주택대출, 신용카드 등)

### 은퇴 계획 (RetirementPlan)
- 경제 가정 (물가상승률, 수익률 등)
- 은퇴 목표 (목표 자금, 기간 등)
- 자산 프로젝션 (미래 자산 예측)
- 포트폴리오 배분 (자산별 비중)
- 인출 전략 (인출률, 방법 등)

## 🧪 테스트

### MCP 서버 테스트
```bash
# 간단한 MCP 서버 테스트 (권장)
python test_mcp_simple.py

# 성능 테스트
python test_performance.py

# 통합 테스트
python test_integration.py
```

### 개별 서버 테스트
```bash
# 적립 서버 테스트
python test_accumulation.py

# 투자 서버 테스트
python test_investment.py

# 인출 서버 테스트
python test_withdrawal.py

# 데이터 서버 테스트
python test_data_server.py

# 외부 API 서버 테스트
python test_external_api.py
```

### 단위 테스트
```bash
# 단위 테스트 실행
pytest tests/

# 커버리지 포함 테스트
pytest --cov=src tests/

# 특정 테스트 실행
pytest tests/test_servers/test_accumulation_server.py
```

### 테스트 파일 설명
- **`test_mcp_simple.py`**: MCP 서버 기본 연결 및 도구 테스트
- **`test_integration.py`**: 전체 시스템 통합 테스트
- **`test_performance.py`**: 성능 최적화 기능 테스트
- **`test_accumulation.py`**: 적립메이트 서버 기능 테스트
- **`test_investment.py`**: 투자메이트 서버 기능 테스트
- **`test_withdrawal.py`**: 인출메이트 서버 기능 테스트
- **`test_data_server.py`**: 데이터 관리 서버 기능 테스트
- **`test_external_api.py`**: 외부 API 서버 기능 테스트

## 📈 성능 모니터링

- **Redis 캐싱**: 응답 속도 최적화
- **비동기 처리**: 동시 요청 처리
- **성능 모니터링**: 요청 시간 및 처리량 추적
- **로그 관리**: 구조화된 로깅
- **헬스체크**: 서비스 상태 모니터링

## 🎯 사용 방법

### Claude Desktop에서 사용하기
1. **Claude Desktop 재시작** 후 연결 상태 확인
2. **테스트 질문**:
   ```
   "안녕하세요! 은퇴 설계 AI 에이전트가 연결되었나요?"
   "35세 직장인을 위한 은퇴 계획을 수립해주세요"
   "현재 자산 1억원, 목표 은퇴 자산 10억원으로 계획을 세워주세요"
   ```

### 웹 대시보드 사용하기
1. **대시보드 실행**: `streamlit run web_dashboard.py --server.port 8501`
2. **브라우저 접속**: `http://localhost:8501`
3. **기능 사용**: 
   - 대시보드: 전체 현황 조회
   - 적립: 자산 적립 계획 수립
   - 투자: 포트폴리오 구성
   - 인출: 은퇴 후 인출 전략
   - 데이터: 개인 데이터 관리
   - 시장: 실시간 시장 정보

### 모바일 API 사용하기
1. **API 서버 실행**: `python mobile_api.py`
2. **API 문서**: `http://localhost:8001/docs`
3. **주요 엔드포인트**:
   - `GET /api/health`: 서버 상태 확인
   - `GET /api/user/profile`: 사용자 프로필 조회
   - `POST /api/accumulation/calculate`: 은퇴 목표 계산
   - `GET /api/external/market-data`: 시장 데이터 조회

### Docker 환경 사용하기
1. **서비스 시작**: `docker-compose up -d`
2. **HTTP API**: `http://localhost:8000/docs`
3. **서비스 상태**: `docker ps`
4. **로그 확인**: `docker-compose logs -f`

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 🔧 문제 해결

### Claude Desktop 연결 문제
1. **Claude Desktop 재시작**: 완전히 종료 후 다시 실행
2. **설정 파일 확인**: 
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS/Linux: `~/.config/claude/claude_desktop_config.json`
3. **경로 확인**: `{PROJECT_ROOT}` 부분이 실제 프로젝트 경로로 교체되었는지 확인
4. **Python 환경**: Python 3.10+ 설치 확인
5. **경로 형식**: Windows는 백슬래시(`\`), macOS/Linux는 슬래시(`/`) 사용

### Docker 실행 문제
1. **Docker Desktop 실행**: Docker Desktop이 실행 중인지 확인
2. **포트 충돌**: 8000, 5432, 6379 포트 사용 여부 확인
3. **로그 확인**: `docker-compose logs -f`

### 패키지 설치 문제
1. **Python 버전**: Python 3.10+ 사용
2. **가상환경**: 가상환경 생성 후 패키지 설치
3. **의존성**: `pip install -r requirements.txt`

### 대안 실행 방법
1. **웹 대시보드**: `streamlit run web_dashboard.py --server.port 8501`
2. **모바일 API**: `python mobile_api.py`
3. **HTTP API**: `python src/docker_main.py`

---

**프로젝트**: 2025 Koscom AI Agent Challenge  
**지원 플랫폼**: Claude Desktop, 웹 대시보드, 모바일 API, Docker
