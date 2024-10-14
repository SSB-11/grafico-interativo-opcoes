from abc import ABC, abstractmethod


class Opcao(ABC):
    def __init__(self, nome: str, strike: float, premio: float, operacao: str = 'Compra', quantidade: int = 100):
        """
        Inicializa uma nova instância da classe Opcao.
        
        Args:
        nome (str): Nome que identifica a opção.
        strike (float): Preço de exercício (strike).
        premio (float): Prêmio pago ou recebido pela opção.
        operacao (str): `Compra` ou `Venda` da opção (padrão é `Compra`).
        quantidade (int): Quantidade de opções compradas ou vendidas (padrão é 100).
        """
        self.nome = nome
        self.strike = strike
        self.premio = premio
        self.quantidade = quantidade
        self.operacao = operacao

        self.conferir_atributos()


    def conferir_atributos(self):
        "Checar se quantidade é um número inteiro positivo, strike é positivo, etc etc."
        pass


    @abstractmethod
    def calcular_preco_vencimento(self, preco_acao):
        pass


    def calcular_payoff(self, preco_acao):
        """
        Calcula o lucro ou prejuízo da opção, por cada opção negociada. Para achar o valor total calcule `payoff * quantidade`.
        - Quando uma opção é comprada, paga-se um prêmio.
        - Quando uma opção é vendida, recebe-se um prêmio.
        """
        if self.operacao == 'Compra':
            return self.quantidade * (self.calcular_preco_vencimento(preco_acao) - self.premio)
        if self.operacao == 'Venda':
            return self.quantidade * (self.premio - self.calcular_preco_vencimento(preco_acao))


    def __str__(self):
            """
            Retorna uma representação em string da opção.
            """
            return f"Strike: {self.strike}, Prêmio: {self.premio}, Quantidade: {self.quantidade}, Operação: {self.operacao}"
