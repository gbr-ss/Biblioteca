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
    disponivel = "sim"  # Define o valor padrão para 'disponivel'
    cursor.execute("""
        INSERT INTO biblioteca (titulo, autor, ano, disponivel)
        VALUES (?, ?, ?, ?)
    """, (titulo, autor, ano, disponivel))
    conexao.commit()
