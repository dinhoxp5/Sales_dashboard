import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Sales Dashboard - Real Time")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("vendas.csv")

tabela = load_data()

# Sidebar - Add Sale
with st.sidebar:
    st.header("➕ Add New Sale")
    data_venda = st.date_input("Date", value=date.today())
    vendedor = st.selectbox("Salesperson", ["Ana", "Bruno", "Carla"])
    produto = st.selectbox("Product", ["Notebook", "Celular", "Fone"])
    quantidade = st.number_input("Quantity", min_value=1, step=1)
    valor = st.number_input("Total Value", min_value=0.0, step=100.0)
    botao = st.button("Add Sale", type="primary", use_container_width=True)

    if botao:
        if valor <= 0:
            st.error("Value must be greater than 0")
        else:
            nova_venda = {
                'data': str(data_venda),
                'vendedor': vendedor,
                'produto': produto,
                'quantidade': quantidade,
                'valor': valor
            }
            # concat é mais seguro que .loc[len(tabela)]
            tabela = pd.concat([tabela, pd.DataFrame([nova_venda])], ignore_index=True)
            tabela.to_csv("vendas.csv", index=False)
            st.success("✅ Sale added!")
            st.cache_data.clear()
            st.rerun()

# Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Revenue", f"$ {tabela['valor'].sum():,.2f}")
with col2:
    st.metric("Total Sales", len(tabela))
with col3:
    top_prod = tabela.groupby('produto')['valor'].sum().idxmax() if not tabela.empty else "-"
    st.metric("Top Product", top_prod)
with col4:
    top_seller = tabela.groupby('vendedor')['valor'].sum().idxmax() if not tabela.empty else "-"
    st.metric("Top Seller", top_seller)

# Charts
col_left, col_right = st.columns(2)
with col_left:
    st.subheader("Revenue by Salesperson")
    grafico = px.bar(tabela, x="vendedor", y="valor", color="produto", barmode="group", template="plotly_white")
    st.plotly_chart(grafico, use_container_width=True)

with col_right:
    st.subheader("Revenue by Product")
    grafico2 = px.pie(tabela, names="produto", values="valor", hole=0.4)
    st.plotly_chart(grafico2, use_container_width=True)

# Table - Versão Inglesa pro cliente
st.subheader("All Sales")
tabela_ingles = tabela.rename(columns={
    'data':'Date', 
    'vendedor':'Salesperson', 
    'produto':'Product', 
    'quantidade':'Qty', 
    'valor':'Value'
})
st.dataframe(tabela_ingles, use_container_width=True, height=400)
