import os
from PIL import Image, ImageDraw, ImageFont
from typing import cast

# Texte complet
text = "PYMOX.FR"

# Segments et couleurs ANSI
BLUE = "\033[34;1m"
WHITE = "\033[37;1m"
RED = "\033[31;1m"
RESET = "\033[0m"

segments = [
    ("PY", BLUE),
    ("MOX.", WHITE),
    ("FR", RED),
]

# Police
font_path = os.path.join(os.path.dirname(__file__), "BlockShadow-Bold.ttf")
font = ImageFont.truetype(font_path, 40)

# 1. Rendre le texte dans une image
img = Image.new("L", (600, 150), color=0)
draw = ImageDraw.Draw(img)
draw.text((10, 10), text, fill=255, font=font)

# 2. Rogner automatiquement autour du texte
bbox = img.getbbox()
img = img.crop(bbox)

# 3. Redimensionner pour lisibilité
img = img.resize((190, 13))

# --- Calcul des zones horizontales ---
widths = []
for seg, _ in segments:
    b = font.getbbox(seg)
    w = b[2] - b[0]
    widths.append(w)

total_width = sum(widths)
scale = img.width / total_width

zones = []
x = 0
for w in widths:
    zones.append((int(x * scale), int((x + w) * scale)))
    x += w

# 4. Convertir en ASCII binaire
print()
for y in range(img.height):
    line = ""
    for x in range(img.width):
        pixel = cast(int, img.getpixel((x, y)))

        # Trouver la couleur correspondant à la zone
        for (start, end), (_, color) in zip(zones, segments):
            if start <= x < end:
                ansi = color
                break

        if pixel > 128:
            line += f"{ansi}7{RESET}"
        else:
            line += " "
    print(line)
print()
