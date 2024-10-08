import numpy as np
from .opcao_base import Opcao

class Call(Opcao):
    # tipo_ordem? tipo_operação? se qtd > ou < 0 (compra ou venda)
    # payoff por opção? valor total? porcentagem?
    # adicionar método para calcular o black&sholes?
    # criar uma classe separada Compra() e uma Venda() para calcular payoff? => Estrategia().adicionar_opcao(Compra(Call()))? Venda(Call()), Compra(Put())...? -> inverte o sinal do payoff?
    
    def calcular_preco_vencimento(self, preco_acao):
        """
        O valor da opção de compra no vencimento é `preco_acao - strike_opcao`.
        - Se a ação sobe, a opção também sobe (diretamente proporcional).

        Depois, multiplicado pela quantidade!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        Se a opção tiver sido comprada, o valor mínimo é zero. 
        Se a opção tiver sido vendida, o valor máximo é zero.
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11

        Calcula o preço da opção no vencimento, de acordo com o preço atual da ação.
        Args:
        preco_acao (np.array): Preço da ação no vencimento.
        """
        return np.maximum(preco_acao - self.strike, 0)


class Put(Opcao):
    def calcular_preco_vencimento(self, preco_acao):
        """
        O valor da opção de venda no vencimento é `strike_opcao - preco_acao`.
        - Se a ação sobe, a opção cai (inversamente proporcional).
        """
        return np.maximum(self.strike - preco_acao, 0)


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
