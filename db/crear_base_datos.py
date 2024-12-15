import sqlite3
import os

DB_PATH = "db/costos_pedidos.db"

def crear_base_datos():
    if not os.path.exists("db"):
        os.makedirs("db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        tipo_tela TEXT,
        color TEXT,
        precio_base REAL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS materia_prima (
        id_materia INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        precio_unitario REAL,
        cantidad_disponible REAL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mano_obra (
        id_mano_obra INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT,
        costo_por_hora REAL,
        horas_por_unidad REAL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS costos_indirectos (
        id_costo_indirecto INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        valor REAL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ordenes_pedido (
        id_orden INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT,
        cantidad INTEGER,
        modelo TEXT,
        fecha_entrega DATE,
        costo_total REAL,
        precio_unitario REAL
    )
    """)
    conn.commit()
    conn.close()
    print("Base de datos creada con éxito.")

if __name__ == "__main__":
    crear_base_datos()
