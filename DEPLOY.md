# Streamlit Cloud 배포 가이드

## 1. GitHub 저장소 생성

1. GitHub에 로그인
2. New Repository 클릭
3. 저장소 이름: `trader-analysis-dashboard`
4. Public으로 설정
5. Create repository

## 2. 로컬 코드를 GitHub에 푸시

```bash
cd C:\DEV\trader-analysis-mvp

# Git 초기화
git init

# 파일 추가
git add .

# 커밋
git commit -m "Initial commit: Trader Analysis Dashboard"

# 원격 저장소 연결
git remote add origin https://github.com/YOUR_USERNAME/trader-analysis-dashboard.git

# 푸시
git push -u origin main
```

## 3. Streamlit Cloud 배포

1. https://share.streamlit.io/ 접속
2. Sign in with GitHub
3. "New app" 클릭
4. 저장소 선택: `YOUR_USERNAME/trader-analysis-dashboard`
5. Branch: `main`
6. Main file path: `app.py`
7. Advanced settings 클릭

## 4. Secrets 설정 (중요!)

Advanced settings → Secrets에 다음 추가:

```toml
[api]
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

## 5. Deploy!

- "Deploy!" 버튼 클릭
- 5-10분 대기
- 배포 완료 후 URL 확인: `https://YOUR_APP_NAME.streamlit.app`

## 주의사항

1. **API 키 보안**: 
   - .env 파일은 GitHub에 업로드 안 됨 (.gitignore)
   - secrets.toml도 업로드 안 됨
   - Streamlit Cloud에서만 Secrets 설정

2. **데이터 파일**:
   - data/*.json, data/*.csv는 저장소에 포함됨
   - 민감한 데이터는 제외하거나 암호화

3. **무료 플랜 제한**:
   - 1개 앱
   - 공개 저장소만
   - 리소스 제한 있음

## 문제 해결

### 배포 실패 시
1. Logs 확인
2. requirements.txt 버전 확인
3. 파일 경로 확인 (절대 경로 문제)

### API 키 오류
- Streamlit Cloud Secrets 재확인
- 키 형식 확인

## 로컬 테스트

배포 전 로컬에서 테스트:
```bash
streamlit run app.py
```
