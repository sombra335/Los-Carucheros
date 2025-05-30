import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
import os
import shutil
from datetime import datetime

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NOTICIAS_DIR = os.path.join(BASE_DIR, "noticias")
NOTICIERO_HTML = os.path.join(BASE_DIR, "noticiero.html")

def copy_image(src_path, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    filename = os.path.basename(src_path)
    dest_path = os.path.join(dest_dir, filename)
    shutil.copy2(src_path, dest_path)
    return filename

def create_new():
    # 1. Ask for title, subtitle, text
    title = simpledialog.askstring("Título", "Introduce el título de la noticia:")
    if not title: return
    subtitle = simpledialog.askstring("Subtítulo", "Introduce el subtítulo de la noticia:")
    if subtitle is None: return
    text = simpledialog.askstring("Texto", "Introduce el texto de la noticia:")
    if text is None: return

    # 2. Pick main image
    main_img_path = filedialog.askopenfilename(title="Selecciona la imagen principal", filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.gif")])
    if not main_img_path: return

    # 3. Pick gallery images
    gallery_img_paths = filedialog.askopenfilenames(title="Selecciona imágenes para la galería", filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.gif")])

    # 4. Create noticia folder structure
    slug = title.lower().replace(" ", "_")[:30]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    noticia_folder = os.path.join(NOTICIAS_DIR, f"{slug}_{timestamp}")
    images_folder = os.path.join(noticia_folder, "images")
    os.makedirs(images_folder, exist_ok=True)

    # 5. Copy main image and gallery images
    main_img_filename = copy_image(main_img_path, noticia_folder)
    gallery_img_filenames = []
    for img_path in gallery_img_paths:
        gallery_img_filenames.append(copy_image(img_path, images_folder))

    # 6. Create noticia.html in noticia_folder
    noticia_filename = "noticia.html"
    noticia_filepath = os.path.join(noticia_folder, noticia_filename)
    # For gallery, use relative paths: images/filename
    gallery_imgs_rel = [f"images/{img}" for img in gallery_img_filenames]
    main_img_rel = main_img_filename
    # If no gallery, show main image in gallery
    first_gallery_img = gallery_imgs_rel[0] if gallery_imgs_rel else main_img_rel

    with open(noticia_filepath, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="../../style.css">
    <link rel="stylesheet" href="../../noticia.css">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Special+Gothic+Expanded+One&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Special+Gothic&family=Special+Gothic+Expanded+One&display=swap" rel="stylesheet">
</head>

<body>
    <div class="topnav" style="align-items: center;">
        <a href="../../index.html" class="">Inicio</a>
        <a href="../../galeria.html" class="">Galería</a>
        <a href="../../noticiero.html" class="active">Noticias</a>
        <a href="../../salidas.html" class="">Salidas</a>
        <a href="../../contacto.html" class="">Contacto</a>
        <img src="../../logo.png" alt="logo" style="width: 90px; height: auto; margin-left: 20px;">
    </div>

    <div id="atras">
        <a href="../../noticiero.html" class="atras">← Volver</a>
    </div>

    <h3 style="text-align: left;">
        {title}
    </h3>

    <h4 style="text-align: left;"><em>
        {subtitle}
    </em></h4>

    <h5 style="text-align: left;">
        {text}
    </h5>

    <div id="Galeria">
        <button class="gallery-nav prev" onclick="patras()">❮</button>
        <div class="container" style="text-align: center;">
            <img src="{gallery_imgs_rel[0] if gallery_imgs_rel else main_img_rel}" alt="imagen" class="gallery-img" id="gallery-img">
            <div style="margin-top: 10px;">
                <a id="download-btn" href="{gallery_imgs_rel[0] if gallery_imgs_rel else main_img_rel}" download>
                    <button
                        style="padding: 10px 20px; font-size: 1.5rem; cursor: pointer; background-color: rgb(255, 255, 255); color: rgb(0, 0, 0); border: 2px solid rgb(0, 0, 0); border-radius: 5px; font-family: Special Gothic; box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.5);">💾Descargar</button>
                </a>
            </div>
        </div>
        <button class="gallery-nav next" onclick="plante()">❯</button>
    </div>
    <script>
        const images = [{', '.join([f'"{img}"' for img in (gallery_imgs_rel if gallery_imgs_rel else [main_img_rel])] )}];
        let index = 0;
        const imgEl = document.getElementById('gallery-img');

        function plante() {{
            index = (index + 1) % images.length;
            updateGallery();
        }}

        function patras() {{
            index = (index - 1 + images.length) % images.length;
            updateGallery();
        }}

        function updateGallery() {{
            imgEl.src = images[index];
            document.getElementById("download-btn").href = images[index];
        }}

        updateGallery(); // set initial
    </script>
    <style>
        #Galeria {{
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 10px;
            margin-top: 10px;
            max-height: 70vh;
        }}

        .container {{
            background-color: rgb(255, 255, 255);
            object-fit: cover;
            align-items: center;
        }}

        .gallery-img {{
            max-height: 70vh;
            width: 90%;
            border-radius: 10px;
            object-fit: contain;
            border: 2px solid black;
            box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.5);
        }}

        .gallery-nav {{
            flex: 1;
            background-color: transparent;
            border: none;
            font-size: 3rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 70vh;
        }}

        .gallery-nav:hover {{
            background-color: rgba(0, 0, 0, 0.1);
        }}
    </style>

    <div class="botnav">
        <div
            style="color: #ffffff;display: flex; align-items: center; justify-content: space-around; flex-wrap: wrap; margin: 20px;">
            <img src="../../logo_grande.png" alt="logo" style="width: 50%; height: auto;">
            <div style="text-align: center;">
                <h1 style="font-family: Special Gothic Expanded One, sans-serif; font-weight: 400;">Contacto:</h1>
                <h2 style="font-family: Special Gothic, sans-serif; font-weight: 400;">📩asoc.loscarucheros@outlook.com
            </div>
    </div>
</body>
</html>
""")

    # 7. Insert new card at top of noticiero.html
    with open(NOTICIERO_HTML, "r", encoding="utf-8") as f:
        html = f.read()
    insert_pos = html.find('<div class="news">')
    if insert_pos == -1:
        messagebox.showerror("Error", "No se encontró el contenedor de noticias en noticiero.html")
        return
    # Relative path from noticiero.html to noticia.html and main image
    noticia_rel_path = os.path.relpath(noticia_filepath, BASE_DIR).replace("\\", "/")
    main_img_card_rel = os.path.relpath(os.path.join(noticia_folder, main_img_filename), BASE_DIR).replace("\\", "/")
    card_html = f'''
        <a href="{noticia_rel_path}"><div class="card" >

            <img src="{main_img_card_rel}" alt="imagen">

            <h1>
                {title}
            </h1>

            <h2 ><em>
                    {subtitle}
                </em></h2>
        </div></a>

        <hr>
    '''
    # Insert after <div class="news">
    insert_pos = html.find('>', insert_pos) + 1
    new_html = html[:insert_pos] + card_html + html[insert_pos:]
    with open(NOTICIERO_HTML, "w", encoding="utf-8") as f:
        f.write(new_html)

    messagebox.showinfo("Éxito", f"Noticia creada en: {noticia_rel_path}")

root = tk.Tk()
root.title("Gestor de Noticias")
root.geometry("300x150")
btn = tk.Button(root, text="Crear Nueva Noticia", command=create_new, font=("Arial", 14), padx=20, pady=20)
btn.pack(expand=True)
root.mainloop()