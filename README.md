# Angel One F&O Breakout Scanner

A Python-based scanner that identifies high and low breakouts in NSE F&O stocks
using price action, RSI, and volume filters. Alerts are delivered via Telegram.

## Strategy Overview
- Lookback period: 5 trading days
- Indicator: RSI (14)
- Volume filter: Above 20-day average volume

### High Breakout Conditions
- Close > last 5 days high
- RSI ≥ 60
- Volume ≥ average volume

### Low Breakout Conditions
- Close < last 5 days low
- RSI ≤ 40
- Volume ≥ average volume

## Tech Stack
- Python
- Angel One SmartAPI
- Pandas, NumPy
- TA-Lib
- Telegram Bot API

## How It Works
1. Filter F&O stocks from all listed stock in NSE 
2. Fetches daily candle data
3. Applies breakout conditions
4. Sends alerts to Telegram Bot

## Setup Instructions
1. Clone the repository
2. Install dependencies:

         pip install -r requirements.txt
4. Add API credentials 
5. Run the script after market close
