import tesserocr
from PIL import Image

image = Image.open('captcha2.png')
result = tesserocr.image_to_text(image)
print(result)
