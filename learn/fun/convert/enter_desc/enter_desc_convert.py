import pandas as pd
from collections import defaultdict
# 读取文件
# 写python代码，有一个 名称.txt 和 描述.txt ，这两个文件的每一行一一对应，在下面的筛选过程中绑定对应关系，
# 要求： 对描述进行排序，对于相同的描述，再对其对应的名称按照名称排序，生成Excel 将第一种描述放到第二列，对应名称放到第一列，第三列留白，以此顺序按不同的描述放到不同列上
# 相同描述少描述列的放在前列，描述多描述列的在后列，以此排序

with open('名称.txt', encoding='utf-8') as f_name:
    names = [l.strip() for l in f_name]
with open('描述.txt', encoding='utf-8') as f_descr:
    descrs = [l.strip() for l in f_descr]
assert len(names) == len(descrs), "名称和描述数量不一致"
# 1. 绑定并按描述和名称排序（保证名称和描述顺序一致）
data = list(zip(names, descrs))
data.sort(key=lambda x: (x[1], x[0]))  # 先按描述、再按名称排序
# 2. 分组: 按描述分组，每组名称按名称排序
grouped = defaultdict(list)
for name, descr in data:
    grouped[descr].append(name)
# 3. 对所有描述（=每组选项），按“该描述出现的名称数量”升序排列
descrs_sorted = sorted(
    grouped.keys(),
    key=lambda d: (len(grouped[d]), d)  # 名称数少的在前，若一样再按描述字典序
)
columns = []
for i, descr in enumerate(descrs_sorted, 1):
    columns += [f'名称{i}', f'描述{i}', '']  # 每组三列
max_group_len = max(len(grouped[descr]) for descr in descrs_sorted)
rows = []
for row_idx in range(max_group_len):
    row = []
    for descr in descrs_sorted:
        names_list = grouped[descr]
        if row_idx < len(names_list):
            if row_idx % 50 == 0:
                row.extend(['', '', ''])
                row.extend(['', '', ''])
                row.extend(['', '', ''])
                row.extend(['', '', ''])
                row.extend(['', '', ''])
            row.extend([names_list[row_idx], descr, ' '])
        else:
            row.extend(['', '', ''])
    rows.append(row)
df = pd.DataFrame(rows, columns=columns)
df.to_excel('筛选结果4.xlsx', index=False)