def should_buy(data, sma_short, sma_long, rsi):
    if data['Close'].iloc[-1] > sma_short.iloc[-1] > sma_long.iloc[-1] and rsi.iloc[-1] < 70:
        return True
    return False

def should_sell(data, sma_short, sma_long, rsi):
    if data['Close'].iloc[-1] < sma_short.iloc[-1] < sma_long.iloc[-1] and rsi.iloc[-1] > 30:
        return True
    return False

class Portfolio:
    def __init__(self, cash):
        self.cash = cash
        self.stocks = {}

    def buy(self, symbol, quantity, price):
        cost = quantity * price
        if cost <= self.cash:
            self.cash -= cost
            if symbol in self.stocks:
                self.stocks[symbol] += quantity
            else:
                self.stocks[symbol] = quantity
            return True
        return False

    def sell(self, symbol, quantity, price):
        if symbol in self.stocks and self.stocks[symbol] >= quantity:
            self.stocks[symbol] -= quantity
            self.cash += quantity * price
            if self.stocks[symbol] == 0:
                del self.stocks[symbol]
            return True
        return False

    def value(self, current_prices):
        stock_value = sum(self.stocks.get(symbol, 0) * current_prices.get(symbol, 0) for symbol in self.stocks)
        return self.cash + stock_value
