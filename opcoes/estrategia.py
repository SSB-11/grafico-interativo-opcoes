import numpy as np

class Estrategia:
    def __init__(self):
        self._opcoes = []


    def get_opcoes(self):
        return self._opcoes


    def adicionar_opcao(self, opcao):
        self._opcoes.append(opcao)


    def remover_opcao(self, opcao):
        if opcao in self.get_opcoes():
            self._opcoes.remove(opcao)
            return True
        print('A opção especificada não está na estratégia.')
        return False 


    def limpar_estrategia(self):
        self._opcoes = []

        
    def calcular_payoff(self, preco_acao):
        payoff = 0
        for opcao in self.get_opcoes():
            payoff += opcao.calcular_payoff(preco_acao)
        return payoff


    def calcular_investimento(self):
        investimento = 0
        for opcao in self.get_opcoes():
            if opcao.operacao == 'Compra':
                investimento -= (opcao.premio * opcao.quantidade)
            else:
                investimento += (opcao.premio * opcao.quantidade)
        return investimento

    
    def calcular_perda_maxima(self, preco_acao):
        return np.min(self.calcular_payoff(preco_acao)).round(2)

    
    def calcular_ganho_maximo(self, preco_acao):
        return np.max(self.calcular_payoff(preco_acao)).round(2)
