class Estrategia:
    def __init__(self):
        self._opcoes = []


    def adicionar_opcao(opcao):
        self._opcoes.append(opcao)


    def remover_opcao(opcao):
        try:
            self._opcoes.remove(opcao)
            return True
        except ValueError:
            print("A opção especificada não está na estratégia.")
            return False

    
    def calcular_payoff(preco_acao):
        payoff = 0
        for opcao in self._opcoes:
            payoff += opcao.calcular_payoff(preco_acao)
        return payoff
