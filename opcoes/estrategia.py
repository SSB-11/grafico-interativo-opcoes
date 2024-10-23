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


    def calcular_custo(self):
        custo = 0
        for opcao in self.get_opcoes():
            if opcao.operacao == 'Compra':
                custo += (opcao.premio * opcao.quantidade)
            else:
                custo -= (opcao.premio * opcao.quantidade)
        return custo

    
    def calcular_perda_maxima(self):
        return np.min(self.calcular_payoff([0, np.inf]))
