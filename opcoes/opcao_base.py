from abc import ABC, abstractmethod


class Opcao(ABC):
    def __init__(self, strike: float, premio: float, quantidade: int = 100):
        """
        Inicializa uma nova instância da classe Opcao.
        
        Args:
        strike (float): Preço de exercício (strike).
        premio (float): Prêmio pago pela opção.
        quantidade (int): Quantidade de opções compradas (quantidade > 0) ou vendidas (quantidade < 0) (padrão é 100).
        """

        self.strike = strike
        self.premio = premio
        self.quantidade = quantidade

        self.conferir_atributos()


    def conferir_atributos(self):
        pass


    def __str__(self, tipo):
            """
            Retorna uma representação em string da opção.
            """
            return f"Strike: {self.strike}, Prêmio: {self.premio}, Quantidade: {self.quantidade}"
