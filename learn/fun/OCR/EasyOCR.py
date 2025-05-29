import os
import easyocr
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
    # OCR识别（中英混合）
    reader = easyocr.Reader(['ch', 'en'])  # 支持中文和英文
    results = reader.readtext(latest_file, detail=0)
    print("识别结果：")
    for line in results:
        print(line)