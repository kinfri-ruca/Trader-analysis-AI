# 📊 Trader Analytics Dashboard

> AI 기반 실시간 트레이더 성과 분석 및 인사이트 제공

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Gemini](https://img.shields.io/badge/Gemini-AI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)

## 🎯 주요 기능

- **📈 실시간 성과 분석**: 50명 트레이더의 승률, 샤프 비율, MDD 등 핵심 지표
- **🤖 AI 챗봇**: Gemini AI 기반 자연어 질의응답
- **📊 대화형 차트**: Plotly 기반 인터랙티브 시각화
- **🔍 필터링**: 거래 스타일, 리스크 성향, 경력별 필터
- **💡 인사이트**: 자동화된 성과 분석 및 개선 제안

## 🚀 데모

[Live Demo](https://your-app.streamlit.app)

## 🛠️ 기술 스택

- **Frontend**: Streamlit
- **AI**: Google Gemini API
- **Data**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib
- **Font**: Pretendard

## 📦 설치 및 실행

```bash
# 저장소 클론
git clone https://github.com/YOUR_USERNAME/trader-analysis-dashboard.git
cd trader-analysis-dashboard

# 패키지 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일에 GEMINI_API_KEY 추가

# 실행
streamlit run app.py
```

## 🔑 API 키 설정

1. [Google AI Studio](https://makersuite.google.com/app/apikey)에서 무료 API 키 발급
2. `.env` 파일에 추가:
```
GEMINI_API_KEY=your_api_key_here
```

## 📊 데이터 구조

```
data/
├── analysis_results_50.json    # 50명 트레이더 성과 분석
├── trader_profiles_50.csv       # 트레이더 프로필
└── trading_transactions_50.csv  # 2,310건 거래 내역
```

## 🌐 배포

[DEPLOY.md](DEPLOY.md) 참고

## 📝 라이선스

MIT License

## 👥 기여

Pull Request 환영합니다!

## 📧 문의

이슈 또는 이메일로 문의해주세요.

---

Made with ❤️ using Streamlit and Gemini AI
