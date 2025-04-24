import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from datetime import datetime
import os
import shutil
import locale

def add_salida():
    # Set locale to Spanish for date formatting
    locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")

    # Step 3: Ask for the destination and date
    destination = simpledialog.askstring("Destino", "¿A dónde fue la salida?")
    date = simpledialog.askstring("Fecha", "¿Cuándo fue la salida? (Formato: DD/MM/AAAA)")
    if not destination or not date:
        messagebox.showerror("Error", "El destino y la fecha son obligatorios.")
        return

    # Format the date to Spanish
    try:
        date_obj = datetime.strptime(date, "%d/%m/%Y")
        formatted_date = date_obj.strftime("%d de %B de %Y")  # Updated to Spanish format
    except ValueError:
        messagebox.showerror("Error", "La fecha debe estar en el formato DD/MM/AAAA.")
        return

    # Step 4: Ask for a brief description
    description = simpledialog.askstring("Descripción", "Escribe una breve descripción de la salida:")
    if not description:
        messagebox.showerror("Error", "La descripción es obligatoria.")
        return

    # Step 5: Drag-and-drop window for gallery images
    gallery_images = filedialog.askopenfilenames(
        title="Selecciona las imágenes para la galería",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.webp")]
    )
    if not gallery_images:
        messagebox.showerror("Error", "Debes seleccionar al menos una imagen para la galería.")
        return

    # Generate folder and file paths
    salida_folder = "salida"
    os.makedirs(salida_folder, exist_ok=True)
    safe_destination = destination.replace(" ", "_").replace("/", "_")
    folder_name = f"{safe_destination}"
    folder_path = os.path.join(salida_folder, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # Copy gallery images to the new folder
    gallery_folder = os.path.join(folder_path, "gallery")
    os.makedirs(gallery_folder, exist_ok=True)
    for img in gallery_images:
        shutil.copy(img, gallery_folder)

    # Add the salida to salidas.html
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
                style="padding: 10px 20px; font-size: 1rem; cursor: pointer; background-color: rgb(255, 255, 255); color: rgb(0, 0, 0); border: 2px solid rgb(0, 0, 0); border-radius: 5px; font-family: Special Gothic; box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.5);">💾Descargar</button>
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
    Status_bar = """
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

    salida_html = f"""
    <li>
        <span class="date">{formatted_date}</span>
        <a href="salida/{folder_name}/index.html">{destination}</a>
        <p>{description}</p>
    </li>
    
    """

    with open("salidas.html", "r", encoding="utf-8") as f:
        content = f.read()

    insert_point = content.find('<a id="una mierda"></a>')
    if insert_point == -1:
        messagebox.showerror("Error", "No se pudo encontrar el marcador para insertar la salida.")
        return
    insert_point += len('<a id="una mierda"></a>')

    new_content = content[:insert_point] + salida_html + content[insert_point:]
    with open("salidas.html", "w", encoding="utf-8") as f:
        f.write(new_content)

    # Create the salida HTML file
    html_path = os.path.join(folder_path, "index.html")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{destination}</title>
  <link rel="stylesheet" href="../../newstyle copy.css">
</head>
<body>
    {Status_bar}
  <div style="padding: 2rem;">
    <h1 class="Titulo">{destination}</h1>
    <time>{formatted_date}</time>
    <p>{description}</p>
    {gallery_html}
    {footer_html}
  </div>
</body>
</html>
""")
    messagebox.showinfo("Éxito", f"Salida añadida en '{folder_path}'.")

# UI
root = tk.Tk()
root.title("Añadir Nueva Salida")
root.geometry("300x150")
tk.Button(root, text="Añadir nueva salida", command=add_salida, height=2, width=30).pack(pady=30)
root.mainloop()
