import os
import qrcode
from flask import url_for
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm


class ConfirmationService:
    def __init__(self, seat, reservation, output_dir, filename):
        self.seat = seat
        self.reservation = reservation
        self.output_dir = output_dir
        self.filename = filename

    def create_confirmation(self):
        # Initialize new_line variable
        qr_url = url_for('home.check_reservation', reservation_code=self.reservation.reservation_code, _external=True)

        new_line = 0

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Save QR code image
        img.save(os.path.join(self.output_dir, "qrcode.png"))

        # Create PDF with A4 paper size
        c = canvas.Canvas(os.path.join(self.output_dir, self.filename), pagesize=A4)
        width, height = A4

        # Add some text
        text = "Potvrda o rezervaciji"
        c.setFont("Helvetica", 22)
        c.drawString((width - c.stringWidth(text, "Helvetica", 22)) / 2, height - 2*cm, text)

        # Update new_line variable
        new_line += 18 + 2 * cm  # The height of the string is determined by the font size

        # Draw QR code on PDF
        qr_size = 4*cm
        c.drawImage(os.path.join(self.output_dir, "qrcode.png"), (width - qr_size)/2, height - qr_size - new_line, qr_size, qr_size)

        # Update new_line variable
        new_line += qr_size + 1*cm

        text = "Pozicija: " + self.seat.x_axis + self.seat.y_axis
        c.setFont("Helvetica", 18)
        c.drawString((width - c.stringWidth(text, "Helvetica", 18)) / 2, height - new_line, text)

        # Update new_line variable
        new_line += 18 + 1*cm

        text = f"Rezervacijski kod: {self.reservation.reservation_code}"
        c.setFont("Helvetica", 12)
        c.drawString((width - c.stringWidth(text, "Helvetica", 12))/2, height - new_line, text)

        # Update new_line variable
        new_line += 12 + 1*cm

        text = "Partner 1: " + self.reservation.partner_1
        c.setFont("Helvetica", 12)
        c.drawString((width - c.stringWidth(text, "Helvetica", 12)) / 2, height - new_line, text)

        # Update new_line variable
        new_line += 12 + 0.5 * cm

        text = "Partner 2: " + self.reservation.partner_2
        c.setFont("Helvetica", 12)
        c.drawString((width - c.stringWidth(text, "Helvetica", 12)) / 2, height - new_line, text)

        # Update new_line variable
        new_line += 12 + 1 * cm

        # Save PDF
        c.save()