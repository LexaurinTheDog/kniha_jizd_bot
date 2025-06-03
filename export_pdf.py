from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def export_to_pdf(jizdy, filename="jizdy_export.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Přehled jízd")
    y -= 30
    c.setFont("Helvetica", 12)

    for j in jizdy:
        line = f"{j['odkud']} ➝ {j['kam']} ({j['km']} km) – {j['ucel']}"
        c.drawString(50, y, line)
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 12)

    c.save()
