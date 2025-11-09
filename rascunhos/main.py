# Add unit tests later

# import numpy as np
# import matplotlib.pyplot as plt
# from opcoes.opcao import Call, Put

# print('Sucesso!')

# # Teste do cálculo de valor. Depois, testar o payoff com a quantidade negativa (venda) e positiva (compra) de cada.
# print('\nValor da Call')
# print(Call(12, 0.5, 100).calcular_preco_vencimento(14))
# print(Call(12, 0.5, 100).calcular_preco_vencimento(12.5))
# print(Call(12, 0.5, 100).calcular_preco_vencimento(10))
# print('\nPayoff da Call')
# print(Call(12, 0.5, 100).calcular_payoff(14))
# print(Call(12, 0.5, 100).calcular_payoff(12.5))
# print(Call(12, 0.5, 100).calcular_payoff(10))

# print('\nValor da Put')
# print(Put(12, 0.5, 100).calcular_preco_vencimento(14))
# print(Put(12, 0.5, 100).calcular_preco_vencimento(11.5))
# print(Put(12, 0.5, 100).calcular_preco_vencimento(10))
# print('\nPayoff da Put')
# print(Put(12, 0.5, -100).calcular_payoff(10))
# print(Put(12, 0.5, 100).calcular_payoff(12.5))
# print(Put(12, 0.5, 100).calcular_payoff(14))

# strike1 = 12
# premio_compra = 0.5
# strike2 = 14
# premio_venda = 0.2
# x = np.arange(strike1 - 1, strike2 + 1, 0.01)
# opcao1 = Call(strike1, premio_compra, 100)
# opcao2 = Call(strike2, premio_venda, -100)
# plt.figure(figsize=(6, 6))
# y = opcao1.calcular_payoff(x)
# plt.plot(x, opcao1.calcular_payoff(x) + opcao2.calcular_payoff(x))
# plt.axhline(0, color='black', lw=1)
# plt.savefig('teste_trava.png')