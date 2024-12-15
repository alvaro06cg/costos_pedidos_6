def calcular_costos(modelo, cantidad):
    # Estos valores son ficticios. Reemplázalos con consultas reales a la base de datos.
    costo_materia_prima = 5.0  # Costo por unidad
    costo_mano_obra = 2.0  # Costo por unidad
    costo_indirecto = 1.0  # Costo por unidad

    # Calcular los costos
    materia_prima = costo_materia_prima * cantidad
    mano_obra = costo_mano_obra * cantidad
    costos_indirectos = costo_indirecto * cantidad
    costo_total = materia_prima + mano_obra + costos_indirectos
    precio_unitario = costo_total / cantidad

    resultados = {
        "costo_total": costo_total,
        "precio_unitario": precio_unitario,
        "detalle": {
            "materia_prima": materia_prima,
            "mano_obra": mano_obra,
            "costos_indirectos": costos_indirectos
        }
    }
    return resultados
