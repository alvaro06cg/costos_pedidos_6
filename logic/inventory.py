def validar_inventario(modelo, cantidad):
    inventario_disponible = 1000  # Reemplazar con consulta real
    return inventario_disponible >= cantidad

def actualizar_inventario(modelo, cantidad):
    print(f"Inventario actualizado para {modelo} con cantidad {cantidad}")
