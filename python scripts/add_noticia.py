import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from datetime import datetime
import os
import shutil

def create_news():
    # Step 3: Ask for the title
    title = simpledialog.askstring("Título", "Ingresa el título de la noticia:")
    if not title:
        messagebox.showerror("Error", "El título es obligatorio.")
        return

    # Step 4: Ask for the subtitle
    subtitle = simpledialog.askstring("Subtítulo", "Ingresa el subtítulo:")
    if not subtitle:
        messagebox.showerror("Error", "El subtítulo es obligatorio.")
        return
    
    text = simpledialog.askstring("Texto", "Ingresa el Texto:")

    # Step 5: Ask for the main image file
    main_image = filedialog.askopenfilename(
        title="Selecciona la imagen principal",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.webp")]
    )
    if not main_image:
        messagebox.showerror("Error", "Debes seleccionar una imagen principal.")
        return

    # Step 6: Drag-and-drop window for gallery images
    gallery_images = filedialog.askopenfilenames(
        title="Selecciona las imágenes para la galería",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.webp")]
    )
    if not gallery_images:
        messagebox.showerror("Error", "Debes seleccionar al menos una imagen para la galería.")
        return

    # Generate folder and file paths
    date_obj = datetime.now()
    date_machine = date_obj.strftime("%Y-%m-%d")
    date_display = date_obj.strftime("%d-%B-%Y").replace('-', ' ')
    safe_title = title.replace(" ", "_").replace("/", "_")
    folder_name = f"{safe_title}_{date_display.replace(' ', '-')}"
    folder_path = os.path.join("noticia", folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # Copy the main image to the new folder
    main_image_filename = os.path.basename(main_image)
    main_image_dest = os.path.join(folder_path, main_image_filename)
    shutil.copy(main_image, main_image_dest)

    # Copy gallery images to the new folder
    gallery_folder = os.path.join(folder_path, "gallery")
    os.makedirs(gallery_folder, exist_ok=True)
    for img in gallery_images:
        shutil.copy(img, gallery_folder)

    # Step 7: Add a link to the noticia in noticiero.html
    preview_card = f"""
    <a href="noticia/{folder_name}/index.html" class="preview-card">
        <div class="card">
            <div class="card-text">
                <h2>{title}</h2>
                <p>{subtitle}</p>
            </div>
            <div class="card-image">
                <img src="noticia/{folder_name}/{main_image_filename}" alt="Imagen">
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

    # Step 8: Create the noticia HTML file
    html_path = os.path.join(folder_path, "index.html")
    gallery_images_js = ", ".join(f'"gallery/{os.path.basename(img)}"' for img in gallery_images)
    gallery_html = f"""
    <div id="Galeria">
        <div class="container" style="text-align: center;"></div>
        <button class="gallery-nav prev" onclick="patras()">❮</button>
        <img src="gallery/{os.path.basename(gallery_images[0])}" alt="imagen" class="gallery-img" id="gallery-img">
        <button class="gallery-nav next" onclick="plante()">❯</button>
    </div>
    <div style="text-align: center; margin-top: 10px;">
        <a id="download-btn" href="gallery/{os.path.basename(gallery_images[0])}" download>
            <button
                style="padding: 10px 20px; font-size: 1rem; cursor: pointer; background-color: rgb(255, 255, 255); color: rgb(0, 0, 0); border: 2px solid rgb(0, 0, 0); border-radius: 5px; font-family: inherit; box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.5);">💾Descargar</button>
        </a>
    </div>
    <script>
        const images = [{gallery_images_js}];
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
            max-height: 70vh;
        }}

        .container {{
            background-color: aqua;
            object-fit: cover;
            align-items: center;
        }}

        .gallery-img {{
            max-height: 70vh;
            width: 80%;
            border-radius: 10px;
            object-fit: contain;
            border: 2px solid black;
            box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.5);
        }}

        .gallery-nav {{
            flex: 1;
            background-color: transparent;
            border: none;
            font-size: 2rem;
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
    """
    footer_html = """
    <div style="background-color: black; color: white;">
        <div style="display: flex; align-items: center; justify-content: space-around; flex-wrap: wrap; margin: 20px;">
            <img src="../../logo_grande.png" alt="logo" style="width: 50%; height: auto;">
            <div style="text-align: center;">
                <h1 style="font-family: Special Gothic Expanded One, sans-serif; font-weight: 400;">Contacto:</h1>
                <h2 style="font-family: Special Gothic, sans-serif; font-weight: 400;">📞+34 681350394 (15:00 - 21:00)</h2>
                <h2 style="font-family: Special Gothic, sans-serif; font-weight: 400;">📩asoc.loscarucheros@outlook.com</h2>
            </div>
        </div>
    </div>
    """
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="stylesheet" href="../../newstyle copy.css">
</head>
<body>
  <div id="Barra_De_Status" class="status">
    <img src="../../logo.png" alt="logo">
    <ul>
      <li><a href="../../index copia.html" class="status">Inicio</a></li>
      <li><a href="../../galeria.html" class="status">Galería</a></li>
      <li><a href="../../acerca.html" class="status">Acerca</a></li>
      <li><a href="../../noticiero.html" class="status">Noticias</a></li>
      <li><a href="../../salidas.html" class="status">Salidas</a></li>
      <li><a href="../../contacto.html" class="status">Contacto</a></li>
    </ul>
  </div>

  <div style="padding: 2rem;">
    <h1 class="Titulo" style="font-family: 'Special Gothic Expanded One', sans-serif;">{title}</h1>
    <time datetime="{date_machine}">{date_display}</time>
    <h3 class="Subtitulo">{subtitle}</h3>
    <p>{text}</p>
    {gallery_html}
    {footer_html}
  </div>
</body>
</html>
""")
    messagebox.showinfo("Éxito", f"Noticia creada en '{folder_path}'.")

# UI
root = tk.Tk()
root.title("Crear Noticia")
root.geometry("300x150")
tk.Button(root, text="Crear nueva noticia", command=create_news, height=2, width=30).pack(pady=30)
root.mainloop()
