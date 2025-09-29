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
biblioteca = [
   ("Enzo", "a", 2, "sim"),
    ("Murilo", "b", 3, "não"),
    ("Eduardo", "b", 4, "sim")
]

cursor.executemany("""
    INSERT INTO biblioteca (titulo, autor, ano, disponivel)
    VALUES (?, ?, ?, ?)
""", biblioteca)
conexao.commit()
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

def mostra_lista(linha):
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