import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('partes.db')
cursor = conn.cursor()

# Intentar agregar la columna 'fecha'
try:
    cursor.execute("ALTER TABLE partes ADD COLUMN fecha TEXT")
    print("✅ Columna 'fecha' agregada con éxito.")
except sqlite3.OperationalError as e:
    print(f"⚠️ Ya existe la columna o hubo un error: {e}")

conn.commit()
conn.close()
