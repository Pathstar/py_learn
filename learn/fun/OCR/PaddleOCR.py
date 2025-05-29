import os
from paddleocr import PaddleOCR
# 文件夹路径
folder_path = r'D:\OCR'
# 获取所有png文件
png_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
             if f.lower().endswith('.png')]
if not png_files:
    print("文件夹内没有PNG文件")
else:
    # 获取最新的png文件
    latest_file = max(png_files, key=os.path.getctime)
    print("最新的PNG文件：", latest_file)
    # OCR识别（中文支持中英文混合）
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # lang="ch" 支持中英文
    results = ocr.ocr(latest_file, cls=True)
    print("识别结果：")
    for line in results:
        print(line[1][0])