import pandas as pd
import numpy as np
from datetime import datetime
import json

class TradingPerformanceAnalyzer:
    """거래 성과 분석 클래스"""
    
    def __init__(self, transactions_file, profiles_file):
        self.transactions = pd.read_csv(transactions_file)
        self.profiles = pd.read_csv(profiles_file)
        self.transactions['datetime'] = pd.to_datetime(
            self.transactions['date'] + ' ' + self.transactions['time']
        )
        
    def calculate_trader_metrics(self, trader_id):
        """트레이더별 핵심 지표 계산"""
        trader_trades = self.transactions[self.transactions['trader_id'] == trader_id]
        
        # 매수/매도 매칭
        trades = []
        symbols = trader_trades['symbol'].unique()
        
        for symbol in symbols:
            symbol_trades = trader_trades[trader_trades['symbol'] == symbol].sort_values('datetime')
            buys = symbol_trades[symbol_trades['side'] == 'Buy']
            sells = symbol_trades[symbol_trades['side'] == 'Sell']
            
            for i in range(min(len(buys), len(sells))):
                buy = buys.iloc[i]
                sell = sells.iloc[i]
                
                pnl = sell['total_amount'] - buy['total_amount']
                hold_days = (sell['datetime'] - buy['datetime']).days
                
                trades.append({
                    'symbol': symbol,
                    'buy_date': buy['datetime'],
                    'sell_date': sell['datetime'],
                    'buy_price': buy['price'],
                    'sell_price': sell['price'],
                    'quantity': buy['quantity'],
                    'pnl': pnl,
                    'pnl_pct': (pnl / buy['total_amount']) * 100,
                    'hold_days': hold_days
                })
        
        if not trades:
            return None
            
        trades_df = pd.DataFrame(trades)
        
        # 핵심 지표 계산
        total_trades = len(trades_df)
        winning_trades = len(trades_df[trades_df['pnl'] > 0])
        losing_trades = len(trades_df[trades_df['pnl'] < 0])
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        avg_win = trades_df[trades_df['pnl'] > 0]['pnl'].mean() if winning_trades > 0 else 0
        avg_loss = abs(trades_df[trades_df['pnl'] < 0]['pnl'].mean()) if losing_trades > 0 else 0
        profit_factor = avg_win / avg_loss if avg_loss != 0 else 0
        
        # 샤프 비율 (연환산)
        returns = trades_df['pnl_pct']
        sharpe_ratio = (returns.mean() / returns.std() * np.sqrt(252)) if returns.std() != 0 else 0
        
        # MDD
        cumulative = trades_df['pnl'].cumsum()
        running_max = cumulative.expanding().max()
        drawdown = cumulative - running_max
        max_drawdown = drawdown.min()
        max_drawdown_pct = (max_drawdown / running_max.max() * 100) if running_max.max() != 0 else 0
        
        # 패턴 분석
        trades_df['hour'] = pd.to_datetime(trader_trades.iloc[:len(trades_df)]['time'].values).hour
        trades_df['weekday'] = trades_df['buy_date'].dt.day_name()
        
        return {
            'trader_id': trader_id,
            'total_trades': total_trades,
            'win_rate': round(win_rate, 2),
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'total_pnl': round(trades_df['pnl'].sum(), 2),
            'avg_return_pct': round(returns.mean(), 2),
            'avg_win': round(avg_win, 2),
            'avg_loss': round(avg_loss, 2),
            'profit_factor': round(profit_factor, 2),
            'sharpe_ratio': round(sharpe_ratio, 2),
            'max_drawdown': round(max_drawdown, 2),
            'max_drawdown_pct': round(max_drawdown_pct, 2),
            'avg_hold_days': round(trades_df['hold_days'].mean(), 1),
            'top_symbols': trades_df['symbol'].value_counts().to_dict()
        }
    
    def analyze_patterns(self, trader_id):
        """거래 패턴 분석"""
        trader_trades = self.transactions[self.transactions['trader_id'] == trader_id]
        
        hourly = trader_trades['time'].apply(lambda x: int(x.split(':')[0])).value_counts().to_dict()
        weekly = trader_trades['datetime'].dt.day_name().value_counts().to_dict()
        
        return {
            'trader_id': trader_id,
            'hourly_distribution': hourly,
            'weekly_distribution': weekly,
            'avg_position_size': round(trader_trades['total_amount'].mean(), 2),
            'most_active_hour': max(hourly, key=hourly.get),
            'most_active_day': max(weekly, key=weekly.get)
        }
    
    def generate_full_report(self, output_file='data/analysis_results.json'):
        """전체 트레이더 분석 리포트 생성"""
        results = {}
        
        for trader_id in self.transactions['trader_id'].unique():
            profile = self.profiles[self.profiles['trader_id'] == trader_id].iloc[0].to_dict()
            performance = self.calculate_trader_metrics(trader_id)
            pattern = self.analyze_patterns(trader_id)
            
            if performance:
                results[trader_id] = {
                    'profile': profile,
                    'performance': performance,
                    'pattern': pattern
                }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"[OK] Analysis complete: {len(results)} traders")
        print(f"[SAVED] {output_file}")
        return results

# 실행
if __name__ == "__main__":
    analyzer = TradingPerformanceAnalyzer(
        'data/trading_transactions_enhanced.csv',
        'data/trader_profiles_enhanced.csv'
    )
    results = analyzer.generate_full_report()
    
    # 샘플 출력
    for trader_id, data in list(results.items())[:2]:
        print(f"\n{'='*50}")
        print(f"Trader: {data['profile']['name']} ({trader_id})")
        print(f"Win Rate: {data['performance']['win_rate']}%")
        print(f"Sharpe Ratio: {data['performance']['sharpe_ratio']}")
