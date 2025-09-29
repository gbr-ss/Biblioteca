import sqlite3
conexao = sqlite3.connect("biblioteca.db")
cursor = conexao.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS alunos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    título TEXT NOT NULL,
    autor TEXT NOT NULL       
    ano INTEGER,
    disponivel TEXT CHECK(disponivel IN ('sim', 'não'))
        
                """)
