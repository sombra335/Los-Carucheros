import os

def rename_images(folder_path):
    images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'))]
    images.sort()
    
    for idx, filename in enumerate(images, start=1):
        ext = os.path.splitext(filename)[1]
        new_name = f"img{idx}{ext}"
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_name}")

# Llamada a la función con la ruta correcta
rename_images(r'C:\Users\parte\Documents\carucheros\images')
