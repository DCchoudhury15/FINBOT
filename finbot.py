import re
import yfinance as yf
import ollama

def get_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        price = stock.info['regularMarketPrice']
        return price
    except Exception as e:
        print(f"Error fetching stock price for {symbol}: {e}")
        return None

def generate_summary(prices, user_input):
    prompt = f"User asked: '{user_input}'.\n"
    prompt += "Here are the current stock prices:\n"
    for symbol, price in prices.items():
        prompt += f"{symbol}: {price}\n"
    prompt += "Generate a helpful financial summary for this."

    response = ollama.chat(model='llama3', messages=[
        {'role': 'user', 'content': prompt}
    ])
    return response['message']['content']

def extract_symbols(user_input):
    # Basic symbol matcher (uppercase words 1-5 letters)
    return re.findall(r'\b[A-Z]{1,5}\b', user_input)

def main():
    print("📊 Welcome to FinBot! Ask me about any stock (example: 'Compare AAPL and TSLA'):")
    while True:
        user_input = input("\n🗣️  You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("👋 Goodbye!")
            break

        symbols = extract_symbols(user_input)
        if not symbols:
            print("❗ Please mention at least one stock symbol (like AAPL or TSLA).")
            continue

        prices = {}
        for symbol in symbols:
            price = get_stock_price(symbol)
            if price is not None:
                prices[symbol] = price
            else:
                prices[symbol] = "Unavailable"

        print("\n📈 Current Stock Prices:")
        for symbol, price in prices.items():
            print(f"   {symbol}: {price}")

        print("\n🧠 Generating summary...\n")
        summary = generate_summary(prices, user_input)
        print("FinBot:", summary)

if __name__ == "__main__":
    main()
