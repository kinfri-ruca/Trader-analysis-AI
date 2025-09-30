"""
50명 트레이더 현실적 데이터 생성
웹 검색 기반 통계 반영
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# 시드 고정 (재현성)
np.random.seed(42)
random.seed(42)

# 한국 이름 풀
FIRST_NAMES = ['민준', '서연', '지훈', '하은', '도윤', '수아', '시우', '지우', '예준', '서현',
               '준서', '하윤', '주원', '지민', '건우', '지아', '유준', '채원', '현우', '다은',
               '지호', '소율', '준혁', '서윤', '도현', '예은', '시윤', '서우', '윤서', '지환',
               '민서', '하준', '지후', '채윤', '승우', '수민', '준우', '지율', '시원', '서진',
               '태양', '가은', '우진', '나은', '민재', '예진', '지안', '서아', '현준', '은서']

LAST_NAMES = ['김', '이', '박', '최', '정', '강', '조', '윤', '장', '임',
              '한', '오', '서', '신', '권', '황', '안', '송', '전', '홍']

# 실제 주요 주식 심볼
SYMBOLS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META', 'AMD',
           'NFLX', 'ADBE', 'CRM', 'ORCL', 'INTC', 'CSCO', 'QCOM',
           'JPM', 'BAC', 'WFC', 'GS', 'MS', 'V', 'MA', 'PYPL',
           'DIS', 'NKE', 'MCD', 'SBUX', 'KO', 'PEP', 'WMT']

# 거래 스타일
TRADING_STYLES = ['단기매매', '중기투자', '장기투자', '스윙트레이딩']

# 리스크 성향
RISK_LEVELS = ['저위험', '중위험', '고위험']

# 섹터
SECTORS = ['기술/반도체', '금융/은행', '헬스케어', '소비재', '에너지', '통신']

def generate_trader_profiles(n=50):
    """50명 트레이더 프로필 생성"""
    profiles = []
    
    for i in range(n):
        trader_id = f"T{i+1:03d}"
        name = random.choice(LAST_NAMES) + random.choice(FIRST_NAMES)
        
        # 경력 (1-10년)
        years_exp = random.randint(1, 10)
        
        # 거래 스타일 (경력에 따라)
        if years_exp <= 2:
            style = random.choice(['단기매매', '스윙트레이딩'])
        elif years_exp <= 5:
            style = random.choice(['단기매매', '중기투자', '스윙트레이딩'])
        else:
            style = random.choice(TRADING_STYLES)
        
        # 리스크 성향
        risk = random.choices(RISK_LEVELS, weights=[0.3, 0.5, 0.2])[0]
        
        profile = {
            'trader_id': trader_id,
            'name': name,
            'join_date': (datetime.now() - timedelta(days=years_exp*365)).strftime('%Y-%m-%d'),
            'trading_style': style,
            'risk_tolerance': risk,
            'preferred_sectors': random.choice(SECTORS),
            'years_experience': years_exp,
            'education': random.choice(['서울대', 'KAIST', '연세대', '고려대', '경북대', '부산대']),
            'certifications': random.choice(['CFA Level 1', 'CFA Level 2', 'CFA Level 3', 'None']),
            'account_size': random.randint(100000, 500000),
            'performance_goal': f"{random.randint(10, 30)}% annual return"
        }
        profiles.append(profile)
    
    return pd.DataFrame(profiles)

def generate_transactions(profiles_df, n_trades_per_trader=20):
    """거래 내역 생성 (현실적 통계 반영)"""
    transactions = []
    
    for _, trader in profiles_df.iterrows():
        trader_id = trader['trader_id']
        years_exp = trader['years_experience']
        risk = trader['risk_tolerance']
        style = trader['trading_style']
        
        # 경력/스타일에 따른 승률 (웹 검색 통계 반영)
        if years_exp >= 7:
            base_win_rate = random.uniform(0.60, 0.75)  # 상위 트레이더
        elif years_exp >= 4:
            base_win_rate = random.uniform(0.50, 0.65)  # 중급
        else:
            base_win_rate = random.uniform(0.40, 0.55)  # 초급
        
        # 스타일 보정
        if style == '장기투자':
            base_win_rate += 0.05
        elif style == '단기매매':
            base_win_rate -= 0.05
        
        # 거래 횟수
        n_trades = random.randint(15, 30)
        
        # 날짜 범위
        start_date = datetime.now() - timedelta(days=180)
        
        for trade_idx in range(n_trades):
            # Buy
            buy_date = start_date + timedelta(days=random.randint(0, 180))
            buy_time = f"{random.randint(9, 15):02d}:{random.randint(0, 59):02d}:00"
            
            symbol = random.choice(SYMBOLS)
            quantity = random.choice([10, 25, 50, 100, 200])
            buy_price = round(random.uniform(50, 500), 2)
            commission = round(quantity * buy_price * 0.001, 2)
            buy_total = round(quantity * buy_price + commission, 2)
            
            transactions.append({
                'trader_id': trader_id,
                'date': buy_date.strftime('%Y-%m-%d'),
                'time': buy_time,
                'symbol': symbol,
                'side': 'Buy',
                'quantity': quantity,
                'price': buy_price,
                'commission': commission,
                'total_amount': buy_total
            })
            
            # Sell (승패 결정)
            is_win = random.random() < base_win_rate
            
            # 보유 기간
            if style == '단기매매':
                hold_days = random.randint(1, 5)
            elif style == '중기투자':
                hold_days = random.randint(5, 30)
            else:
                hold_days = random.randint(10, 60)
            
            sell_date = buy_date + timedelta(days=hold_days)
            sell_time = f"{random.randint(9, 15):02d}:{random.randint(0, 59):02d}:00"
            
            # 수익/손실 (현실적 분포)
            if is_win:
                pnl_pct = random.uniform(0.5, 15)  # 0.5-15% 수익
            else:
                pnl_pct = random.uniform(-10, -0.5)  # -10~-0.5% 손실
            
            sell_price = round(buy_price * (1 + pnl_pct/100), 2)
            sell_total = round(quantity * sell_price - commission, 2)
            
            transactions.append({
                'trader_id': trader_id,
                'date': sell_date.strftime('%Y-%m-%d'),
                'time': sell_time,
                'symbol': symbol,
                'side': 'Sell',
                'quantity': quantity,
                'price': sell_price,
                'commission': commission,
                'total_amount': sell_total
            })
    
    return pd.DataFrame(transactions).sort_values(['trader_id', 'date', 'time'])

# 실행
print("=" * 60)
print("50명 트레이더 데이터 생성 중...")
print("=" * 60)

# 프로필 생성
profiles = generate_trader_profiles(50)
print(f"\n[1/3] 프로필 생성 완료: {len(profiles)}명")

# 거래 내역 생성
transactions = generate_transactions(profiles)
print(f"[2/3] 거래 내역 생성 완료: {len(transactions)}건")

# 저장
profiles.to_csv('data/trader_profiles_50.csv', index=False, encoding='utf-8-sig')
transactions.to_csv('data/trading_transactions_50.csv', index=False, encoding='utf-8-sig')

print("[3/3] 파일 저장 완료")
print(f"\n출력 파일:")
print(f"  - data/trader_profiles_50.csv")
print(f"  - data/trading_transactions_50.csv")

# 통계
print(f"\n통계:")
print(f"  트레이더: {len(profiles)}명")
print(f"  총 거래: {len(transactions)}건")
print(f"  평균 거래/인: {len(transactions)//len(profiles)//2}회")
print(f"  기간: {transactions['date'].min()} ~ {transactions['date'].max()}")

print("\n[OK] 데이터 생성 완료!")
