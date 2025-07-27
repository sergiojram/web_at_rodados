from flask import Flask, render_template, request, redirect, send_file
import sqlite3
from datetime import datetime
import io
from weasyprint import HTML

app = Flask(__name__)

# Ruta principal: mostrar el formulario
@app.route('/')
def formulario():
    # Opcional: lógica para generar número de planilla automáticamente
    conn = sqlite3.connect('partes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(planilla_id) FROM partes")
    ultimo_id = cursor.fetchone()[0]
    conn.close()
    nuevo_id = 1 if ultimo_id is None else ultimo_id + 1
    return render_template('formulario.html', numero_planilla=nuevo_id)

# Ruta para guardar los datos del formulario
@app.route('/guardar', methods=['POST'])
def guardar():
    try:
        planilla = request.form['planilla']
        horometro = request.form['horometro']

        # Validaciones básicas
        if not planilla.isdigit():
            return "❌ Error: N° de planilla debe ser un número entero"
        if not horometro.isdigit():
            return "❌ Error: Horómetro debe ser un número entero"

        datos = (
            int(planilla),
            request.form['cliente'],
            request.form['direccion'],
            request.form['modelo'],
            request.form['interno'],
            int(horometro),
            request.form['falla'],
            request.form['causa'],
            request.form['solucion'],
            datetime.now().strftime('%Y-%m-%d')
        )

        conn = sqlite3.connect('partes.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO partes 
            (planilla_id, cliente, direccion, modelo, interno, 
             horometro, falla, causa, solucion, fecha)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', datos)
        conn.commit()
        conn.close()
        return redirect('/')

    except Exception as e:
        return f"❌ Error al guardar los datos: {e}"

# Ruta para ver el historial filtrado por fecha
@app.route('/historial', methods=['GET'])
def historial():
    desde = request.args.get('desde')
    hasta = request.args.get('hasta')

    conn = sqlite3.connect('partes.db')
    cursor = conn.cursor()

    if desde and hasta:
        cursor.execute('''
            SELECT planilla_id, cliente, modelo, interno, horometro, falla, causa, solucion, fecha 
            FROM partes 
            WHERE fecha BETWEEN ? AND ?
            ORDER BY fecha DESC
        ''', (desde, hasta))
    else:
        cursor.execute('''
            SELECT planilla_id, cliente, modelo, interno, horometro, falla, causa, solucion, fecha 
            FROM partes 
            ORDER BY fecha DESC
        ''')

    registros = cursor.fetchall()
    conn.close()

    return render_template('historial.html', registros=registros, desde=desde, hasta=hasta)

# Ruta para generar PDF del historial completo
@app.route('/descargar_pdf')
def descargar_pdf():
    conn = sqlite3.connect('partes.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT planilla_id, cliente, modelo, interno, horometro, falla, causa, solucion, fecha 
        FROM partes 
        ORDER BY fecha DESC
    ''')
    registros = cursor.fetchall()
    conn.close()

    rendered = render_template('historial_pdf.html', registros=registros)
    pdf = HTML(string=rendered).write_pdf()

    return send_file(io.BytesIO(pdf), download_name="historial_partes.pdf", as_attachment=True)

# Ejecutar servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

