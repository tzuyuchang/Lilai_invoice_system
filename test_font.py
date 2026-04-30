import os
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

fonts_to_try = [
    "C:\\Windows\\Fonts\\msjh.ttc",
    "C:\\Windows\\Fonts\\msjh.ttf",
    "C:\\Windows\\Fonts\\mingliu.ttc",
    "C:\\Windows\\Fonts\\simhei.ttf"
]

font_loaded = False
for path in fonts_to_try:
    if os.path.exists(path):
        try:
            pdfmetrics.registerFont(TTFont("ChineseFont", path))
            print(f"Successfully loaded font: {path}")
            font_loaded = True
            break
        except Exception as e:
            print(f"Failed to load {path}: {e}")

if not font_loaded:
    print("Could not load any Chinese font.")

c = canvas.Canvas("test.pdf")
if font_loaded:
    c.setFont("ChineseFont", 12)
    c.drawString(100, 100, "測試中文 Test")
c.save()
print("Saved test.pdf")
