import numpy as np
from .base_option import Option

class Call(Option):
    # type_ordem? type_operação? se qtd > ou < 0 (compra ou venda)
    # payoff por opção? valor total? porcentagem?
    # adicionar método para calcular o black&sholes?
    # criar uma classe separada Compra() e uma Venda() para calcular payoff? => Estrategia().adicionar_opcao(Compra(Call()))? Venda(Call()), Compra(Put())...? -> inverte o sinal do payoff?
    type = 'Call'

    def calcular_preco_vencimento(self, asset_price):
        """
        O valor da opção de compra no vencimento é `asset_price - strike`.
        - Se a ação sobe, a opção também sobe (diretamente proporcional).

        Depois, multiplicado pela quantidade!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        Se a opção tiver sido comprada, o valor mínimo é zero. 
        Se a opção tiver sido vendida, o valor máximo é zero.
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11

        Calcula o preço da opção no vencimento, de acordo com o preço atual da ação.
        Args:
        asset_price (np.array): Preço da ação no vencimento.
        """
        return np.maximum(asset_price - self.strike, 0).round(2)


class Put(Option):
    type = 'Put'
    
    def calcular_preco_vencimento(self, asset_price):
        """
        O valor da opção de venda no vencimento é `strike - asset_price`.
        - Se a ação sobe, a opção cai (inversamente proporcional).
        """
        return np.maximum(self.strike - asset_price, 0).round(2)
