import os

import cv2
import pytesseract
import pandas as pd

# 加载图像
image = cv2.imread('D:\ZHUOMIAN\GPT\code\image.jpg')

# 对图像进行预处理
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# 提取文本
text = pytesseract.image_to_string(gray, lang='eng')

# 将文本转换为数据表格
data = pd.read_csv(pd.compat.StringIO(text), sep='\t')

# 保存为Excel文件
data.to_excel('output.xlsx', index=False)
print(os.getcwd())
