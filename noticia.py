import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime
import os

def create_news():
    title = simpledialog.askstring("Título", "Ingresa el título de la noticia:")
    subtitle = simpledialog.askstring("Subtítulo", "Ingresa el subtítulo:")
    text = simpledialog.askstring("Texto", "Ingresa el contenido completo de la noticia:")
    image_url = simpledialog.askstring("Imagen", "Ingresa el enlace de la imagen:")

    if not all([title, subtitle, text, image_url]):
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    date_obj = datetime.now()
    date_machine = date_obj.strftime("%Y-%m-%d")
    date_display = date_obj.strftime("%d-%B-%Y").replace('-', ' ')

    safe_title = title.replace(" ", "_").replace("/", "_")
    folder_name = f"{safe_title}_{date_display.replace(' ', '-')}"
    folder_path = os.path.join("noticia", folder_name)
    os.makedirs(folder_path, exist_ok=True)

    html_path = os.path.join(folder_path, "index.html")

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="stylesheet" href="../noticia.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Special+Gothic+Expanded+One&display=swap" rel="stylesheet">
</head>
<body>
  <div id="Barra_De_Status" class="status">
    <img src="../../logo.png" alt="logo">
    <ul>
      <li><a href="../../index.html" class="status">Inicio</a></li>
      <li><a href="../../galeria.html" class="status">Galería</a></li>
      <li><a href="../../acerca.html" class="status">Acerca</a></li>
      <li><a href="../../noticiero.html" class="status">noticiero</a></li>
      <li><a href="../../salidas.html" class="status">Salidas</a></li>
      <li><a href="../../contacto.html" class="status">Contacto</a></li>
    </ul>
  </div>

  <div style="padding: 2rem;">
    <h1 class="Titulo" style="font-family: 'Special Gothic Expanded One', sans-serif;">{title}</h1>
    <time datetime="{date_machine}">{date_display}</time>
    <h3 class="Subtitulo">{subtitle}</h3>
    <img src="../../{image_url}" alt="Imagen" style="max-width: 100%; margin-top: 1rem;">
    <p style="margin-top: 1rem;" class="Texto">{text}</p>
  </div>
</body>
</html>
""")

        preview_card = f"""
    <a href="noticia/{folder_name}/index.html" class="preview-card">
        <div class="card">
            <div class="card-text">
                <h2>{title}</h2>
                <p>{subtitle}</p>
            </div>
            <div class="card-image">
                <img src="{image_url}" alt="Imagen">
            </div>
        </div>
    </a>
"""

    with open("noticiero.html", "r", encoding="utf-8") as f:
        content = f.read()

    insert_point = content.find('<div id="dynamic-content">')
    if insert_point == -1:
        messagebox.showerror("Error", "No se pudo encontrar dónde insertar la noticia.")
        return
    insert_point += len('<div id="dynamic-content">')

    new_content = content[:insert_point] + preview_card + content[insert_point:]

    with open("noticiero.html", "w", encoding="utf-8") as f:
        f.write(new_content)

    messagebox.showinfo("Éxito", f"Noticia creada en '{folder_path}'.")

# UI
root = tk.Tk()
root.title("Crear Noticia")
root.geometry("300x150")
tk.Button(root, text="Crear nueva noticia", command=create_news, height=2, width=30).pack(pady=30)
root.mainloop()
