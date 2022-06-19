import pandas as pd

# INGRESSO
ingresso_url = 'https://us-central1-raccoon-bi.cloudfunctions.net/psel_de_ingressos'
tabela_ingresso = pd.read_json(ingresso_url)

# SHOW
show_url = 'https://us-central1-raccoon-bi.cloudfunctions.net/psel_de_shows'
tabela_show_1 = pd.read_json(show_url)
tabela_show = tabela_show_1.transpose().reset_index().rename(columns={'index':'show'})

# COMPRA
compra_url = 'https://us-central1-raccoon-bi.cloudfunctions.net/psel_de_compras'
tabela_compra1 = pd.read_csv(compra_url)
tabela_compra = tabela_compra1.groupby(['nome','show'], as_index=False).sum()

#Criação da tabela geral
tabela_ingresso_show = pd.merge(tabela_ingresso, tabela_show, how='left', on= ['dia','mes','ano'])
tabela_compra_show = pd.merge(tabela_compra, tabela_show, how='left', on= ['show'])
tabela_geral = pd.merge(tabela_compra_show,tabela_ingresso_show, how='left', on= ['show', 'dia','mes','ano','nome'])
tabela_geral2 = pd.merge(tabela_ingresso_show,tabela_compra_show, how='left', on= ['show', 'dia','mes','ano','nome'])
#1. Qual a média de gastos de pessoas com ingresso Pista?
df_filtro = tabela_geral[tabela_geral.tipo == "Pista"]
df_filtro_2 = df_filtro[df_filtro.status == "Concluido"]
Questao1 = df_filtro_2["gastos"].mean()
print("QUESTÃO 1 - A média de gastos de pessoas com ingresso Pista é de: ", Questao1,'\n')
# Cálculo feito com pessoas que tiveram seu status de compra como Concluído e cadastradas no setor Pista.

#2. Quais pessoas não compareceram aos shows?
df_q2 = tabela_ingresso_show[tabela_ingresso_show.status == "Concluido"]
df_filtro1 = pd.merge(df_q2,tabela_compra_show, how='left', on= ['show','nome', 'dia','mes','ano'])
Questao2 = df_filtro1[df_filtro1['gastos'].isna()]
lista_q2 = list(Questao2['nome'])
print('QUESTAO 2 - Lista de pessoas que não compareceram aos shows:',lista_q2,'\n')

#3. Quais pessoas compraram ingressos com concorrentes?
lista_q3 = list(df_q2['nome'])
Questao3 = ~tabela_compra_show.nome.isin(lista_q3)
Q3 = tabela_compra_show[Questao3].drop_duplicates('nome')
lista_q3_final = list(Q3['nome'])
print('QUESTAO 3 - Lista de pessoas que compraram com concorrentes:', lista_q3_final,'\n')

#4. Qual o dia com maior gasto?
df_q4 = tabela_geral.groupby(['dia','ano','mes','show'], as_index=False).sum('gastos').max()
print('QUESTÃO 4 - Dia com maior gasto e valor total do dia:','\n',df_q4[['dia','gastos']],'\n')

#5. Faça uma lista com os clientes que desistiram de comprar o ingresso com a AT, a soma do valor que foi gasto durante
# os shows e quais shows eles desistiram de comprar.
df_tabela_geral2 = tabela_geral2.loc[:, ~tabela_geral2.columns.isin(['ano', 'mes','dia','tipo'])]
df_q5a = df_tabela_geral2.groupby(['nome','show','status'],dropna=True).sum().reset_index()
questao5= df_q5a[df_q5a['gastos'] != 0]
questao5['nomeshow'] = questao5['nome']+','+questao5['show']
Q5_1 = questao5[questao5.status == "Concluido"]
lista_q5 = list(Q5_1['nomeshow'])
tabela_Questao5 = ~questao5.nomeshow.isin(lista_q5)
Q5 = questao5[tabela_Questao5].drop_duplicates('nome')
questao5_final = Q5.loc[:, Q5.columns.isin(['nome','gastos','show'])]
ls = questao5_final.to_json(orient='records')
print('QUESTÃO 5 -' ,ls)