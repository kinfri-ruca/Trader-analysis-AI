import json
from typing import List, Dict, Optional

class TradingKnowledgeBase:
    """트레이더 성과 데이터 검색 시스템"""
    
    def __init__(self, json_path: str):
        with open(json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.traders = list(self.data.keys())
    
    def search_by_trader(self, query: str) -> Optional[Dict]:
        """트레이더 이름 또는 ID로 검색"""
        query = query.strip().upper()
        
        # ID로 검색
        if query in self.data:
            result = self.data[query].copy()
            result['trader_id'] = query
            return result
        
        # 이름으로 검색
        for trader_id, info in self.data.items():
            if query in info['profile']['name']:
                result = info.copy()
                result['trader_id'] = trader_id
                return result
        
        return None
    
    def search_by_metric(self, metric: str, threshold: float, operator: str = '>') -> List[Dict]:
        """성과 지표로 필터링"""
        results = []
        
        for trader_id, info in self.data.items():
            value = info['performance'].get(metric)
            if value is None:
                continue
            
            if operator == '>' and value > threshold:
                results.append({**info, 'trader_id': trader_id})
            elif operator == '<' and value < threshold:
                results.append({**info, 'trader_id': trader_id})
            elif operator == '==' and value == threshold:
                results.append({**info, 'trader_id': trader_id})
        
        return results
    
    def get_top_performers(self, metric: str, top_n: int = 3, ascending: bool = False) -> List[Dict]:
        """상위 성과자 조회"""
        traders_with_metric = []
        
        for trader_id, info in self.data.items():
            value = info['performance'].get(metric)
            if value is not None:
                traders_with_metric.append({
                    'trader_id': trader_id,
                    'value': value,
                    'data': info
                })
        
        # 정렬
        sorted_traders = sorted(traders_with_metric, key=lambda x: x['value'], reverse=not ascending)
        return [item['data'] for item in sorted_traders[:top_n]]
    
    def compare_traders(self, trader1_query: str, trader2_query: str) -> Optional[Dict]:
        """두 트레이더 비교"""
        t1 = self.search_by_trader(trader1_query)
        t2 = self.search_by_trader(trader2_query)
        
        if not t1 or not t2:
            return None
        
        return {
            'trader1': t1,
            'trader2': t2,
            'comparison': {
                'win_rate_diff': t1['performance']['win_rate'] - t2['performance']['win_rate'],
                'sharpe_diff': t1['performance']['sharpe_ratio'] - t2['performance']['sharpe_ratio'],
                'pnl_diff': t1['performance']['total_pnl'] - t2['performance']['total_pnl']
            }
        }
    
    def search_by_pattern(self, pattern_key: str, pattern_value: str) -> List[Dict]:
        """거래 패턴으로 검색"""
        results = []
        
        for trader_id, info in self.data.items():
            patterns = info.get('pattern', {})
            
            if pattern_key in patterns:
                if str(patterns[pattern_key]) == pattern_value:
                    results.append({**info, 'trader_id': trader_id})
        
        return results
    
    def search_by_time_pattern(self, hour_range: tuple) -> List[Dict]:
        """시간대별 검색 (예: (9, 11) = 9시~11시)"""
        results = []
        
        for trader_id, info in self.data.items():
            active_hour = info.get('pattern', {}).get('most_active_hour')
            if active_hour and hour_range[0] <= active_hour <= hour_range[1]:
                results.append({**info, 'trader_id': trader_id})
        
        return results
    
    def search_by_weekday(self, day: str) -> List[Dict]:
        """요일별 검색 (예: 'Monday', 'Thursday')"""
        results = []
        
        for trader_id, info in self.data.items():
            active_day = info.get('pattern', {}).get('most_active_day')
            if active_day and day.lower() in active_day.lower():
                results.append({**info, 'trader_id': trader_id})
        
        return results
    
    def search_by_metric_complex(self, metric: str, order: str = 'desc', top_n: int = 3) -> List[Dict]:
        """모든 지표 검색 지원 (order: 'desc'=높은순, 'asc'=낮은순)"""
        ascending = (order == 'asc')
        return self.get_top_performers(metric, top_n, ascending)
    
    def get_pattern_traders(self, pattern_key: str, pattern_value) -> List[Dict]:
        """패턴 기반 필터링 (유연한 값 비교)"""
        results = []
        
        for trader_id, info in self.data.items():
            pattern_val = info.get('pattern', {}).get(pattern_key)
            if pattern_val == pattern_value:
                results.append({**info, 'trader_id': trader_id})
        
        return results
    
    def get_all_traders(self) -> List[Dict]:
        """모든 트레이더 정보"""
        return [{'trader_id': tid, **data} for tid, data in self.data.items()]
    
    def find_similar_names(self, query: str, top_n: int = 3) -> List[str]:
        """유사한 이름 찾기 (간단한 문자열 매칭)"""
        query_clean = query.strip()
        
        # 모든 트레이더 이름 추출
        all_names = [info['profile']['name'] for info in self.data.values()]
        
        # 유사도 계산 (공통 문자 개수)
        similarities = []
        for name in all_names:
            # 공통 문자 개수
            common_chars = sum(1 for c in query_clean if c in name)
            # 길이 차이 페널티
            length_diff = abs(len(name) - len(query_clean))
            # 점수 = 공통문자 - 길이차이*0.5
            score = common_chars - (length_diff * 0.5)
            
            similarities.append((name, score))
        
        # 점수 높은 순으로 정렬
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # 상위 N개 반환 (점수 > 0만)
        result = [name for name, score in similarities[:top_n] if score > 0]
        return result
    
    def build_context(self, query: str, search_results: List[Dict]) -> Dict:
        """검색 결과를 컨텍스트로 변환"""
        if not search_results:
            return {'query': query, 'results': [], 'count': 0}
        
        context = {
            'query': query,
            'count': len(search_results),
            'traders': []
        }
        
        for result in search_results:
            trader_context = {
                'id': result.get('trader_id'),
                'name': result['profile']['name'],
                'style': result['profile']['trading_style'],
                'performance': {
                    'win_rate': result['performance']['win_rate'],
                    'sharpe_ratio': result['performance']['sharpe_ratio'],
                    'total_pnl': result['performance']['total_pnl'],
                    'max_drawdown_pct': result['performance']['max_drawdown_pct']
                },
                'pattern': {
                    'most_active_hour': result['pattern']['most_active_hour'],
                    'most_active_day': result['pattern']['most_active_day']
                }
            }
            context['traders'].append(trader_context)
        
        return context

# 테스트
if __name__ == "__main__":
    kb = TradingKnowledgeBase('data/analysis_results.json')
    
    print("=== RAG System Test ===\n")
    
    # Test 1: 트레이더 검색
    print("1. Search by name:")
    result = kb.search_by_trader("T001")
    if result:
        print(f"   Found: {result['profile']['name']}, Win Rate: {result['performance']['win_rate']}%")
    
    # Test 2: 상위 성과자
    print("\n2. Top 3 by Sharpe Ratio:")
    top3 = kb.get_top_performers('sharpe_ratio', 3)
    for i, trader in enumerate(top3, 1):
        print(f"   {i}. {trader['profile']['name']}: {trader['performance']['sharpe_ratio']}")
    
    # Test 3: 필터링
    print("\n3. Win Rate > 90%:")
    high_win = kb.search_by_metric('win_rate', 90, '>')
    for trader in high_win:
        print(f"   {trader['profile']['name']}: {trader['performance']['win_rate']}%")
    
    print("\n[OK] RAG System ready")
