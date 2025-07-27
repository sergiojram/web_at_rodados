import sqlite3

# Conectamos con la base de datos
conn = sqlite3.connect('partes.db')
cursor = conn.cursor()

# Ejecutamos una consulta para ver los registros
cursor.execute("SELECT * FROM partes_tecnicos")
resultados = cursor.fetchall()

# Mostramos los resultados
print("📋 Registros guardados:")
for fila in resultados:
    print(fila)

conn.close()
