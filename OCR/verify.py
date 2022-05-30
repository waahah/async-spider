import tesserocr
from PIL import Image

#新建一个图片对象，将图片转换为文本
image = Image.open('code2.jpg')
result = tesserocr.image_to_text(image)
print(result)
