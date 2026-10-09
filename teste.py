import streamlit as st

# 1. CONFIGURAÇÃO DA PÁGINA WEB
st.set_page_config(page_title="Sistema de Auditoria - Login", page_icon="🔒", layout="centered")

# FÓRMULA DE FORMATAÇÃO DE MOEDA BR
def formatar_real(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# FÓRMULA DE CONVERSÃO DE NÚMERO
def converter_para_numero(texto):
    try:
        limpo = texto.replace("R$", "").replace("%", "").replace(".", "").replace(",", ".").strip()
        return float(limpo)
    except:
        return 0.0

# TELA DE LOGIN PROFISSIONAL
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown("<h2 style='text-align: center;'>🔐 Painel de Acesso Restrito</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Insira as credenciais da concessionária para acessar a auditoria fiscal.</p>", unsafe_allow_html=True)
    
    usuario = st.text_input("Usuário do Sistema:")
    senha = st.text_input("Senha de Segurança:", type="password")
    
    if st.button("Acessar Painel 🚀", use_container_width=True):
        if usuario == "admin" and senha == "garagem123":
            st.session_state.autenticado = True
            st.success("Acesso autorizado com sucesso!")
            st.rerun()
        else:
            st.error("Usuário ou Senha incorretos. Tentativa registrada.")
else:
    # 🔓 SISTEMA COMPLETO AUTORIZADO
    st.sidebar.markdown("### 👤 Sessão Ativa")
    st.sidebar.write("Logado como: **Administrador**")
    if st.sidebar.button("🔒 Sair do Sistema"):
        st.session_state.autenticado = False
        st.rerun()

    st.title("🚗 Sistema de Auditoria - Loja de Carros")
    st.subheader("Gerenciamento Fiscal Detalhado, Margens e Fluxo de Estoque")
    st.write("---")

    # 2. ENTRADA DE DADOS DO VEÍCULO / PRODUTO
    st.markdown("### 📋 Dados do Automóvel")
    modelo_carro = st.text_input("Modelo e Ano do Veículo:", value="Honda Civic 2020")

    col1, col2, col3 = st.columns(3)
    with col1:
        txt_custo = st.text_input("Preço de COMPRA (Custo Unitário):", value="70.000,00")
    with col2:
        txt_venda = st.text_input("Preço de VENDA (Anúncio Unitário):", value="85.000,00")
    with col3:
        quantidade = st.number_input("Quantidade vendida:", min_value=1, value=1, step=1)

    col4, col5 = st.columns(2)
    with col4:
        txt_desconto = st.text_input("Desconto concedido ao cliente (%):", value="0,0%")
    with col5:
        txt_comissao = st.text_input("Comissão do Vendedor da Loja (%):", value="1,5%")

    # CUSTOS OCULTOS DE GARAGEM
    st.markdown("### 🛠️ Custos de Preparação e Pátio")
    col_cust1, col_cust2 = st.columns(2)
    with col_cust1:
        txt_preparacao = st.text_input("Gasto com Estética/Oficina (Polimento, Mecânica, Pintura):", value="1.200,00")
    with col_cust2:
        txt_patio = st.text_input("Custo Fixo Rateado de Pátio (Aluguel/Água/Luz por carro):", value="300,00")

    preco_custo = converter_para_numero(txt_custo)
    preco_venda = converter_para_numero(txt_venda)
    porcentagem_desconto = converter_para_numero(txt_desconto)
    taxa_comissao_vendedor = converter_para_numero(txt_comissao)
    gasto_preparacao = converter_para_numero(txt_preparacao)
    gasto_patio = converter_para_numero(txt_patio)

    st.write("---")

    # 3. LOGÍSTICA DE FRETE
    st.markdown("### 🚚 Logística de Entrega (Frete)")
    regiao_sugerida = st.selectbox(
        "Guia de Região (Sugestão de Preço):",
        ["Sudeste (Média: R$ 1.500,00)", "Sul (Média: R$ 2.250,00)", "Centro-Oeste (Média: R$ 2.800,00)", "Nordeste (Média: R$ 3.500,00)", "Norte (Média: R$ 4.200,00)"]
    )

    if "Sudeste" in regiao_sugerida: valor_sugerido = "1.500,00"
    elif "Sul" in regiao_sugerida: valor_sugerido = "2.250,00"
    elif "Centro-Oeste" in regiao_sugerida: valor_sugerido = "2.800,00"
    elif "Nordeste" in regiao_sugerida: valor_sugerido = "3.500,00"
    else: valor_sugerido = "4.200,00"

    txt_frete = st.text_input("Valor REAL do Frete Unitário Cobrado:", value=valor_sugerido)
    frete_final_unitario = converter_para_numero(txt_frete)

    st.write("---")

    # 4. ÁREA DOS IMPOSTOS SEPARADA
    st.markdown("### 🏛️ Configuração de Impostos do CNPJ")
    col_imp1, col_imp2 = st.columns(2)
    with col_imp1:
        txt_das = st.text_input("Quanto por cento de DAS (Imposto Federal)?", value="4,5%")
    with col_imp2:
        txt_icms = st.text_input("Quanto por cento de ICMS (Imposto Estadual)?", value="1,5%")

    porcentagem_das = converter_para_numero(txt_das)
    porcentagem_icms = converter_para_numero(txt_icms)

    st.write("---")

    # 5. TAXAS DE MAQUININHA
    st.markdown("### 💳 Configuração da Maquininha / Cartão")
    tipo_pagamento = st.radio("Qual foi a forma de pagamento no cartão?", ["Débito", "Crédito", "Dinheiro/Pix (Sem Taxa)"])

    if tipo_pagamento == "Débito":
        txt_cartao = st.text_input("Taxa Real do DÉBITO:", value="1,2%")
    elif tipo_pagamento == "Crédito":
        txt_cartao = st.text_input("Taxa Real do CRÉDITO:", value="3,5%")
    else:
        txt_cartao = "0,0%"

    taxa_cartao = converter_para_numero(txt_cartao)

    st.write("---")

    # 6. GESTÃO DE ESTOQUE
    st.markdown("### ⚙️ Reserva para o Estoque Novo")
    repor_estoque = st.radio("Deseja reservar dinheiro do caixa para o estoque novo?", ["Sim", "Não"])

    if repor_estoque == "Sim":
        sugestao_reserva = formatar_real(preco_custo * quantidade).replace("R$", "").strip()
        txt_reposicao = st.text_input("Digite o valor em dinheiro que deseja RESERVAR para o estoque novo:", value=sugestao_reserva)
        custo_total_reposicao = converter_para_numero(txt_reposicao)
    else:
        custo_total_reposicao = 0.0

    # 7. MATEMÁTICA FINANCEIRA AVANÇADA
    subtotal_venda_bruta = preco_venda * quantidade
    desconto_calculado = subtotal_venda_bruta * (porcentagem_desconto / 100)
    valor_final_veiculos = subtotal_venda_bruta - desconto_calculado

    frete_total = frete_final_unitario * quantidade
    valor_total_cliente = valor_final_veiculos + frete_total

    custo_total_inicial = preco_custo * quantidade
    custo_total_preparacao = gasto_preparacao * quantidade
    custo_total_patio = gasto_patio * quantidade

    lucro_bruto = valor_final_veiculos - custo_total_inicial
    comissao_vendedor = valor_final_veiculos * (taxa_comissao_vendedor / 100)

    valor_das_calculado = valor_final_veiculos * (porcentagem_das / 100)
    valor_icms_calculado = valor_final_veiculos * (porcentagem_icms / 100)
    imposto_total = valor_das_calculado + valor_icms_calculado

    taxa_intermediario = valor_total_cliente * (taxa_cartao / 100)

    despesas_operacionais = (custo_total_preparacao + custo_total_patio + 
                            comissao_vendedor + imposto_total + taxa_intermediario)
    
    lucro_liquido = valor_final_veiculos - custo_total_inicial - despesas_operacionais

    if valor_final_veiculos > 0:
        margem_porcentagem = (lucro_liquido / valor_final_veiculos) * 100
    else:
        margem_porcentagem = 0.0

    # 8. EXIBIÇÃO DO RELATÓRIO FINAL E DA NOTINHA
    if st.button("🚀 Gerar Auditoria Completa", type="primary"):
        st.write("---")
        aba_relatorio, aba_notinha = st.tabs(["📊 Relatório Detalhado", "🧾 Cupom de Auditoria (Notinha)"])
        
        with aba_relatorio:
            st.markdown("### Relatório Financeiro Classificado")
            st.write(f"**🚘 Veículo Avaliado:** {modelo_carro}")
            st.write(f"**🔢 Quantidade Comercializada:** {quantidade} unidades")
            st.write(f"**💵 Faturamento Bruto dos Veículos:** {formatar_real(valor_final_veiculos)}")
            st.write(f"**🚚 Valor do Frete de Entrega Total:** {formatar_real(frete_total)}")
            st.write(f"**🛍️ TOTAL FATURADO (Valor Total do Cliente):** {formatar_real(valor_total_cliente)}")
            st.write(f"**📈 Lucro Bruto Direto da Venda (Margem Bruta):** {formatar_real(lucro_bruto)}")
            st.write("---")
            
            st.markdown("#### 🏛️ Impostos Classificados (Saídas):")
            st.write(f"   - **DAS (Imposto Federal - {porcentagem_das}%):** {formatar_real(valor_das_calculado)}")
            st.write(f"   - **ICMS (Imposto Estadual - {porcentagem_icms}%):** {formatar_real(valor_icms_calculado)}")
            st.write(f"   - **Total de Tributos Fiscais Retidos:** {formatar_real(imposto_total)}")
            
            st.markdown(f"#### 💸 Custos Operacionais e Logística ({tipo_pagamento}):")
            st.write(f"   - Custo de Aquisição (Compra): {formatar_real(custo_total_inicial)}")
            st.write(f"   - Taxa de Intermediação de Cartão ({taxa_cartao}%): {formatar_real(taxa_intermediario)}")
            st.write(f"   - Comissão Separada do Vendedor ({taxa_comissao_vendedor}%): {formatar_real(comissao_vendedor)}")
            st.write(f"   - Gastos de Oficina/Preparação: {formatar_real(custo_total_preparacao)}")
            st.write(f"   - Custo de Manutenção de Pátio/Aluguel: {formatar_real(custo_total_patio)}")
            if repor_estoque == "Sim":
                st.write(f"   - *Reserva Sugerida para Novo Estoque:* {formatar_real(custo_total_reposicao)}")
            st.write("---")
            
            if lucro_liquido >= 0:
                st.success(f"💰 LUCRO LÍQUIDO REAL DA OPERAÇÃO: {formatar_real(lucro_liquido)} ({margem_porcentagem:.1f}% de margem líquida)")
            else:
                st.error(f"🚨 PREJUÍZO LÍQUIDO NA OPERAÇÃO: {formatar_real(lucro_liquido)} ({margem_porcentagem:.1f}% de margem líquida)")

        with aba_notinha:
            st.markdown("### 📝 Cupom de Auditoria Interna")
            notinha_texto = f"""
========================================
       AUDITORIA DE VENDA - VEÍCULOS    
========================================
VEÍCULO: {modelo_carro.upper()}
QTD: {quantidade} un
----------------------------------------
(+) FATUR. VEÍCULOS:   {formatar_real(valor_final_veiculos)}
(+) FRETE COBRADO:     {formatar_real(frete_total)}

(=) TOTAL RECEBIDO:    {formatar_real(valor_total_cliente)}


(-) CUSTO DO VEÍCULO:  {formatar_real(custo_total_inicial)}
(-) GASTO PREPARAÇÃO:  {formatar_real(custo_total_preparacao)}
(-) CUSTO DE PÁTIO:    {formatar_real(custo_total_patio)}
(-) COMISSÃO VENDEDOR: {formatar_real(comissao_vendedor)}
(-) IMP_FED DAS ({porcentagem_das}%):  {formatar_real(valor_das_calculado)}
(-) IMP_EST ICMS ({porcentagem_icms}%): {formatar_real(valor_icms_calculado)}
(-) TAXA MAQ. ({taxa_cartao}%):    {formatar_real(taxa_intermediario)}

========================================
LUCRO LÍQUIDO REAL:    {formatar_real(lucro_liquido)}
MARGEM LÍQUIDA:        {margem_porcentagem:.1f}%

AUDITORIA CONCLUÍDA
"""
            st.code(notinha_texto, language="text")