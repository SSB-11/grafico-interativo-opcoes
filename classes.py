class Opcao:
    CALL = 'call'
    PUT = 'put'

    def __init__(self, tipo: str, strike: float, premio: float, quantidade: int = 100):
        """
        Inicializa uma nova instância da classe Opcao.
        
        Args:
        tipo (str): Tipo da opção (`Opcao.CALL` ou `Opcao.PUT`).
        strike (float): Preço de exercício (strike).
        premio (float): Prêmio pago pela opção.
        quantidade (int): Quantidade de contratos (padrão é 1).
        """
        if tipo.lower != Opcao.CALL.lower() and tipo.lower != Opcao.PUT.lower():
            raise ValueError(f'Tipo da Opção deve ser "{Opcao.CALL}" ou "{Opcao.PUT}". Tipo informado: "{tipo}" não é válido.')
        
        self.tipo = tipo.lower()
        self.strike = strike
        self.premio = premio
        self.quantidade = quantidade


    def __str__(self):
        """
        Retorna uma representação em string da opção.
        """
        return f"Opção {self.tipo.upper()} - Strike: {self.strike}, Prêmio: {self.premio}, Quantidade: {self.quantidade}"

