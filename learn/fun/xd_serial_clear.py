import os
import datetime
from lxml import html

count = 0
def extract_table(html_content):
    global count
    tree = html.fromstring(html_content)
    tables = tree.xpath('//div[contains(@class, "devui-table-view") '
                        'and contains(@class, "contain-fix-height") '
                        'and contains(@class, "devui-table-scroll-left")]')
    # class="devui-table-view contain-fix-height devui-table-scroll-left"
    if not tables:
        raise ValueError("没找到表格")
    rows = tables[0].xpath('.//tr[td]')
    # results = []
    result = ""

    for row in rows:
        cell = row.xpath('.//td[3]//text()')
        clean_text = ' '.join(''.join(cell).strip().split())
        if clean_text:
            count = count + 1
            if count % 50 == 0:
                # results.append(clean_text + "\n")
                result += clean_text + ";\n\n"
            else:
                # results.append(clean_text)
                result += clean_text + ";"
    # return ';'.join(results) if results else '没有提取到数据'
    return result

def main():
    try:
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        file_path = os.path.join(desktop_path, 'clear.txt')
        with open(file_path, 'r', encoding='utf-8') as f:
            html_input = f.read()
        if not html_input.strip():
            raise ValueError("文件内容为空")
        result = extract_table(html_input)
        output = "\n—————————— 提取结果 ——————————\n\n" + result
        print(output)
        # 文件保存逻辑
        now = datetime.datetime.now()
        # count = len(result.split(';')) if result != '没有提取到数据' else 0
        filename = f"{now.month:02}.{now.day:02} {now.hour:02}-{now.minute:02} {count}条.txt"
        save_dir = os.path.join(desktop_path, '用例记录')

        os.makedirs(save_dir, exist_ok=True)

        save_path = os.path.join(save_dir, filename)
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(result)

        print(f"\n\n文件已保存至：{save_path}")
    except Exception as e:
        print(f"\n错误：{str(e)}")


if __name__ == "__main__":
    main()