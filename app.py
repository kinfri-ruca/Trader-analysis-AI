"""
Trader Performance Dashboard - Streamlit Web UI
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys
import os
from dotenv import load_dotenv

# .env 로드
load_dotenv()

# 경로 설정
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir / 'src'))

from rag_system import TradingKnowledgeBase
from chatbot import TraderAnalysisChatbot

# 페이지 설정
st.set_page_config(
    page_title="Trader Analytics Dashboard",
    page_icon="📊",
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
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stMetric {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Claude 스타일 채팅 UI */
    [data-testid="stChatMessageContent"] {
        background-color: transparent !important;
        padding: 1rem !important;
    }
    
    /* 사용자 메시지 */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background-color: #f7f7f8 !important;
        border-radius: 1rem !important;
        margin: 0.5rem 0 !important;
        padding: 1rem !important;
    }
    
    /* AI 메시지 */
    [data-testid="stChatMessage"]:not([data-testid*="user"]) {
        background-color: white !important;
        border: 1px solid #e5e5e5 !important;
        border-radius: 1rem !important;
        margin: 0.5rem 0 !important;
        padding: 1rem !important;
    }
    
    /* 입력창 스타일 */
    [data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        padding: 1rem !important;
        background: white !important;
        border-top: 1px solid #e5e5e5 !important;
        z-index: 999 !important;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05) !important;
    }
    
    /* PC 화면만 사이드바 여백 적용 */
    @media (min-width: 768px) {
        [data-testid="stChatInput"] {
            left: 21rem !important;
        }
        
        [data-testid="collapsedControl"] ~ div [data-testid="stChatInput"] {
            left: 0 !important;
        }
    }
    
    /* 입력창 내부 컨테이너 */
    [data-testid="stChatInput"] > div:first-child {
        background: transparent !important;
        padding: 0 !important;
    }
    
    [data-testid="stChatInput"] > div {
        max-width: 100% !important;
        margin: 0 auto !important;
        display: flex !important;
        align-items: center !important;
        gap: 0.5rem !important;
    }
    
    [data-testid="stChatInput"] textarea {
        min-height: 60px !important;
        max-height: 60px !important;
        border-radius: 16px !important;
        border: 1.5px solid #d1d5db !important;
        padding: 1rem 1.5rem !important;
        font-size: 0.95rem !important;
        resize: none !important;
        box-shadow: none !important;
        background: white !important;
    }
    
    [data-testid="stChatInput"] textarea::selection {
        background-color: #bfdbfe !important;
        color: #1e40af !important;
    }
    
    [data-testid="stChatInput"] textarea::-moz-selection {
        background-color: #bfdbfe !important;
        color: #1e40af !important;
    }
    
    ::selection {
        background-color: #bfdbfe !important;
        color: #1e40af !important;
    }
    
    ::-moz-selection {
        background-color: #bfdbfe !important;
        color: #1e40af !important;
    }
    
    [data-testid="stChatInput"] textarea:focus {
        border-color: #4b5563 !important;
        border-width: 2.5px !important;
        outline: none !important;
        box-shadow: none !important;
        background: white !important;
    }
    
    [data-testid="stChatInput"] button {
        background: #1f77b4 !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.5rem 0.8rem !important;
        color: white !important;
        margin: 0 0.5rem 0 0.25rem !important;
        height: auto !important;
        min-width: 40px !important;
        align-self: center !important;
    }
    
    [data-testid="stChatInput"] button:hover {
        background: #1557a0 !important;
    }
    
    /* 메인 컨텐츠 하단 여백 */
    .main > div {
        padding-bottom: 120px !important;
    }
</style>
""", unsafe_allow_html=True)

# 데이터 로드 (캐싱)
@st.cache_data
def load_data():
    """데이터 로드"""
    data_path = current_dir / 'data' / 'analysis_results_50.json'
    kb = TradingKnowledgeBase(str(data_path))
    traders = kb.get_all_traders()
    return pd.DataFrame([
        {
            'trader_id': t['trader_id'],
            'name': t['profile']['name'],
            'style': t['profile']['trading_style'],
            'risk': t['profile']['risk_tolerance'],
            'experience': t['profile']['years_experience'],
            'win_rate': t['performance']['win_rate'],
            'sharpe_ratio': t['performance']['sharpe_ratio'],
            'total_pnl': t['performance']['total_pnl'],
            'max_drawdown_pct': t['performance']['max_drawdown_pct'],
            'total_trades': t['performance']['total_trades'],
            'avg_hold_days': t['performance']['avg_hold_days']
        }
        for t in traders
    ])

