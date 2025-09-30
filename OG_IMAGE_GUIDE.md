# OG Image 가이드

## 권장 사양
- 크기: 1200 x 630px
- 포맷: PNG 또는 JPG
- 용량: 8MB 이하
- 비율: 1.91:1

## 포함할 내용
1. **타이틀**: "Trader Analytics Dashboard"
2. **서브타이틀**: "AI 기반 트레이더 성과 분석"
3. **아이콘**: 📊 차트 이미지
4. **배경**: 깔끔한 그라데이션 또는 단색

## 제작 방법

### 옵션 1: Canva (추천)
1. https://canva.com 접속
2. "Custom size" → 1200 x 630
3. 템플릿 선택 또는 직접 디자인
4. PNG로 다운로드

### 옵션 2: Figma
1. Frame 생성 (1200 x 630)
2. 디자인
3. Export as PNG

### 옵션 3: 온라인 도구
- https://www.opengraph.xyz/
- https://hotpot.ai/templates/social-media

## 저장 위치
```
trader-analysis-mvp/
└── static/
    └── og-image.png
```

## app.py 수정
이미지 업로드 후 아래 경로 수정:
```html
<meta property="og:image" content="https://your-app.streamlit.app/app/static/og-image.png">
```

## 디자인 예시
```
┌─────────────────────────────────────┐
│                                     │
│         📊                          │
│   Trader Analytics                  │
│        Dashboard                    │
│                                     │
│  AI 기반 트레이더 성과 분석          │
│                                     │
│  ✓ 실시간 분석  ✓ AI 챗봇           │
│  ✓ 50명 트레이더  ✓ 2,310건 거래    │
│                                     │
└─────────────────────────────────────┘
```

## 테스트
- https://www.opengraph.xyz/
- https://cards-dev.twitter.com/validator
