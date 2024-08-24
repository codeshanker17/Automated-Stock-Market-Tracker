import yfinance as yf

def get_stock_data(symbol, start_date, end_date):
    stock = yf.Ticker(symbol)
    data = stock.history(start=start_date, end=end_date)
    return data

def get_current_price(symbol):
    stock = yf.Ticker(symbol)
    todays_data = stock.history(period='1d')
    if not todays_data.empty:
        return todays_data['Close'].iloc[0]
    return None  # Handle case when data is not available
