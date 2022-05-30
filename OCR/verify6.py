import tesserocr
from PIL import Image
import numpy as np

"""
思路：把图片转化为灰度图像，然后根据阈值删除图片中的干扰点
"""
image = Image.open('captcha2.png')
#把图片(RGBA)转化成256个级别的灰度图像(L)，颜色越深灰度越高
image = image.convert('L')
#设置灰度的阈值
threshold = 50
#将图片转化为NumPy数组
array = np.array(image)
"""
使用NumPy的where方法对数组进行筛选和处理
指定将灰度大于阈值的图片的像素设置为255，表示白色
否则设置为0，表示黑色
"""
array = np.where(array > threshold, 255, 0)
image = Image.fromarray(array.astype('uint8'))
print(tesserocr.image_to_text(image))
