from PIL import Image, ImageDraw, ImageFont
from typing import cast

text = "PyMox.fr"
# ❌ Py bleu Mox blanc .fr rouge pour Pymox.fr
# text = "Cote7.com"
# font = ImageFont.truetype("arial.ttf", 40)
font = ImageFont.truetype("arial.ttf", 40)

# 1. Rendre le texte dans une image
img = Image.new("L", (600, 150), color=0)
draw = ImageDraw.Draw(img)
draw.text((10, 10), text, fill=255, font=font)

# 2. Rogner automatiquement autour du texte
bbox = img.getbbox()
img = img.crop(bbox)

# 3. Redimensionner pour lisibilité
img = img.resize((190, 13))

# 4. Convertir en ASCII binaire
print()
for y in range(img.height):
    line = ""
    for x in range(img.width):
        pixel = cast(int, img.getpixel((x, y)))
        if int(pixel) > 128:
            line += "\033[31;1m7\033[0m"
        else:
            line += " "
    print(line)
print()
