#!/usr/bin/env python3
"""
🌐 SIMPLE TRADOVATE PROP FIRM WEB DASHBOARD
Access your trading signals from your phone!
"""

from flask import Flask, render_template, jsonify
import os
import time
from datetime import datetime
try:
    import yfinance as yf
except ImportError:
    yf = None

app = Flask(__name__)

class SimpleWebDashboard:
    def __init__(self):
        self.symbols = {
            'ES=F': 'ES',  # S&P 500 E-mini
            'NQ=F': 'NQ',  # NASDAQ E-mini  
            'YM=F': 'MYM', # Dow E-mini
            'GC=F': 'GC',  # Gold
            'MGC=F': 'MGC', # Micro Gold
            'BTC-USD': 'MBT' # Bitcoin (proxy for MBT)
        }
        self.latest_data = []
        
    def get_live_signals(self):
        """Get current market data and basic signals"""
        signals = []
        
        if not yf:
            # Fallback demo data if yfinance not available
            return self._get_demo_signals()
        
        for yahoo_symbol, display_symbol in self.symbols.items():
            try:
                ticker = yf.Ticker(yahoo_symbol)
                hist = ticker.history(period="1d", interval="5m")
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    
                    # Simple trend analysis
                    sma_20 = hist['Close'].rolling(20).mean().iloc[-1]
                    sma_50 = hist['Close'].rolling(50).mean().iloc[-1] if len(hist) >= 50 else sma_20
                    
                    # Determine direction
                    if current_price > sma_20 > sma_50:
                        direction = "LONG"
                        strength = 4
                        confidence = 85
                    elif current_price < sma_20 < sma_50:
                        direction = "SHORT" 
                        strength = 4
                        confidence = 85
                    elif current_price > sma_20:
                        direction = "LONG"
                        strength = 2
                        confidence = 65
                    elif current_price < sma_20:
                        direction = "SHORT"
                        strength = 2  
                        confidence = 65
                    else:
                        direction = "NEUTRAL"
                        strength = 1
                        confidence = 45
                    
                    # Calculate TP/SL
                    atr = (hist['High'] - hist['Low']).rolling(14).mean().iloc[-1]
                    
                    if direction == "LONG":
                        tp = current_price + (atr * 2)
                        sl = current_price - (atr * 1)
                    elif direction == "SHORT":
                        tp = current_price - (atr * 2)
                        sl = current_price + (atr * 1)
                    else:
                        tp = current_price + (atr * 0.5)
                        sl = current_price - (atr * 0.5)
                    
                    rr_ratio = abs(tp - current_price) / abs(current_price - sl) if abs(current_price - sl) > 0 else 2.0
                    
                    signals.append({
                        'symbol': display_symbol,
                        'price': f"${current_price:.2f}",
                        'direction': direction,
                        'strength': strength,
                        'confidence': f"{confidence}%",
                        'tp': f"${tp:.2f}",
                        'sl': f"${sl:.2f}",
                        'rr_ratio': f"{rr_ratio:.1f}:1",
                        'session': 'LIVE',
                        'timestamp': datetime.now().strftime('%H:%M:%S')
                    })
                    
            except Exception as e:
                print(f"Error getting data for {yahoo_symbol}: {e}")
                
        return signals
    
    def _get_demo_signals(self):
        """Fallback demo signals when yfinance unavailable"""
        demo_signals = []
        import random
        
        for yahoo_symbol, display_symbol in self.symbols.items():
            base_price = {"ES=F": 4500, "NQ=F": 16000, "YM=F": 35000, "GC=F": 2000, "MGC=F": 200, "BTC-USD": 45000}.get(yahoo_symbol, 1000)
            current_price = base_price + random.randint(-50, 50)
            
            directions = ["LONG", "SHORT", "NEUTRAL"]
            direction = random.choice(directions)
            strength = random.randint(1, 4)
            confidence = random.randint(65, 95)
            
            if direction == "LONG":
                tp = current_price + random.randint(20, 100)
                sl = current_price - random.randint(10, 50)
            elif direction == "SHORT":
                tp = current_price - random.randint(20, 100)
                sl = current_price + random.randint(10, 50)
            else:
                tp = current_price + random.randint(5, 25)
                sl = current_price - random.randint(5, 25)
            
            rr_ratio = abs(tp - current_price) / abs(current_price - sl) if abs(current_price - sl) > 0 else 2.0
            
            demo_signals.append({
                'symbol': display_symbol,
                'price': f"${current_price:.2f}",
                'direction': direction,
                'strength': strength,
                'confidence': f"{confidence}%",
                'tp': f"${tp:.2f}",
                'sl': f"${sl:.2f}",
                'rr_ratio': f"{rr_ratio:.1f}:1",
                'session': 'DEMO',
                'timestamp': datetime.now().strftime('%H:%M:%S')
            })
        
        return demo_signals
    
    def get_mtf_analysis(self):
        """Get simple multi-timeframe analysis"""
        mtf_data = []
        
        if not yf:
            return self._get_demo_mtf()
        
        for yahoo_symbol, display_symbol in self.symbols.items():
            try:
                ticker = yf.Ticker(yahoo_symbol)
                
                # Get different timeframes
                hist_1h = ticker.history(period="5d", interval="1h")
                hist_15m = ticker.history(period="2d", interval="15m") 
                hist_5m = ticker.history(period="1d", interval="5m")
                hist_1m = ticker.history(period="1d", interval="1m")
                
                def get_trend(data):
                    if data.empty or len(data) < 20:
                        return "NEUTRAL"
                    
                    sma_20 = data['Close'].rolling(20).mean().iloc[-1]
                    current = data['Close'].iloc[-1]
                    
                    if current > sma_20 * 1.001:
                        return "BULLISH"
                    elif current < sma_20 * 0.999:
                        return "BEARISH"
                    else:
                        return "NEUTRAL"
                
                trend_1h = get_trend(hist_1h)
                trend_15m = get_trend(hist_15m)
                trend_5m = get_trend(hist_5m)
                trend_1m = get_trend(hist_1m)
                
                # Determine alignment
                bullish_count = [trend_1h, trend_15m, trend_5m, trend_1m].count('BULLISH')
                bearish_count = [trend_1h, trend_15m, trend_5m, trend_1m].count('BEARISH')
                
                if bullish_count >= 3:
                    alignment = "STRONG BULL"
                    bias = "LONG BIAS"
                elif bearish_count >= 3:
                    alignment = "STRONG BEAR"
                    bias = "SHORT BIAS"
                elif bullish_count > bearish_count:
                    alignment = "WEAK BULL"
                    bias = "LONG LEAN"
                elif bearish_count > bullish_count:
                    alignment = "WEAK BEAR" 
                    bias = "SHORT LEAN"
                else:
                    alignment = "MIXED"
                    bias = "NO BIAS"
                
                mtf_data.append({
                    'symbol': display_symbol,
                    'trend_1h': trend_1h,
                    'trend_15m': trend_15m,
                    'trend_5m': trend_5m,
                    'trend_1m': trend_1m,
                    'alignment': alignment,
                    'bias': bias
                })
                
            except Exception as e:
                print(f"Error getting MTF for {yahoo_symbol}: {e}")
                
        return mtf_data
    
    def _get_demo_mtf(self):
        """Demo MTF data when yfinance unavailable"""
        import random
        trends = ["BULLISH", "BEARISH", "NEUTRAL"]
        alignments = ["STRONG BULL", "WEAK BULL", "MIXED", "WEAK BEAR", "STRONG BEAR"]
        
        demo_mtf = []
        for yahoo_symbol, display_symbol in self.symbols.items():
            trend_1h = random.choice(trends)
            trend_15m = random.choice(trends)
            trend_5m = random.choice(trends)
            trend_1m = random.choice(trends)
            alignment = random.choice(alignments)
            bias = "DEMO MODE" if "BULL" in alignment else "DEMO MODE"
            
            demo_mtf.append({
                'symbol': display_symbol,
                'trend_1h': trend_1h,
                'trend_15m': trend_15m,
                'trend_5m': trend_5m,
                'trend_1m': trend_1m,
                'alignment': alignment,
                'bias': bias
            })
        return demo_mtf
    
    def get_session_info(self):
        """Get current session information"""
        now = datetime.now()
        hour = now.hour
        
        if 4 <= hour < 9:
            session = "Pre-Market"
            volume = "Low"
            volatility = "Moderate"
            strategy = "Gap Analysis"
        elif 9 <= hour < 16:
            session = "Regular Hours"
            volume = "High"
            volatility = "High"
            strategy = "All Strategies"
        elif 16 <= hour < 20:
            session = "After Hours"
            volume = "Moderate"
            volatility = "Moderate"
            strategy = "News Reaction"
        else:
            session = "Overnight"
            volume = "Low"
            volatility = "Low"
            strategy = "Asia/Europe News"
        
        return {
            'session': session,
            'time': now.strftime('%H:%M:%S EST'),
            'volume_expectation': volume,
            'volatility': volatility,
            'best_symbols': 'ES, NQ, GC',
            'strategy_focus': strategy
        }

# Initialize dashboard
dashboard = SimpleWebDashboard()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/signals')
def api_signals():
    """API endpoint for live signals"""
    return jsonify(dashboard.get_live_signals())

@app.route('/api/mtf')
def api_mtf():
    """API endpoint for MTF analysis"""
    return jsonify(dashboard.get_mtf_analysis())

@app.route('/api/session')
def api_session():
    """API endpoint for session info"""
    return jsonify(dashboard.get_session_info())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🌐 Starting Simple Tradovate Web Dashboard...")
    print(f"📱 Running on port: {port}")
    print("💻 Dashboard starting...")
    app.run(host='0.0.0.0', port=port, debug=False)