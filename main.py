import streamlit as st
import sqlite3
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
def adicionando(titulo,autor,ano):
    disponivel = "sim"
    cursor.execute("""
        INSERT INTO biblioteca (titulo, autor, ano, disponivel)
        VALUES (?, ?, ?, ?)
    """, (titulo, autor, ano, disponivel))
    conexao.commit()

def mostra_lista():
    cursor.execute("SELECT * FROM biblioteca")
    for linha in cursor.fetchall():
        st.write(f"ID: {linha[0]} | TITULO: {linha[1]} | AUTOR: {linha[2]} | ANO: {linha[3]} | DISPONIVEL: {linha[4]}")

def atualizar_banco():
    print(mostra_lista)

    id_livro = st.text_input("Digite o ID do livro que deseja atualizar: ")

    disponivel = st.text_input("O livro esta disponivel so resposta de 'sim' or 'não':")

    cursor.execute("""
    UPDATE biblioteca
    SET disponivel = ?
    WHERE id = ?    
    """,(disponivel, id_livro))

    conexao.commit()
    st.success("Status do livro atualizado") 
def deletar_banco():
    try:
        conexao = sqlite3.connect("biblioteca.db")
        cursor = conexao.cursor()
        mostra_lista()
        id_livro = st.number_input("Digite o id do livro que deseja deletar: ")
        cursor.execute("DELETE FROM biblioteca WHERE id = ?", (id_livro,))
        conexao.commit()
       
        if cursor.rowcount > 0:
            st.success("O livro foi removido com sucesso!")
        else:
            st.warning("Nenhum livro cadastrado com o ID fornecido")
    except Exception as erro:
        st.error(f"Erro ao tentar excluir o livro {erro}")
    finally:
        #Sempre fecha a conexão, com sucesso ou erro
        if conexao:
            conexao.close()

st.title("Bem vindo a minha biblioteca 2.0")
menu = st.sidebar.selectbox("Menu", ["Adicionar", "Listar", "Atualizar", "Deletar"])

if menu == "Adicionar":
    st.title("Cadastros para os livros📕")
    titulo = st.text_input("Digite o nome do livro que deseja cadastrar:")
    autor = st.text_input("Digite o nome do autor:")
    ano = st.number_input("Digite o ano de lançamento do livro:", step=1, format="%d")
    if st.button("Cadastrar livro📕"):
        if titulo and autor:
            adicionando(titulo, autor, ano)
            st.success("Livro cadastrado com sucesso!")
        else:
            st.warning("Preencha todos os campos antes de cadastrar.")
if menu == "Listar":
    st.title("livro cadastrados📕")
    cursor.execute("SELECT * FROM biblioteca")
    for linha in cursor.fetchall():
        st.write(f"ID: {linha[0]} | TITULO: {linha[1]} | AUTOR: {linha[2]} | ANO: {linha[3]} | DISPONIVEL: {linha[4]}")
