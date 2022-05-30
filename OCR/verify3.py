import tesserocr
from PIL import Image

#针对有干扰的图片做去噪处理
image = Image.open('code2.jpg')

#把图片转化成256个级别的灰度图像，颜色越深灰度越高
image = image.convert('L')
#设置阈值，如果灰度小于阈值变为白色（黑色），否则变为黑色（白色）
threshold = 127
#将图片转化成一维的灰度值数组
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

#参照这个表进行二值化
image = image.point(table, '1')
image.show()

#这个代码并不能去除那些验证码和干扰线灰度值交错不一的干扰线
result = tesserocr.image_to_text(image)
print(result)