@st.cache_resource
def load_chatbot():
    """챗봇 로드"""
    # Streamlit Cloud secrets 우선, 없으면 .env
    try:
        api_key = st.secrets["api"]["GEMINI_API_KEY"]
    except:
        api_key = os.getenv('GEMINI_API_KEY')
    
    data_path = str(current_dir / 'data' / 'analysis_results_50.json')
    return TraderAnalysisChatbot(api_key=api_key, provider='gemini', data_path=data_path)

# 메인
def main():
    # 헤더
    st.markdown('<h1 class="main-header">📊 Trader Performance Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # 데이터 로드
    try:
        df = load_data()
        chatbot = load_chatbot()
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        return
    
    # 사이드바
    with st.sidebar:
        st.header("🔍 필터")
        
        # 거래 스타일 필터
        styles = ['전체'] + sorted(df['style'].unique().tolist())
        selected_style = st.selectbox("거래 스타일", styles)
        
        # 리스크 필터
        risks = ['전체'] + sorted(df['risk'].unique().tolist())
        selected_risk = st.selectbox("리스크 성향", risks)
        
        # 경력 필터
        exp_range = st.slider(
            "경력 (년)",
            min_value=int(df['experience'].min()),
            max_value=int(df['experience'].max()),
            value=(int(df['experience'].min()), int(df['experience'].max()))
        )
        
        st.markdown("---")
        st.markdown("**📈 데이터 요약**")
        st.metric("총 트레이더", len(df))
        st.metric("평균 승률", f"{df['win_rate'].mean():.1f}%")
        st.metric("평균 샤프", f"{df['sharpe_ratio'].mean():.2f}")
    
    # 필터 적용
    filtered_df = df.copy()
    if selected_style != '전체':
        filtered_df = filtered_df[filtered_df['style'] == selected_style]
    if selected_risk != '전체':
        filtered_df = filtered_df[filtered_df['risk'] == selected_risk]
    filtered_df = filtered_df[
        (filtered_df['experience'] >= exp_range[0]) &
        (filtered_df['experience'] <= exp_range[1])
    ]
    
    # 탭 구성 - AI 챗봇을 첫 번째로
    tab1, tab2, tab3, tab4 = st.tabs(["💬 AI 챗봇", "📊 대시보드", "📈 차트", "📋 트레이더 목록"])
    
    with tab1:
        show_chatbot(chatbot)
    
    with tab2:
        show_dashboard(filtered_df)
    
    with tab3:
        show_charts(filtered_df)
    
    with tab4:
        show_trader_list(filtered_df)

def show_dashboard(df):
    """대시보드 탭"""
    st.subheader("📊 핵심 지표")
    
    # 상위 지표
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "평균 승률",
            f"{df['win_rate'].mean():.1f}%",
            f"{df['win_rate'].mean() - 50:.1f}% vs 50%"
        )
    
    with col2:
        st.metric(
            "평균 샤프 비율",
            f"{df['sharpe_ratio'].mean():.2f}",
            f"{df['sharpe_ratio'].mean() - 1:.2f} vs 1.0"
        )
    
    with col3:
        st.metric(
            "총 수익",
            f"${df['total_pnl'].sum():,.0f}",
            f"${df['total_pnl'].mean():,.0f} 평균"
        )
    
    with col4:
        st.metric(
            "평균 MDD",
            f"{df['max_drawdown_pct'].mean():.1f}%",
            "손실폭"
        )
    
    st.markdown("---")
    
    # Top 5 트레이더
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🥇 승률 Top 5")
        top_win = df.nlargest(5, 'win_rate')[['name', 'win_rate', 'total_trades']]
        for idx, row in top_win.iterrows():
            st.markdown(f"**{row['name']}**: {row['win_rate']:.1f}% ({row['total_trades']}회)")
    
    with col2:
        st.subheader("🥇 샤프 비율 Top 5")
        top_sharpe = df.nlargest(5, 'sharpe_ratio')[['name', 'sharpe_ratio', 'total_pnl']]
        for idx, row in top_sharpe.iterrows():
            st.markdown(f"**{row['name']}**: {row['sharpe_ratio']:.2f} (${row['total_pnl']:,.0f})")

