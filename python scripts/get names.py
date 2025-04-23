import os

# Specify the directory containing the images
folder_path = 'images'  # Change this to the folder containing your images

# Get a list of all files in the folder
files = os.listdir(folder_path)

# Filter out the image files (you can adjust this for other image extensions as well)
image_files = [file for file in files if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]

# Start the JavaScript array
js_array = 'const images = [\n'

# Add each image file to the array
for image in image_files:
    js_array += f'    "images/{image}",\n'

# End the array
js_array += '];'

# Print the result to copy
print(js_array)
