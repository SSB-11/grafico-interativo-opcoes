import numpy as np
from abc import ABC, abstractmethod

class Option(ABC):
    def __init__(self, name: str, strike: float, premium: float, trade_type: str = 'Compra', quantity: int = 100):
        """
        Base option for all types (i.e. Call and Put).
        
        Args:
        name (str): Nome que identifica a opção.
        strike (float): Preço de exercício (strike).
        premium (float): Prêmio pago ou recebido pela opção.
        trade_type (str): `Compra` ou `Venda` da opção (padrão é `Compra`).
        quantity (int): quantity de opções compradas ou vendidas (padrão é 100).
        """
        self.name = name
        self.strike = strike
        self.premium = premium
        self.quantity = quantity
        self.trade_type = trade_type

        self.conferir_atributos()

    def conferir_atributos(self):
        "Checar se quantity é um número inteiro positivo, strike é positivo, etc etc."
        # todo
        pass

    @abstractmethod
    def calcular_preco_vencimento(self, asset_price):
        pass

    def calculate_payoff(self, asset_price):
        """
        Calcula o lucro ou prejuízo da opção, por cada opção negociada. Para achar o valor total calcule `payoff * quantity`.
        - Quando uma opção é comprada, paga-se um prêmio.
        - Quando uma opção é vendida, recebe-se um prêmio.
        """
        asset_price = np.array(asset_price)
        if self.trade_type == 'Compra':
            return self.quantity * (self.calcular_preco_vencimento(asset_price) - self.premium).round(2)
        if self.trade_type == 'Venda':
            return self.quantity * (self.premium - self.calcular_preco_vencimento(asset_price)).round(2)

    def get_data(self):
        """
        Retorna os dados da opção em formato de dicionário.
        """
        return {
            'name': self.name, 
            'type': self.type, 
            'strike': self.strike, 
            'premium': self.premium, 
            'quantity': self.quantity, 
            'trade_type': self.trade_type,
        }

    def describe(self):
        return f'({self.type}, Strike: {self.strike}, Prêmio: {self.premium}, Qtd: {self.quantity}, {self.trade_type})'

    def __str__(self):
            """
            Retorna uma representação em string da opção.
            """
            return f'{self.name}'

    def __eq__(self, other):
        if isinstance(other, Option):
            return self.__dict__ == other.__dict__
        return False
        