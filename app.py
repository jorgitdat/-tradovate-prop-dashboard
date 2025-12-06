#!/usr/bin/env python3
"""
🌐 SIMPLE TRADOVATE PROP FIRM WEB DASHBOARD
Access your trading signals from your phone!
"""

from flask import Flask, render_template, jsonify
import os
import random
from datetime import datetime

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
        
    def get_live_signals(self):
        """Get demo trading signals"""
        signals = []
        
        for yahoo_symbol, display_symbol in self.symbols.items():
            base_price = {
                "ES=F": 4500, 
                "NQ=F": 16000, 
                "YM=F": 35000, 
                "GC=F": 2000, 
                "MGC=F": 200, 
                "BTC-USD": 45000
            }.get(yahoo_symbol, 1000)
            
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
            
            signals.append({
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
        
        return signals
    
    def get_mtf_analysis(self):
        """Get demo MTF data"""
        trends = ["BULLISH", "BEARISH", "NEUTRAL"]
        alignments = ["STRONG BULL", "WEAK BULL", "MIXED", "WEAK BEAR", "STRONG BEAR"]
        
        mtf_data = []
        for yahoo_symbol, display_symbol in self.symbols.items():
            trend_1h = random.choice(trends)
            trend_15m = random.choice(trends)
            trend_5m = random.choice(trends)
            trend_1m = random.choice(trends)
            alignment = random.choice(alignments)
            bias = "DEMO MODE"
            
            mtf_data.append({
                'symbol': display_symbol,
                'trend_1h': trend_1h,
                'trend_15m': trend_15m,
                'trend_5m': trend_5m,
                'trend_1m': trend_1m,
                'alignment': alignment,
                'bias': bias
            })
        return mtf_data
    
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

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Tradovate Dashboard is running!'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🌐 Starting Tradovate Dashboard...")
    print(f"📱 Port: {port}")
    app.run(host='0.0.0.0', port=port, debug=False)