# Pedir los datos al usuario
titulo = input("Título de la noticia: ")
fecha = input("Fecha: ")
imagen = input("Fuente de la imagen (URL): ")
texto = input("Texto de la noticia: ")

# Plantilla HTML
html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Noticias</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>{titulo}</h1>
    <h2>{fecha}</h2>
    <img id="Noticias-img" src="{imagen}" alt="imagen">
    <div class="container">
        <p>{texto}</p>
    </div>
</body>
</html>"""

# Guardar el resultado en un archivo
with open("noticia.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Archivo 'noticia.html' generado.")
