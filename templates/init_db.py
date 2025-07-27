import sqlite3

conn = sqlite3.connect('partes.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS partes (
        planilla_id INTEGER PRIMARY KEY,
        cliente TEXT,
        direccion TEXT,
        modelo TEXT,
        interno TEXT,
        horometro INTEGER,
        falla TEXT,
        causa TEXT,
        solucion TEXT,
        fecha TEXT
    )
''')

conn.commit()
conn.close()
print("✅ Base de datos inicializada correctamente.")
