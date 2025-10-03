# Claude Desktop 설정 가이드

## 🚀 빠른 설정 방법

### 1단계: 프로젝트 경로 확인
```bash
# 프로젝트 디렉토리로 이동
cd retirement-ai-agent-mcp

# 현재 경로 확인
# Windows
echo %CD%

# macOS/Linux
pwd
```

### 2단계: 설정 파일 복사 및 수정

#### Windows 사용자
```bash
# 1. 예시 파일을 Claude Desktop 설정 위치로 복사
copy claude_desktop_config_example.json "%APPDATA%\Claude\claude_desktop_config.json"

# 2. 설정 파일 편집 (메모장 또는 다른 텍스트 에디터 사용)
notepad "%APPDATA%\Claude\claude_desktop_config.json"
```

#### macOS/Linux 사용자
```bash
# 1. Claude 설정 디렉토리 생성 (없는 경우)
mkdir -p ~/.config/claude

# 2. 예시 파일을 Claude Desktop 설정 위치로 복사
cp claude_desktop_config_example.json ~/.config/claude/claude_desktop_config.json

# 3. 설정 파일 편집
nano ~/.config/claude/claude_desktop_config.json
```

### 3단계: 경로 수정

설정 파일에서 `{PROJECT_ROOT}` 부분을 실제 프로젝트 경로로 교체:

#### Windows 예시
```json
{
  "mcpServers": {
    "retirement-ai-agent": {
      "command": "python",
      "args": ["C:\\Users\\YourName\\path\\to\\retirement-ai-agent-mcp\\src\\mcp_server.py"],
      "env": {
        "PYTHONPATH": "C:\\Users\\YourName\\path\\to\\retirement-ai-agent-mcp",
        "SECRET_KEY": "retirement-ai-agent-secret-key-2025",
        "ENCRYPTION_KEY": "retirement-encryption-key-2025"
      }
    }
  }
}
```

#### macOS/Linux 예시
```json
{
  "mcpServers": {
    "retirement-ai-agent": {
      "command": "python",
      "args": ["/Users/YourName/path/to/retirement-ai-agent-mcp/src/mcp_server.py"],
      "env": {
        "PYTHONPATH": "/Users/YourName/path/to/retirement-ai-agent-mcp",
        "SECRET_KEY": "retirement-ai-agent-secret-key-2025",
        "ENCRYPTION_KEY": "retirement-encryption-key-2025"
      }
    }
  }
}
```

### 4단계: Claude Desktop 재시작

1. **Claude Desktop 완전 종료**
2. **Claude Desktop 다시 실행**
3. **연결 상태 확인**: 하단에 "retirement-ai-agent" 서버 연결 표시 확인

## 🔧 문제 해결

### 경로 문제
- **Windows**: 백슬래시(`\`) 사용, 경로에 공백이 있으면 따옴표로 감싸기
- **macOS/Linux**: 슬래시(`/`) 사용, 절대 경로 사용 권장

### Python 환경 문제
```bash
# Python 버전 확인
python --version

# Python 3.10+ 필요
# 가상환경 사용 권장
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 연결 테스트
Claude Desktop에서 다음 질문으로 연결 확인:
```
"안녕하세요! 은퇴 설계 AI 에이전트가 연결되었나요?"
```

## 📁 파일 위치 요약

- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS/Linux**: `~/.config/claude/claude_desktop_config.json`
- **예시 파일**: `claude_desktop_config_example.json`
