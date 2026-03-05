from operator import is_
import os
from PIL import Image, ImageDraw, ImageFont
from typing import Any, cast

# Couleurs ANSI + RGB
BLUE = "\033[34;1m"
WHITE = "\033[37;1m"
RED = "\033[31;1m"
RESET = "\033[0m"

# Texte et groupes de couleurs
color_groups = [
    ("PyMoX", BLUE, (0, 120, 255)),
    ("-", WHITE, (255, 255, 255)),
    ("Kit", RED, (255, 0, 0)),
]

# Générer le texte et les segments à partir des groupes de couleurs
text = "".join(group_text for group_text, _, _ in color_groups)
text_upper = text.upper()  # Pour PILImage (font n'a que majuscules)

# Générer les segments (lettre_majuscule, couleur_ansi, couleur_rgb, est_majuscule_origine)
segments = []
for group_text, ansi, rgb in color_groups:
    for char in group_text:
        is_upper = char.isupper()
        is_important = True if char in "-" else False # Char. à mettre en '#
        segments.append((char.upper(), ansi, rgb, is_upper, is_important))

# Police BlockShadow
font_path = os.path.join(os.path.dirname(__file__), "BlockShadow-Bold.ttf")
font = ImageFont.truetype(font_path, 40)

# 1. Rendre le texte dans une image
img = Image.new("L", (600, 150), color=0)
draw = ImageDraw.Draw(img)
draw.text((10, 10), text_upper, fill=255, font=font)

# 2. Rogner automatiquement autour du texte
crop_box = img.getbbox()
if crop_box is None:
    raise RuntimeError("Aucun pixel de texte détecté pour le recadrage")
img = img.crop(crop_box)

# 3. Redimensionner pour lisibilité
try:
    resample_mode = Image.Resampling.NEAREST
except AttributeError:
    resample_mode = getattr(Image, "NEAREST")

img = img.resize((200, 15), resample_mode) # 200, 19

# img = img.point(lambda p: 255 if p > 128 else 0)

# --- Calcul des zones horizontales basé sur rendu réel ---
zones = []
base_x = 10  # même offset que draw.text((10, 10), ...)

# Utiliser la largeur avancée réelle (kerning inclus) pour éviter les fuites de couleur
boundaries = [base_x]
prefix = ""
for seg, _, _, _, _ in segments:
    prefix += seg
    boundaries.append(base_x + int(round(draw.textlength(prefix, font=font))))

# Adapter au crop + resize avec bornes contiguës garanties
crop_left = crop_box[0]
cropped_width_before_resize = crop_box[2] - crop_box[0]
resized_width = img.width  # largeur APRÈS crop + resize
scale = resized_width / cropped_width_before_resize

for index in range(len(segments)):
    start = int(round((boundaries[index] - crop_left) * scale))
    end = int(round((boundaries[index + 1] - crop_left) * scale))
    start = max(0, min(resized_width, start))
    end = max(start, min(resized_width, end))
    zones.append((start, end))

# Corriger les éventuels gaps/overlaps dus aux arrondis
for index in range(1, len(zones)):
    prev_start, _ = zones[index - 1]
    curr_start, curr_end = zones[index]
    zones[index - 1] = (prev_start, curr_start)
    zones[index] = (curr_start, curr_end)

if zones:
    first_start, first_end = zones[0]
    zones[0] = (0, first_end)
    last_start, _ = zones[-1]
    zones[-1] = (last_start, resized_width)

# --- AFFICHAGE CLI ASCII ---
print()
for y in range(img.height):
    line = ""
    for x in range(img.width):
        pixel = cast(int, img.getpixel((x, y)))
        color = RESET
        ascii_char = "7"
        in_zone = False

        # Trouver la couleur correspondant à la zone
        for (start, end), (seg_text, ansi, _, is_upper, is_important) in zip(zones, segments):
            if start <= x < end:
                # print (f'-------------- {seg_text} -------------')
                color = ansi
                ascii_char = "#" if (is_upper or is_important) else "7"
                in_zone = True
                break

        if pixel > 128 and in_zone:
            line += f"{color}{ascii_char}{RESET}"
        else:
            line += " "
    print(line)
print()

# --- GÉNÉRATION PNG IDENTIQUE AU RENDU ASCII ---
ascii_font = ImageFont.load_default()
cell_w, cell_h = 8, 13 # 8, 13

out = Image.new("RGBA", (img.width * cell_w, img.height * cell_h), (0, 0, 0, 0))
draw_out = ImageDraw.Draw(out)

for y in range(img.height):
    for x in range(img.width):
        pixel = cast(int, img.getpixel((x, y)))
        color_rgb = (255, 255, 255)
        ascii_char = "7"
        in_zone = False

        # Trouver la couleur RGB + caractère ASCII
        for (start, end), (seg_text, _, rgb, is_upper, is_important) in zip(zones, segments):
            if start <= x < end:
                color_rgb = rgb
                ascii_char = "#" if is_upper or is_important else "7"
                in_zone = True
                break

        if pixel > 128 and in_zone:
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
            for (start, end), (_, _, rgb, _, _) in zip(zones, segments):
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

# Sauvegarde PNG pour GH transparent BG
# final.save("pymox_shadow.png", format="PNG")
final.save(text + "_Logo.png", format="PNG") # Nom dynamique du fichier
