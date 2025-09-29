import streamlit as st
import sqlite3
@st.cache_resource
def conectar_db():
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS biblioteca(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,       
        ano INTEGER,
        disponivel TEXT CHECK(disponivel IN ('sim', 'não'))
        )
    """)
    conexao.commit()
    return conexao, cursor

conexao, cursor = conectar_db()

def adicionando(titulo,autor, ano):
    disponivel = "sim"
    cursor.execute("""
        INSERT INTO biblioteca (titulo, autor, ano, disponivel)
        VALUES (?, ?, ?, ?)
    """, (titulo, autor, ano, disponivel))
    conexao.commit()
    return True

def mostra_lista():
    cursor.execute("SELECT * FROM biblioteca")
    return cursor.fetchall()

def atualizar_banco(id_livro, disponivel):
    cursor.execute("""
        UPDATE biblioteca
        SET disponivel = ?
        WHERE id = ?    
        """, (disponivel, id_livro))
    conexao.commit()
    return cursor.rowcount > 0
def deletar_banco(id_livro):
    cursor.execute("DELETE FROM biblioteca WHERE id = ?", (id_livro,))
    conexao.commit()
    return cursor.rowcount > 0

st.title("Sistema de Gerenciamento de Biblioteca")
tab_adicionar, tab_mostrar, tab_atualizar, tab_deletar = st.tabs(["Adicionar Livro", "Mostrar Livros", "Atualizar Livro", "Deletar Livro"])
with tab_adicionar:
    st.header("Adicionar Novo Livro")
    with st.form("form_adicionar"):
        titulo = st.text_input("Digite o nome do livro que deseja cadastrar:")
        autor = st.text_input("Digite o nome do autor:")
        ano = st.number_input("Digite o ano de lançamento do livro:", min_value=1500, format="%d")

        submitted = st.form_submit_button("Cadastrar Livro")

        if submitted:
            if titulo and autor and ano:
                adicionando(titulo, autor, ano)
                st.success("Livro adicionado com sucesso!")
            else:
                st.error("Por favor, preencha todos os campos.")

with tab_mostrar:
    st.header("Lista de Livros")
    if st.button("Recarregar Lista"):
        dados = mostra_lista()
        if dados:
            st.table([["ID", "TITULO", "AUTOR", "ANO", "DISPONIVEL"]] + dados)
        else:
            st.warning("Nenhum livro cadastrado.")

with tab_atualizar:
    st.header("Atualizar Status de Livro")
    with st.form("form_atualizar"):
        id_livro_atualizar = st.number_input("Digite o ID do livro que deseja atualizar:", min_value=1, format="%d")
        novo_status = st.selectbox("Selecione a disponibilidade:", ["sim", "não"])
        submitted_atualizar = st.form_submit_button("Atualizar")

        if submitted_atualizar:
            if atualizar_banco(id_livro_atualizar, novo_status):
                st.success("Livro atualizado com sucesso!")
            else:
                st.warning("Nenhum livro encontrado com o ID fornecido.")

with tab_deletar:
    st.header("Excluir Livro")
    with st.form("form_deletar"):
        id_livro_deletar = st.number_input("Digite o ID do livro que deseja deletar:", min_value=1, format="%d")
        submitted_deletar = st.form_submit_button("Deletar")

        if submitted_deletar:
            if deletar_banco(id_livro_deletar):
                st.success("O livro foi removido com sucesso!")
            else:
                st.warning("Nenhum livro encontrado com o ID fornecido.")