def show_charts(df):
    """차트 탭"""
    st.subheader("📈 성과 분석 차트")
    
    # 버블 크기용 절대값 컬럼 추가
    df_chart = df.copy()
    df_chart['pnl_abs'] = df_chart['total_pnl'].abs()
    
    # 차트 1: 승률 vs 샤프 비율
    fig1 = px.scatter(
        df_chart,
        x='win_rate',
        y='sharpe_ratio',
        size='pnl_abs',
        color='style',
        hover_data=['name', 'total_trades', 'total_pnl'],
        title='승률 vs 샤프 비율 (버블 크기 = 총 수익 절대값)',
        labels={'win_rate': '승률 (%)', 'sharpe_ratio': '샤프 비율'}
    )
    fig1.update_layout(height=500)
    st.plotly_chart(fig1, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 차트 2: 거래 스타일별 평균 성과
        style_perf = df.groupby('style').agg({
            'win_rate': 'mean',
            'sharpe_ratio': 'mean',
            'total_pnl': 'sum'
        }).reset_index()
        
        fig2 = px.bar(
            style_perf,
            x='style',
            y='win_rate',
            title='거래 스타일별 평균 승률',
            labels={'style': '거래 스타일', 'win_rate': '평균 승률 (%)'}
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        # 차트 3: 경력별 샤프 비율
        fig3 = px.box(
            df,
            x='experience',
            y='sharpe_ratio',
            title='경력별 샤프 비율 분포',
            labels={'experience': '경력 (년)', 'sharpe_ratio': '샤프 비율'}
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    # 차트 4: 수익 분포
    fig4 = px.histogram(
        df,
        x='total_pnl',
        nbins=30,
        title='수익 분포',
        labels={'total_pnl': '총 수익 ($)'}
    )
    st.plotly_chart(fig4, use_container_width=True)

def show_trader_list(df):
    """트레이더 목록 탭"""
    st.subheader("📋 트레이더 상세 목록")
    
    # 정렬 옵션
    sort_by = st.selectbox(
        "정렬 기준",
        ['승률', '샤프 비율', '총 수익', 'MDD', '거래 횟수']
    )
    
    sort_map = {
        '승률': 'win_rate',
        '샤프 비율': 'sharpe_ratio',
        '총 수익': 'total_pnl',
        'MDD': 'max_drawdown_pct',
        '거래 횟수': 'total_trades'
    }
    
    sorted_df = df.sort_values(sort_map[sort_by], ascending=False)
    
    # 테이블 표시
    display_df = sorted_df[[
        'trader_id', 'name', 'style', 'risk', 'experience',
        'win_rate', 'sharpe_ratio', 'total_pnl', 'max_drawdown_pct', 'total_trades'
    ]].copy()
    
    display_df.columns = [
        'ID', '이름', '스타일', '리스크', '경력',
        '승률(%)', '샤프', '총수익($)', 'MDD(%)', '거래수'
    ]
    
    st.dataframe(
        display_df.style.format({
            '승률(%)': '{:.1f}',
            '샤프': '{:.2f}',
            '총수익($)': '${:,.0f}',
            'MDD(%)': '{:.1f}',
        }),
        use_container_width=True,
        height=600
    )

def show_chatbot(chatbot):
    """AI 챗봇 탭 - Claude 스타일 UI"""
    
    # 대화 히스토리 초기화
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # 웰컴 메시지
    if not st.session_state.chat_history:
        st.markdown("""
        ### 👋 트레이더 성과 분석 AI.
        
        50명의 트레이더 데이터를 분석하여 인사이트를 제공합니다.
        
        **💡 이런 질문을 해보세요:**
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 승률 상위 트레이더는?", use_container_width=True):
                st.session_state.pending_query = "승률이 가장 높은 트레이더 3명은?"
                st.rerun()
            if st.button("💰 수익 1위는?", use_container_width=True):
                st.session_state.pending_query = "총 수익이 가장 많은 트레이더는?"
                st.rerun()
        
        with col2:
            if st.button("🎯 샤프 비율 순위", use_container_width=True):
                st.session_state.pending_query = "샤프 비율 상위 3명 알려줘"
                st.rerun()
            if st.button("⚠️ 주의 필요 트레이더", use_container_width=True):
                st.session_state.pending_query = "MDD가 큰 트레이더들 분석해줘"
                st.rerun()
    
    # 대화 표시
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # pending 쿼리 처리
    if 'pending_query' in st.session_state:
        user_input = st.session_state.pending_query
        del st.session_state.pending_query
        
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        with st.spinner("🤔 분석 중..."):
            response = chatbot.process_query(user_input)
        
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()
    
    # 입력창 (하단 고정)
    user_input = st.chat_input("무엇이든 물어보세요...", key="chat_input")
    
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        with st.spinner("🤔 분석 중..."):
            response = chatbot.process_query(user_input)
        
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()

if __name__ == "__main__":
    main()
