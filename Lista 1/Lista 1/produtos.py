import pandas as pd
import matplotlib.pyplot as plt

# Objetivo 1 - Carregar o CSV: Leia o arquivo vendas.csv para um DataFrame usando pandas.
df = pd.read_csv("vendas.csv")

#Objetivo 2 - Calcular o total de vendas por produto:
df['Total Vendas'] = df['Quantidade'] * df['Preco_Unitario']
df_group = df.groupby('Produto').agg({'Quantidade': 'sum', 'Total Vendas': 'sum'})
print(df_group)

#Opcional Crie um gráfico de barras para visualizar as vendas totais por produto.
#Utilize matplotlib para criar o gráfico de barras de vendas por produto:
plt.figure(figsize=(10, 6))  # Define o tamanho do gráfico

plt.bar(df_group.index, df_group['Total Vendas'])

plt.xlabel('Produto')
plt.ylabel('Total Vendas')
plt.title('Vendas Totais por Produto')

# Mostra o gráfico
plt.show()

"""
Objetivo 3
Filtrar vendas por data:
Filtre as vendas do mês de janeiro (1) de 2023 e crie um DataFrame separado com esses dados.
"""
df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
vendas_janeiro = df[df['Data'].dt.month == 1 & (df['Data'].dt.year == 2023)]
print(vendas_janeiro)

"""
Salvar os resultados:
Exporte o DataFrame filtrado para um novo arquivo CSV chamado vendas_janeiro.csv.
Salve o total de vendas por produto em uma nova planilha Excel chamada total_vendas_produto.xlsx, onde cada aba representa um produto com suas vendas.
"""
vendas_janeiro.to_csv("vendas_janeiro.csv")
df_group.to_excel("total_vendas_produto.xlsx")