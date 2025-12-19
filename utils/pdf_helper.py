from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os


def save_booking_to_pdf(booking):
    os.makedirs("pdf", exist_ok=True)

    file_path = f"pdf/booking_{booking.booking_id}.pdf"
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    y = height - 50

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, y, "BUKTI BOOKING CONSOLE")
    y -= 40

    c.setFont("Helvetica", 12)
    data = [
        ("ID Booking", booking.booking_id),
        ("Username", booking.username),
        ("Room ID", booking.room_id),
        ("Console", booking.console),
        ("Waktu", ", ".join(booking.times)),
        ("Total Harga", f"Rp{booking.price}"),
        ("Tanggal", datetime.now().strftime("%d-%m-%Y %H:%M"))
    ]

    for label, value in data:
        c.drawString(50, y, f"{label} : {value}")
        y -= 20

    y -= 20
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, y, "Terima kasih telah melakukan booking.")

    c.save()

    return file_path
