import numpy as np

class Strategy:
    def __init__(self):
        self._options = []

    def get_options(self):
        return self._options

    def add_option(self, option):
        self._options.append(option)

    def remove_option(self, option):
        if option in self.get_options():
            self._options.remove(option)
            return True
        print('A opção especificada não está na estratégia.')
        return False 

    def clear_strategy(self):
        self._options = []

    def calculate_payoff(self, asset_price):
        payoff = 0
        for option in self.get_options():
            payoff += option.calculate_payoff(asset_price)
        return payoff

    def calculate_invested_amount(self):
        amount = 0
        for option in self.get_options():
            if option.trade_type == 'Compra':
                amount -= (option.premium * option.quantity)
            else:
                amount += (option.premium * option.quantity)
        return amount

    def calculate_maximum_loss(self, asset_price):
        return np.min(self.calculate_payoff(asset_price)).round(2)

    def calculate_maximum_profit(self, asset_price):
        return np.max(self.calculate_payoff(asset_price)).round(2)
