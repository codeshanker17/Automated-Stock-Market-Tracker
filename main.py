import datetime
from stock_data import get_stock_data, get_current_price
from analysis import calculate_sma, calculate_rsi
from trading import should_buy, should_sell, Portfolio

def main():
    symbol = "AAPL"
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=365)
    
    # Fetch historical data
    data = get_stock_data(symbol, start_date, end_date)
    
    # Calculate indicators
    sma_short = calculate_sma(data, 20)
    sma_long = calculate_sma(data, 50)
    rsi = calculate_rsi(data, 14)
    
    # Initialize portfolio
    portfolio = Portfolio(10000)
    
    # Simulate trading
    for i in range(len(data)):
        if i < 50:  # Skip until we have enough data for long SMA
            continue
        
        current_data = data.iloc[:i+1]
        current_sma_short = sma_short.iloc[:i+1]
        current_sma_long = sma_long.iloc[:i+1]
        current_rsi = rsi.iloc[:i+1]
        current_price = current_data['Close'].iloc[-1]
        
        if should_buy(current_data, current_sma_short, current_sma_long, current_rsi):
            quantity = int(portfolio.cash // current_price)
            if quantity > 0:
                portfolio.buy(symbol, quantity, current_price)
                print(f"Bought {quantity} shares at {current_price:.2f}")
        
        elif should_sell(current_data, current_sma_short, current_sma_long, current_rsi):
            if symbol in portfolio.stocks:
                quantity = portfolio.stocks[symbol]
                portfolio.sell(symbol, quantity, current_price)
                print(f"Sold {quantity} shares at {current_price:.2f}")
    
    # Print final portfolio value
    current_price = get_current_price(symbol)
    if current_price:
        print(f"Final portfolio value: ${portfolio.value({symbol: current_price}):.2f}")
    else:
        print("Failed to retrieve the current price.")

if __name__ == "__main__":
    main()
