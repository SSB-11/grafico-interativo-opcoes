import numpy as np
from opcoes.estrategias import Call, Put, Estrategia

print('Sucesso!')

# Teste do cálculo de valor. Depois, testar o payoff com a quantidade negativa (venda) e positiva (compra) de cada.
print('\nValor da Call')
print(Call(12, 0.5, 100).calcular_preco_vencimento(14))
print(Call(12, 0.5, 100).calcular_preco_vencimento(12.5))
print(Call(12, 0.5, 100).calcular_preco_vencimento(10))

print('\n Valor da Put')
print(Put(12, 0.5, 100).calcular_preco_vencimento(14))
print(Put(12, 0.5, 100).calcular_preco_vencimento(11.5))
print(Put(12, 0.5, 100).calcular_preco_vencimento(10))
