# 🤖 트레이더 성과 분석 AI 챗봇 MVP

주식 트레이더들의 거래 패턴과 성과를 분석하고, **RAG + MCP 기술**을 활용한 대화형 AI 챗봇

---

## 🎯 프로젝트 목표

감이 아닌 **데이터 기반**으로 트레이더를 평가하고, AI가 실시간 인사이트와 코칭을 제공합니다.

### 핵심 가치
- ✅ **위험조정수익률 측정** (샤프 비율, MDD)
- 🎯 **거래 패턴 분석** (시간대, 보유기간, 선호 종목)
- 🤖 **AI 코칭** (개선 제안, 벤치마킹)
- 📊 **자연어 대화** ("김민수 트레이더 성과는?")

---

## 📂 프로젝트 구조

```
trader-analysis-mvp/
├── data/                                    # 📊 데이터
│   ├── trading_transactions.csv             # 거래 내역 (기본)
│   ├── trading_transactions_enhanced.csv    # 거래 내역 (확장)
│   ├── trader_profiles.csv                  # 트레이더 프로필 (기본)
│   ├── trader_profiles_enhanced.csv         # 트레이더 프로필 (확장)
│   ├── market_benchmarks.csv                # 시장 벤치마크
│   ├── risk_management_guidelines.md        # 리스크 관리 가이드
│   └── analysis_results.json                # 분석 결과 (지식 베이스)
│
├── src/                                     # 💻 소스 코드
│   ├── analyzer.py                          # ✅ 성과 분석 엔진
│   ├── rag_system.py                        # 🎯 RAG 검색 (다음)
│   ├── mcp_client.py                        # 🎯 MCP 클라이언트 (다음)
│   └── chatbot.py                           # 🎯 챗봇 메인 (다음)
│
├── docs/                                    # 📚 문서
│   ├── MVP_PLAN.md                          # MVP 개발 계획서
│   └── DATA_SAMPLES.md                      # 데이터 형식 설명
│
└── README.md                                # 👈 이 파일
```

---

## 🚀 빠른 시작

### 1. 현재 완료된 것: 데이터 분석 엔진

```bash
cd trader-analysis-mvp
python3 src/analyzer.py
```

**결과:**
- 5~7명 트레이더 성과 분석
- 샤프 비율, MDD, 승률 계산
- AI 인사이트 자동 생성
- JSON 지식 베이스 생성

### 2. 다음 단계: MCP 세팅 후

MCP (Model Context Protocol) 세팅 완료 후:
1. RAG 시스템 구축
2. MCP 클라이언트 연결
3. Claude API 통합 챗봇

---

## 📊 데이터 샘플 미리보기

### 거래 내역 예시
```csv
trader_id,date,time,symbol,side,quantity,price,commission,total_amount,order_type,notes
T001,2024-01-02,09:35:00,AAPL,Buy,100,185.50,9.95,18559.95,Market,Opening position
T001,2024-01-05,14:20:00,AAPL,Sell,100,188.30,9.95,18820.05,Limit,Take profit
```

### 분석 결과 예시
```json
{
  "T001": {
    "profile": {"name": "김민수", "trading_style": "단기매매"},
    "performance": {
      "win_rate": 80.0,
      "sharpe_ratio": 0.46,
      "total_pnl": 4355.50
    }
  }
}
```

자세한 내용: [DATA_SAMPLES.md](docs/DATA_SAMPLES.md)

---

## 💬 챗봇 기능 (예정)

### 질문 예시
- "김민수 트레이더의 최근 성과는?"
- "샤프 비율 상위 3명은?"
- "손실이 큰 트레이더에게 조언해줘"
- "이서연과 박준호 비교해줘"
- "아침에 주로 거래하는 사람은?"

### 응답 예시
```
김민수 트레이더(T001)의 성과:

📊 핵심 지표:
- 총 5회 거래, 승률 80%
- 총 손익: $4,355.50
- 샤프 비율: 0.46 (개선 여지)
- 최대손실폭: -8.95% (우수)

💡 인사이트:
높은 승률이나 리스크 관리 강화 필요.
주로 오전 9시 거래, 목요일이 가장 활발.
```

---

## 🔧 기술 스택

### 데이터 분석
- Python 3.10+
- Pandas, NumPy
- JSON

### RAG 시스템
- 키워드 기반 검색
- 컨텍스트 구성

### AI/LLM
- Claude API (Anthropic)
- Prompt Engineering

### MCP 통합
- Desktop Commander
- 로컬 파일 접근
- 실시간 동기화

---

## 📈 핵심 성과 지표 (KPI)

### 1. 수익성
- 총 손익, 평균 수익률, 승률

### 2. 위험 조정
- **샤프 비율**: 위험 대비 수익
  - 1.0 이상 양호, 1.5+ 우수
- **최대손실폭 (MDD)**: 최고점 대비 최대 하락
  - -10% 이하 우수, -20% 이하 보통

### 3. 거래 효율
- 손익비, 평균 보유기간, 거래 빈도

### 4. 패턴
- 선호 종목/시간대/요일

---

## 📚 문서

- [MVP_PLAN.md](docs/MVP_PLAN.md) - 상세 개발 계획
- [DATA_SAMPLES.md](docs/DATA_SAMPLES.md) - 데이터 형식 설명

---

## 🚦 개발 진행 상태

- [x] **Phase 1**: 데이터 분석 엔진 ✅
  - 거래 데이터 파싱
  - 성과 지표 계산
  - 패턴 분석
  - JSON 지식 베이스 생성

- [ ] **Phase 2**: RAG 시스템
  - Knowledge Base 검색
  - 컨텍스트 구성

- [ ] **Phase 3**: MCP 통합 챗봇
  - Desktop Commander 연결
  - Claude API 통합
  - 대화형 인터페이스

---

## 🎓 참고 자료

### 데이터 형식 참고
- TradingView CSV Export
- E*Trade Transaction History
- Interactive Brokers Report

### 성과 측정 이론
- Sharpe Ratio (William Sharpe, 1966)
- Maximum Drawdown
- Sortino Ratio
- Calmar Ratio

---

## 🙋‍♂️ 다음 단계

**MCP 세팅 완료 후 알려주세요!**

그러면:
1. RAG 시스템 구축
2. MCP 클라이언트 구현
3. Claude API 통합
4. 챗봇 완성

순서대로 진행하겠습니다! 🚀

---

**생성 일시**: 2024-09-30  
**버전**: MVP v0.1  
**라이선스**: MIT
