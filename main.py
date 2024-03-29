import pandas as pd
import plotly.express as px

pd.options.display.float_format = '{:,.2f}'.format

principal_df = pd.read_excel("acoes_puras.xlsx", sheet_name="principal")
ticker_df = pd.read_excel('acoes_puras.xlsx', sheet_name="ticker")
segmentos_chatgpt_df = pd.read_excel('acoes_puras.xlsx', sheet_name="segmentos_chatgpt")
total_de_acoes_df = pd.read_excel('acoes_puras.xlsx', sheet_name="total_de_acoes")
print("PRINCIPAL FRAME\n", principal_df)

principal_first4col_df = principal_df[["Ativo", "Data", "Último (R$)", "Var. Dia (%)"]].copy()
principal_refactor_dr = principal_first4col_df.rename(columns={
    "Ativo": "ativo",
    "Data": "data",
    "Último (R$)": "ultimo",
    "Var. Dia (%)": "var_dia_pct"
}).copy()

principal_refactor_dr["Var_pct"] = principal_refactor_dr["var_dia_pct"] / 100
principal_refactor_dr["Val_inicial"] = principal_refactor_dr["ultimo"] / (1 + principal_refactor_dr["Var_pct"])

principal_refactor_dr = principal_refactor_dr.merge(
    total_de_acoes_df, left_on="ativo", right_on="Código", how="left").drop(columns=["Código"])

principal_refactor_dr["Qtde. Teórica"] = principal_refactor_dr["Qtde. Teórica"].abs()

principal_refactor_dr = principal_refactor_dr.rename(columns={"Qtde. Teórica": "qtd_teorica"}).copy()

principal_refactor_dr["Variacao_rs"] = (
    principal_refactor_dr["ultimo"] - principal_refactor_dr["Val_inicial"]
) * principal_refactor_dr["qtd_teorica"]

print(principal_refactor_dr)

principal_refactor_dr["Resultado"] = (
    principal_refactor_dr["Variacao_rs"].apply(lambda x: 'Subiu' if x > 0 else ('Desceu' if x < 0 else 'Estável')))

principal_refactor_dr = principal_refactor_dr.merge(
    ticker_df, left_on="ativo", right_on="Ticker", how="left").drop(columns=["Ticker"])

principal_refactor_dr = principal_refactor_dr.merge(
    segmentos_chatgpt_df, left_on="Nome", right_on="Empresa", how="left").drop(columns=["Empresa"])

principal_refactor_dr = principal_refactor_dr.rename(columns={"Idade (em anos)": "idade"})

principal_refactor_dr["Faixa de idade"] = principal_refactor_dr["idade"].apply(
    lambda x: 'Centenaria' if x > 100 else ('Jovem' if x < 50 else 'Intermediaria')
)

# ANALISES
maior = principal_refactor_dr["Variacao_rs"].max()
menor = principal_refactor_dr["Variacao_rs"].min()
media = principal_refactor_dr["Variacao_rs"].mean()

media_subiu = principal_refactor_dr[principal_refactor_dr["Resultado"] == "Subiu"]["Variacao_rs"].mean()
media_desceu = principal_refactor_dr[principal_refactor_dr["Resultado"] == "Desceu"]["Variacao_rs"].mean()

principal_subiu_df = principal_refactor_dr[principal_refactor_dr["Resultado"] == "Subiu"]

analise_segmento_df = principal_subiu_df.groupby("Segmento")["Variacao_rs"].sum().reset_index()
analise_saldo_df = principal_refactor_dr.groupby("Resultado")["Variacao_rs"].sum().reset_index()
analise_catidade_df = principal_refactor_dr.groupby("Faixa de idade")["Variacao_rs"].sum().reset_index()

print(analise_catidade_df)

# GRAFICOS
saldo_graph = px.bar(
    analise_saldo_df,
    x="Resultado",
    y="Variacao_rs",
    text="Variacao_rs",
    title="Variacao RS por resultado",
)
saldo_graph.update_traces(texttemplate="R$ %{y:.2f}", textposition="outside")
saldo_graph.show()

segmento_graph = px.pie(
    analise_segmento_df,
    names="Segmento",
    values="Variacao_rs",
    labels="Segmento",
    title="Variacao RS por segmento",
)
segmento_graph.show()

catidade_graph = px.bar(
    analise_catidade_df,
    x="Faixa de idade",
    y="Variacao_rs",
    text="Variacao_rs",
    title="Variacao RS por Faixa de idade"
)
catidade_graph.show()
