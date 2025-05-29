with open('换行转分号.txt', 'r', encoding='utf-8') as f:
    items = [line.strip() for line in f if line.strip()]  # 移除空白和换行
# 写入目标文件，每50项一行
with open('换行转分号_结果.txt', 'w', encoding='utf-8') as fout:
    for idx in range(0, len(items), 50):
        sub_items = items[idx:idx + 50]
        line = ';'.join(sub_items)
        fout.write(line + '\n')
print('处理完成，结果保存在 换行转分号_结果.txt')