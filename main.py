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

def atualizar_banco():
    try:
        print(mostra_lista)

        id_livro = input("Digite o ID do livro que deseja atualizar: ")

        disponivel = input("O livro esta disponivel so resposta de 'sim' or 'não':")

        cursor.execute("""
        UPDATE biblioteca
        SET disponivel = ?
        WHERE id = ?    
        """,(disponivel, id_livro))
        if cursor.rowcount > 0:
            print("O livro foi atualizado com sucesso!")
        else:
            print("Nenhum livro encontrado com o ID fornecido")
    except Exception as erro:
            print(f"Erro ao tentar atualizar o livro {erro}")
    finally:
        #Sempre fecha a conexão, com sucesso ou erro
        if conexao:
            conexao.close()

    conexao.commit()
    print("Status do livro atualizado") 
def deletar_banco():
    try:
        conexao = sqlite3.connect("biblioteca.db")
        cursor = conexao.cursor()
        mostra_lista()
        id_livro = int(input("Digite o id do livro que deseja deletar: "))
        cursor.execute("DELETE FROM biblioteca WHERE id = ?", (id_livro,))
        conexao.commit()
       
        if cursor.rowcount > 0:
            print("O livro foi removido com sucesso!")
        else:
            print("Nenhum livro cadastrado com o ID fornecido")
    except Exception as erro:
        print(f"Erro ao tentar excluir o livro {erro}")
    finally:
        #Sempre fecha a conexão, com sucesso ou erro
        if conexao:
            conexao.close()

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
