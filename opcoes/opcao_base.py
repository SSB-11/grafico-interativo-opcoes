from abc import ABC, abstractmethod


class Opcao(ABC):
    def __init__(self, strike: float, premio: float, quantidade: int = 100):
        """
        Inicializa uma nova instância da classe Opcao.
        
        Args:
        strike (float): Preço de exercício (strike).
        premio (float): Prêmio pago ou recebido pela opção.
        quantidade (int): Quantidade de opções compradas (quantidade > 0) ou vendidas (quantidade < 0) (padrão é 100).
        """

        self.strike = strike
        self.premio = premio
        self.quantidade = quantidade

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
        if self.quantidade > 0:
            return self.calcular_preco_vencimento(preco_acao) - self.premio
        if self.quantidade < 0:
            return self.premio - self.calcular_preco_vencimento(preco_acao)
        else: return 0


    def __str__(self, tipo):
            """
            Retorna uma representação em string da opção.
            """
            return f"Strike: {self.strike}, Prêmio: {self.premio}, Quantidade: {self.quantidade}"
