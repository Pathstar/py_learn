import os
from PIL import Image
import pytesseract
# 文件夹路径
folder_path = r'D:\OCR'
# 获取文件夹下所有png文件的路径
png_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
             if f.lower().endswith('.png')]
# 按文件创建时间排序，获取最新的png文件
if not png_files:
    print("文件夹内没有PNG文件")
else:
    latest_file = max(png_files, key=os.path.getctime)
    print("最新的PNG文件：", latest_file)
    # OCR识别（中英混合）
    text = pytesseract.image_to_string(Image.open(latest_file), lang='chi_sim+eng')
    print("识别结果：")
    print(text)