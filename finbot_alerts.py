import time
import yfinance as yf
import ollama

# User-defined alerts: 'symbol': {'above': X, 'below': Y}
alerts = {
    'AAPL': {'above': 200, 'below': 170},
    'TSLA': {'above': 800, 'below': 600},
    'AMZN': {'above': 150, 'below': 110}
}

# Polling interval (seconds)
CHECK_INTERVAL = 60  # Check every 60 seconds

def get_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        return stock.info['regularMarketPrice']
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

def check_alerts():
    for symbol, conditions in alerts.items():
        price = get_price(symbol)
        if price is None:
            continue

        above = conditions.get('above')
        below = conditions.get('below')

        alert_triggered = False
        message = f"{symbol} is now at ${price:.2f}."

        if above and price > above:
            message += f" 📈 It's above your alert threshold of ${above}!"
            alert_triggered = True
        if below and price < below:
            message += f" 📉 It's below your alert threshold of ${below}!"
            alert_triggered = True

        if alert_triggered:
            print(f"\n🔔 ALERT: {message}")
            generate_response(symbol, price, message)

def generate_response(symbol, price, message):
    prompt = f"The current price of {symbol} is ${price:.2f}. {message} What action should a trader consider?"
    response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
    print("🧠 FinBot Advice:", response['message']['content'])

def main():
    print("🔁 FinBot Alert System Started. Monitoring prices every", CHECK_INTERVAL, "seconds.\n")
    while True:
        check_alerts()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
