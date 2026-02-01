from PIL import Image

# Open an image
img = Image.open('src/efevmo_me/Carnap.jpg')

# Define the new size (width, height)
new_size = (1280, 720) 

# Resize the image
resized_img = img.resize(new_size, Image.Resampling.LANCZOS) # Use LANCZOS for high quality downsampling

# Save the resized image
resized_img.save('src/efevmo_me/Carnap_thumb.jpg')

# Optional: display the image
# resized_img.show() 
