from codecs import ignore_errors
import os
from PIL import Image, ImageDraw, ImageFont
from typing import Any, cast

# Texte complet
text = "PyMoX.fr".upper()

# Segments et couleurs ANSI + RGB
BLUE = "\033[34;1m"
WHITE = "\033[37;1m"
RED = "\033[31;1m"
RESET = "\033[0m"

segments = [
    ("P", BLUE, (0, 120, 255)),
    ("Y", BLUE, (0, 120, 255)),
    ("M", WHITE, (255, 255, 255)),
    ("O", WHITE, (255, 255, 255)),
    ("X", WHITE, (255, 255, 255)),
    (".", WHITE, (255, 255, 255)),
    ("F", RED, (255, 0, 0)),
    ("R", RED, (255, 0, 0)),
]

# Police BlockShadow
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
for seg, _, _ in segments:
    b = font.getbbox(seg)
    w = b[2] - b[0]

    # Réduction de largeur pour les petites lettres
    # if seg not in ("P", "M", "X"):
    #     w = int(w * 0.6)

    widths.append(w)

total_width = sum(widths)
scale = img.width / total_width

zones = []
x = 0
for w in widths:
    zones.append((int(x * scale), int((x + w) * scale)))
    x += w

# --- AFFICHAGE CLI ASCII ---
print()
for y in range(img.height):
    line = ""
    for x in range(img.width):
        pixel = cast(int, img.getpixel((x, y)))

        # Trouver la couleur correspondant à la zone
        for (start, end), (seg_text, ansi, _) in zip(zones, segments):
            if start <= x < end:
                color = ansi
                ascii_char = "#" if seg_text in ("P", "M", "X") else "7"
                break

        if pixel > 128:
            line += f"{color}{ascii_char}{RESET}"
        else:
            line += " "
    print(line)
print()

# --- GÉNÉRATION PNG IDENTIQUE AU RENDU ASCII ---
ascii_font = ImageFont.load_default()
cell_w, cell_h = 8, 12

SMALL_SCALE = 0.6 # Pour les petites majuscules

out = Image.new("RGBA", (img.width * cell_w, img.height * cell_h), (0, 0, 0, 0))
draw_out = ImageDraw.Draw(out)
        # pixel = cast(int, img.getpixel((x, y)))

for y in range(img.height):
    for x in range(img.width):
        # pixel = img.getpixel((x, y))
        pixel = cast(int, img.getpixel((x, y)))

        # Trouver la couleur RGB + caractère ASCII
        for (start, end), (seg_text, _, rgb) in zip(zones, segments):
            if start <= x < end:
                color_rgb = rgb
                ascii_char = "#" if seg_text in ("P", "M", "X") else "7"
                break

        if pixel > 128:
            draw_out.text(
                (x * cell_w, y * cell_h), ascii_char, fill=color_rgb, font=ascii_font
            )

# --- ÉTAPE 1 : RENDRE LES PIXELS OPAQUES ---
pixels = cast(Any, out.load())
for y in range(out.height):
    for x in range(out.width):
        r, g, b, a = pixels[x, y]
        if a > 0:
            pixels[x, y] = (r, g, b, 255)

# --- ÉTAPE 2 : FORCER LES COULEURS EXACTES ---
for y in range(out.height):
    for x in range(out.width):
        r, g, b, a = pixels[x, y]
        if a > 0:
            for (start, end), (_, _, rgb) in zip(zones, segments):
                if start * cell_w <= x < end * cell_w:
                    pixels[x, y] = (rgb[0], rgb[1], rgb[2], 255)
                    break

# --- MARGE PROPORTIONNELLE + CENTRAGE ---
padding_x = cell_w // 2
padding_y = cell_h // 2

final_width = out.width + padding_x * 2
final_height = out.height + padding_y * 2

final = Image.new("RGBA", (final_width, final_height), (0, 0, 0, 0))

offset_x = (final_width - out.width) // 2
offset_y = padding_y

final.paste(out, (offset_x, offset_y), out)

# Sauvegarde PNG
final.save("pymox_shadow.png")
