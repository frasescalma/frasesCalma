import os
import random
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import textwrap

carpeta_imagenes = r"C:\TikTok\FrasesCalma\BaseImages"
carpeta_salida_base = r"C:\TikTok\FrasesCalma\Generadas"
fuente_path = r"C:\TikTok\FrasesCalma\Fonts\Roboto-Bold.ttf"
ruta_tabla = r"C:\TikTok\FrasesCalma\frases.csv"


# LEER LA TABLA
df = pd.read_csv(ruta_tabla)

# FUNCIONES
def crear_imagen_con_frase(imagen_path, frase, salida_path, fuente_path, font_size=60):
    imagen = Image.open(imagen_path).convert("RGBA")
    draw = ImageDraw.Draw(imagen)
    fuente = ImageFont.truetype(fuente_path, font_size)

    lines = textwrap.wrap(frase, width=25)
    total_height = 0
    line_heights = []

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=fuente)
        height = bbox[3] - bbox[1]
        line_heights.append(height + 10)
        total_height += height + 10

    y = (imagen.height - total_height) // 2

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=fuente)
        width = bbox[2] - bbox[0]
        x = max((imagen.width - width) // 2, 60)
        draw.text((x, y), line, font=fuente, fill="white")
        y += line_heights[i]

    imagen.save(salida_path)

# GENERAR IMÁGENES PARA CADA FILA
for index, row in df.iterrows():
    frase1 = str(row['Frase 1'])
    frase2 = str(row['Frase 2'])

    imagenes = [f for f in os.listdir(carpeta_imagenes) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not imagenes:
        print("No hay imágenes en la carpeta.")
        break

    imagen_aleatoria = random.choice(imagenes)
    imagen_path = os.path.join(carpeta_imagenes, imagen_aleatoria)

    # Crear carpeta para este post
    nombre_carpeta = f"post_{index+1:03d}"
    carpeta_post = os.path.join(carpeta_salida_base, nombre_carpeta)
    os.makedirs(carpeta_post, exist_ok=True)

    # Crear las imágenes
    crear_imagen_con_frase(imagen_path, frase1, os.path.join(carpeta_post, "1.png"), fuente_path)
    crear_imagen_con_frase(imagen_path, frase2, os.path.join(carpeta_post, "2.png"), fuente_path)
    df.at[index, 'Imagen'] = nombre_carpeta

    print(f"✅ Generado: {nombre_carpeta}")

df.to_csv(ruta_tabla, index=False)
