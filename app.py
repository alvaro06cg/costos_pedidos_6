from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from reports.generate_pdf import generar_reporte_pdf
from logic.calculations import calcular_costos
from logic.inventory import validar_inventario, actualizar_inventario

app = Flask(__name__)
app.secret_key = "clave_secreta"
DATABASE = "db/costos_pedidos.db"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/nuevo_pedido", methods=["GET", "POST"])
def nuevo_pedido():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM productos")
    productos = [row[0] for row in cursor.fetchall()]
    conn.close()

    resultados = None  # Inicializamos resultados como None

    if request.method == "POST":
        cliente = request.form.get("cliente")
        cantidad = int(request.form.get("cantidad", 0))
        modelo = request.form.get("modelo")
        fecha_entrega = request.form.get("fecha_entrega")
        accion = request.form.get("accion")

        if not cliente or not cantidad or not modelo or not fecha_entrega:
            flash("Todos los campos son obligatorios.")
            return redirect(url_for("nuevo_pedido"))

        # Realizar el cálculo de costos
        resultados = calcular_costos(modelo, cantidad)

        if accion == "calcular":
            # Mostrar los resultados del cálculo en el formulario
            return render_template("nuevo_pedido.html", productos=productos, resultados=resultados)

        if not validar_inventario(modelo, cantidad):
            flash("Inventario insuficiente para completar el pedido.")
            return redirect(url_for("nuevo_pedido"))

        # Registrar pedido y actualizar inventario
        actualizar_inventario(modelo, cantidad)
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO ordenes_pedido (cliente, cantidad, modelo, fecha_entrega, costo_total, precio_unitario)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (cliente, cantidad, modelo, fecha_entrega, resultados["costo_total"], resultados["precio_unitario"]))
        conn.commit()
        conn.close()

        generar_reporte_pdf(cliente, cantidad, modelo, resultados)
        flash("Pedido registrado y PDF generado correctamente.")
        return redirect(url_for("pedidos"))

    return render_template("nuevo_pedido.html", productos=productos, resultados=resultados)

@app.route("/pedidos")
def pedidos():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ordenes_pedido")
    pedidos = cursor.fetchall()
    conn.close()
    return render_template("pedidos.html", pedidos=pedidos)

@app.route("/enviar_reporte/<int:pedido_id>", methods=["GET"])
def enviar_reporte(pedido_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT cliente, cantidad, modelo, costo_total, precio_unitario FROM ordenes_pedido WHERE id_orden = ?", (pedido_id,))
    pedido = cursor.fetchone()
    conn.close()

    if not pedido:
        flash("Pedido no encontrado.")
        return redirect(url_for("pedidos"))

    cliente, cantidad, modelo, costo_total, precio_unitario = pedido
    resultados = {
        "costo_total": costo_total,
        "precio_unitario": precio_unitario
    }

    generar_reporte_pdf(cliente, cantidad, modelo, resultados)
    flash(f"Reporte generado para el pedido {pedido_id}.")
    return redirect(url_for("pedidos"))

@app.route("/admin/<tabla>", methods=["GET", "POST"])
def admin(tabla):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if tabla == "productos":
        if request.method == "POST":
            nombre = request.form["nombre"]
            tipo_tela = request.form["tipo_tela"]
            color = request.form["color"]
            precio_base = float(request.form["precio_base"])
            cursor.execute("""
            INSERT INTO productos (nombre, tipo_tela, color, precio_base)
            VALUES (?, ?, ?, ?)
            """, (nombre, tipo_tela, color, precio_base))
            conn.commit()
            flash("Producto agregado correctamente.")
        cursor.execute("SELECT * FROM productos")
        data = cursor.fetchall()
        columnas = ["ID", "Nombre", "Tipo Tela", "Color", "Precio Base"]

    elif tabla == "materias_primas":
        if request.method == "POST":
            nombre = request.form["nombre"]
            precio_unitario = float(request.form["precio_unitario"])
            cantidad_disponible = float(request.form["cantidad_disponible"])
            cursor.execute("""
            INSERT INTO materia_prima (nombre, precio_unitario, cantidad_disponible)
            VALUES (?, ?, ?)
            """, (nombre, precio_unitario, cantidad_disponible))
            conn.commit()
            flash("Materia prima agregada correctamente.")
        cursor.execute("SELECT * FROM materia_prima")
        data = cursor.fetchall()
        columnas = ["ID", "Nombre", "Precio Unitario", "Cantidad Disponible"]

    elif tabla == "mano_obra":
        if request.method == "POST":
            descripcion = request.form["descripcion"]
            costo_por_hora = float(request.form["costo_por_hora"])
            horas_por_unidad = float(request.form["horas_por_unidad"])
            cursor.execute("""
            INSERT INTO mano_obra (descripcion, costo_por_hora, horas_por_unidad)
            VALUES (?, ?, ?)
            """, (descripcion, costo_por_hora, horas_por_unidad))
            conn.commit()
            flash("Mano de obra agregada correctamente.")
        cursor.execute("SELECT * FROM mano_obra")
        data = cursor.fetchall()
        columnas = ["ID", "Descripción", "Costo por Hora", "Horas por Unidad"]

    elif tabla == "costos_indirectos":
        if request.method == "POST":
            nombre = request.form["nombre"]
            valor = float(request.form["valor"])
            cursor.execute("""
            INSERT INTO costos_indirectos (nombre, valor)
            VALUES (?, ?)
            """, (nombre, valor))
            conn.commit()
            flash("Costo indirecto agregado correctamente.")
        cursor.execute("SELECT * FROM costos_indirectos")
        data = cursor.fetchall()
        columnas = ["ID", "Nombre", "Valor"]

    else:
        conn.close()
        flash("Tabla no encontrada.")
        return redirect(url_for("index"))

    conn.close()
    return render_template(f"admin/{tabla}.html", data=data, columnas=columnas)

if __name__ == "__main__":
    app.run(debug=True)
