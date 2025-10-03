import os
from typing import Dict, List, Optional
from pathlib import Path
from rag_system import TradingKnowledgeBase
from mcp_client import DesktopCommanderClient
import logging

# 로그 설정
logging.basicConfig(
    filename='chatbot_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(message)s'
)

class TraderAnalysisChatbot:
    """Trader Performance Analysis AI Chatbot"""
    
    def __init__(self, api_key: Optional[str] = None, provider: str = 'gemini', data_path: Optional[str] = None):
        self.provider = provider
        
        if provider == 'gemini':
            self.api_key = api_key or os.getenv('GEMINI_API_KEY')
            if not self.api_key:
                print("[WARNING] GEMINI_API_KEY not set. Using mock mode.")
                self.mock_mode = True
            else:
                self.mock_mode = False
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=self.api_key)
                    self.model = genai.GenerativeModel('gemini-2.0-flash')
                    print("[OK] Gemini API connected")
                except ImportError:
                    print("[ERROR] Install: pip install google-generativeai")
                    self.mock_mode = True
        else:
            self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
            self.mock_mode = not self.api_key
        
        # 데이터 경로 설정
        if data_path is None:
            base_dir = Path(__file__).parent.parent
            data_path = str(base_dir / 'data' / 'analysis_results_50.json')
        
        self.kb = TradingKnowledgeBase(data_path)
        self.mcp = DesktopCommanderClient()
        self.conversation_history = []
    
    def _analyze_intent(self, query: str) -> Dict:
        """강화된 의도 분석 - 타입, 메트릭, 필터 반환"""
        query_lower = query.lower()
        result = {
            'type': 'trader_query',
            'metric': None,
            'filter': None
        }
        
        # 메트릭 먼저 분석
        if any(w in query_lower for w in ['승률', 'win', 'rate']):
            result['metric'] = 'win_rate'
        elif any(w in query_lower for w in ['수익', 'profit', 'pnl', '손익']):
            result['metric'] = 'total_pnl'
        elif any(w in query_lower for w in ['mdd', '손실', 'drawdown', '낙폭']):
            result['metric'] = 'max_drawdown_pct'
        elif any(w in query_lower for w in ['샤프', 'sharpe']):
            result['metric'] = 'sharpe_ratio'
        elif any(w in query_lower for w in ['보유', 'hold', '기간']):
            result['metric'] = 'avg_hold_days'
        
        # 필터 분석
        if any(w in query_lower for w in ['높은', 'high', 'best', '많은', '긴', '큰']):
            result['filter'] = 'highest'
        elif any(w in query_lower for w in ['낮은', 'low', 'least', '적은', '짧은', '작은']):
            result['filter'] = 'lowest'
        elif any(w in query_lower for w in ['아침', 'morning', '9시', '10시']):
            result['filter'] = 'morning'
        elif any(w in query_lower for w in ['목요일', 'thursday']):
            result['filter'] = 'thursday'
        elif any(w in query_lower for w in ['안정', 'stable', '일관', 'consistent']):
            result['filter'] = 'stable'
        
        # 타입 분석 (메트릭과 필터를 고려)
        if any(w in query_lower for w in ['비교', '차이', 'compare', 'vs', 'difference']):
            result['type'] = 'comparison'
        elif any(w in query_lower for w in ['조언', '제안', '개선', 'advice', 'suggest', 'improve', '배워야', '학습']):
            result['type'] = 'advice'
        elif any(w in query_lower for w in ['패턴', '스타일', 'pattern', 'style', 'trend', '시간', '요일']) or result['filter'] in ['morning', 'thursday']:
            # 패턴 키워드 또는 시간/요일 필터 → pattern 타입 강제
            result['type'] = 'pattern'
        elif any(w in query_lower for w in ['상위', '순위', '랭킹', 'top', 'rank', 'best', '가장']) or (result['metric'] and result['filter']):
            result['type'] = 'ranking'
        
        return result
    
    def _search_data(self, query: str, intent: Dict) -> List[Dict]:
        """강화된 검색 로직 - 패턴 우선"""
        intent_type = intent['type']
        metric = intent['metric']
        filter_type = intent['filter']
        
        # 패턴 검색 우선 (이름보다 먼저)
        if intent_type == 'pattern' or filter_type in ['morning', 'thursday']:
            if filter_type == 'morning':
                return self.kb.search_by_time_pattern((9, 11))
            elif filter_type == 'thursday':
                return self.kb.search_by_weekday('Thursday')
            else:
                return self.kb.get_all_traders()
        
        # 랭킹 검색
        if intent_type == 'ranking':
            if not metric:
                metric = 'total_pnl'  # 기본값
            
            order = 'asc' if filter_type == 'lowest' else 'desc'
            return self.kb.search_by_metric_complex(metric, order, 3)
        
        # 비교
        elif intent_type == 'comparison':
            # 이름 추출 개선 (조사 제거)
            import re
            # "정지아와" → "정지아", "한서연을" → "한서연"
            # 조사 제거: 와, 과, 을, 를, 이, 가, 은, 는
            query_cleaned = re.sub(r'([가-힣]{2,4})(와|과|을|를|이|가|은|는)', r'\1 ', query)
            names = re.findall(r'[가-힣]{2,4}', query_cleaned)
            
            # 조사/동사 제거 (비교, 해줘 등)
            exclude_words = ['비교', '해줘', '알려', '분석', '차이', '어때']
            names = [n for n in names if n not in exclude_words]
            
            logging.info(f"Comparison - Query: {query}")
            logging.info(f"Cleaned: {query_cleaned}")
            logging.info(f"Found names: {names}")
            
            if len(names) >= 2:
                results = []
                for name in names[:2]:  # 최대 2명
                    trader = self.kb.search_by_trader(name)
                    if trader:
                        results.append(trader)
                        logging.info(f"Found trader: {trader['profile']['name']} ({trader['trader_id']})")
                    else:
                        logging.warning(f"Not found: {name}")
                
                if len(results) >= 2:
                    logging.info(f"Returning {len(results)} traders for comparison")
                    return results
                else:
                    logging.warning(f"Only found {len(results)} traders, need 2")
            
            # 이름 추출 실패 시 전체 중 첫 2명 반환
            logging.warning("Name extraction failed, using first 2")
            return self.kb.get_all_traders()[:2]
        
        # 트레이더 조회
        elif intent_type == 'trader_query':
            # "전체", "명단", "요약" 키워드 처리
            if any(w in query.lower() for w in ['전체', '명단', '리스트', '목록', '요약', 'all', 'list', 'summary']):
                return self.kb.get_all_traders()
            
            # T001, T002 등 ID 추출
            import re
            trader_id_match = re.search(r'T\d{3}', query.upper())
            if trader_id_match:
                trader_id = trader_id_match.group()
                result = self.kb.search_by_trader(trader_id)
                if result:
                    return [result]
            
            # ID 없으면 전체 쿼리로 검색
            result = self.kb.search_by_trader(query)
            if result:
                return [result]
            
            # 검색 실패 - 이름 추출하여 유사 이름 찾기
            import re
            # 한글 이름 추출 (2-4글자)
            name_match = re.search(r'[가-힣]{2,4}', query)
            if name_match:
                search_name = name_match.group()
                # 유사 이름 찾기
                similar_names = self.kb.find_similar_names(search_name, top_n=3)
                
                if similar_names:
                    # 유사 이름이 있으면 특별한 응답 생성
                    return [{
                        'not_found': True,
                        'search_name': search_name,
                        'similar_names': similar_names
                    }]
            
            # 검색 실패 시 필터 적용
            if filter_type == 'morning':
                return self.kb.search_by_time_pattern((9, 11))
            elif filter_type == 'thursday':
                return self.kb.search_by_weekday('Thursday')
            elif filter_type == 'stable':
                # 안정적 = 낮은 MDD
                return self.kb.search_by_metric_complex('max_drawdown_pct', 'asc', 3)
            
            # 아무것도 없으면 전체 반환
            return self.kb.get_all_traders()
        
        # 조언 (전체 데이터 필요)
        else:
            return self.kb.get_all_traders()
    
    def _build_prompt(self, query: str, context: List[Dict]) -> str:
        # 유사 이름 제안 처리
        if context and len(context) == 1 and context[0].get('not_found'):
            search_name = context[0]['search_name']
            similar_names = context[0]['similar_names']
            
            prompt = f"""You are a trading analyst. Answer in Korean.

[SITUATION]
The trader "{search_name}" was NOT found in the database.

[SIMILAR NAMES]
{', '.join(similar_names)}

[QUESTION]
{query}

[INSTRUCTIONS]
1. Answer in Korean
2. Explain that "{search_name}" is not in the database
3. Suggest the similar names found: {', '.join(similar_names)}
4. Ask if the user meant one of these traders
5. Be helpful and professional

Example:
"죄송합니다. '{search_name}' 트레이더는 데이터베이스에 없습니다.
유사한 이름으로는 {', '.join(similar_names)} 등이 있습니다.
혹시 이 중 한 분을 찾으시나요?"
"""
            return prompt
        
        # 디버깅
        logging.info(f"Context size: {len(context)}")
        if context:
            logging.info(f"First trader: {context[0]['profile']['name']}")
        
        context_text = ""
        for t in context:
            context_text += f"""
Trader: {t['profile']['name']} ({t.get('trader_id', 'N/A')})
- Style: {t['profile']['trading_style']}
- Win Rate: {t['performance']['win_rate']}%
- Sharpe: {t['performance']['sharpe_ratio']}
- P&L: ${t['performance']['total_pnl']}
- MDD: {t['performance']['max_drawdown_pct']}%
- Active: {t['pattern']['most_active_hour']}h, {t['pattern']['most_active_day']}
"""
        
        prompt = f"""You are a trading analyst. Answer in Korean.

[DATA]
{context_text}

[QUESTION]
{query}

[INSTRUCTIONS]
1. Answer in Korean
2. Use specific numbers
3. Provide insights
4. Be professional
"""
        return prompt
    
    def _generate_response(self, prompt: str) -> str:
        if self.mock_mode:
            return "[MOCK] API not configured."
        
        try:
            if self.provider == 'gemini':
                response = self.model.generate_content(prompt)
                return response.text
            else:
                import anthropic
                client = anthropic.Anthropic(api_key=self.api_key)
                msg = client.messages.create(
                    model="claude-sonnet-4-5-20250929",
                    max_tokens=2048,
                    messages=[{"role": "user", "content": prompt}]
                )
                return msg.content[0].text
        except Exception as e:
            return f"[ERROR] {e}"
    
    def process_query(self, user_query: str) -> str:
        intent = self._analyze_intent(user_query)
        results = self._search_data(user_query, intent)
        
        # 디버깅 로그
        logging.info(f"Query: {user_query}")
        logging.info(f"Intent: {intent}")
        logging.info(f"Results count: {len(results) if results else 0}")
        if results:
            logging.info(f"First result keys: {list(results[0].keys())}")
        
        if not results:
            return "[INFO] No matching traders."
        
        prompt = self._build_prompt(user_query, results)
        response = self._generate_response(prompt)
        
        self.conversation_history.append({
            'query': user_query, 'intent': intent, 'response': response
        })
        return response
    
    def get_history(self) -> List[Dict]:
        return self.conversation_history
