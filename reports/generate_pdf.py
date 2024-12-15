from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def generar_reporte_pdf(cliente, cantidad, modelo, resultados):
    file_name = f"reports/pedido_{cliente}.pdf"
    
    # Crear el documento y agregar un canvas
    c = canvas.Canvas(file_name, pagesize=letter)

    # Fondo rosa claro para la boleta
    c.setFillColor(colors.pink)  # Rosa suave para el fondo
    c.rect(0, 0, 612, 792, fill=1)  # Rectángulo que cubre toda la página

    # Título con fuente grande y color rosa oscuro
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(colors.darkviolet)  # Rosa oscuro para el título
    c.drawString(100, 750, "✨ Resumen del Pedido ✨")

    # Información del cliente y pedido
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.white)  # Blanco para resaltar
    c.drawString(100, 710, f"Cliente: {cliente}")
    c.drawString(100, 690, f"Modelo: {modelo}")
    c.drawString(100, 670, f"Cantidad: {cantidad}")

    # Detalles del costo con un toque de rosa
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.white)  # Blanco para el detalle
    c.drawString(100, 650, f"Costo Total: ${resultados['costo_total']:.2f}")
    c.drawString(100, 630, f"Precio Unitario: ${resultados['precio_unitario']:.2f}")
    
    # Verificar que 'detalle' existe antes de intentar acceder
    if 'detalle' in resultados:
        c.setFont("Helvetica-Oblique", 12)  # Fuente en cursiva para los detalles
        c.setFillColor(colors.pink)  # Rosa para los detalles
        c.drawString(100, 610, f"Materia Prima: ${resultados['detalle']['materia_prima']:.2f}")
        c.drawString(100, 590, f"Mano de Obra: ${resultados['detalle']['mano_obra']:.2f}")
        c.drawString(100, 570, f"Costos Indirectos: ${resultados['detalle']['costos_indirectos']:.2f}")
    else:
        c.setFont("Helvetica", 12)  # Fuente normal si 'detalle' no está
        c.setFillColor(colors.pink)
        c.drawString(100, 610, "Detalles de costos no disponibles.")

    # Línea divisoria con color rosa brillante
    c.setStrokeColor(colors.fuchsia)
    c.setLineWidth(2)
    c.line(100, 550, 500, 550)

    # Mensaje final con un toque especial
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.darkviolet)
    c.drawString(100, 520, "✨ Gracias por tu compra, ¡esperamos verte pronto! ✨")

    # Firmita de cierre
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.darkred)
    c.drawString(100, 500, "Tu tienda favorita ❤️")

    # Guardar el archivo PDF
    c.save()

    print(f"Reporte generado: {file_name}")
