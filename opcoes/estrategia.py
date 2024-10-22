class Estrategia:
    def __init__(self):
        self._opcoes = []


    def adicionar_opcao(self, opcao):
        self._opcoes.append(opcao)


    def remover_opcao(self, opcao):
        if opcao in self._opcoes:
            self._opcoes.remove(opcao)
            return True
        print("A opção especificada não está na estratégia.")
        return False 


    def get_opcoes(self):
        return self._opcoes

    
    def limpar_estrategia(self):
        self._opcoes = []

    
    def calcular_payoff(self, preco_acao):
        payoff = 0
        for opcao in self.get_opcoes():
            payoff += opcao.calcular_payoff(preco_acao)
        return payoff
