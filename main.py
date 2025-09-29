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
def adicionando():
    titulo = input("Digite o nome do livro que deseja cadastrar: ")
    autor = input("Digite o nome do autor:  ")
    ano = int(input("Digite o ano de lançamento do livro:  "))
    disponivel = "sim"
    cursor.execute("""
        INSERT INTO biblioteca (titulo, autor, ano, disponivel)
        VALUES (?, ?, ?, ?)
    """, (titulo, autor, ano, disponivel))
    conexao.commit()

def mostra_lista():
    cursor.execute("SELECT * FROM biblioteca")
    for linha in cursor.fetchall():
        print(f"ID: {linha[0]} | TITULO: {linha[1]} | AUTOR: {linha[2]} | ANO: {linha[3]} | DISPONIVEL: {linha[4]}")

def atualizar_banco():
    print(mostra_lista)

    id_livro = input("Digite o ID do livro que deseja atualizar: ")

    disponivel = input("O livro esta disponivel so resposta de 'sim' or 'não':")

    cursor.execute("""
    UPDATE biblioteca
    SET disponivel = ?
    WHERE id = ?    
    """,(disponivel, id_livro))

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
while True:
        
    pergunta=int(input("----------Menu----------\n1-Adicionar Livros\n2-Mostrar Livros\n3-Atualizar Livro\n4-Excluir Livro\n5-Sair\n----------Resposta----------\nR:"))
    if pergunta == 1:
        adicionando()
    if pergunta == 2:
        mostra_lista()
    if pergunta ==3:
        atualizar_banco()
    if pergunta == 4:
        deletar_banco()
    if pergunta == 5:
        break

