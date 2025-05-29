import os
import shutil
from datetime import datetime
def get_all_files(root):
    file_set = set()
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            rel_path = os.path.relpath(os.path.join(dirpath, filename), root)
            file_set.add(rel_path)
    return file_set
def main():
    a_root = r'D:\garbages\Python\learn'
    b_root = r'D:\garbages\history\learn'
    today = datetime.now().strftime('%Y%m%d')
    # 注意 history 的拼写
    output_base = rf'D:\garbages\Python\history\{today}'
    target_learn_folder = os.path.join(output_base, 'learn')
    # 1. 创建输出目录
    os.makedirs(target_learn_folder, exist_ok=True)
    a_files = get_all_files(a_root)
    b_files = get_all_files(b_root)
    extra_files = a_files - b_files
    for rel_file in extra_files:
        src_path = os.path.join(a_root, rel_file)
        dst_path = os.path.join(target_learn_folder, rel_file)
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        shutil.copy2(src_path, dst_path)
        print(f'已复制: {dst_path}')
    print(f'共复制 {len(extra_files)} 个文件到 {target_learn_folder}')
    # 2. 将输出的learn文件夹整体拷贝到 D:\garbages\history\learn
    final_target = r'D:\garbages\history\learn'
    # 先将输出learn内容合并到final_target中（如果目标有同名文件会被覆盖）
    for dirpath, _, filenames in os.walk(target_learn_folder):
        rel_dir = os.path.relpath(dirpath, target_learn_folder)
        for filename in filenames:
            src_file = os.path.join(dirpath, filename)
            if rel_dir == ".":
                dst_file = os.path.join(final_target, filename)
            else:
                dst_file = os.path.join(final_target, rel_dir, filename)
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            shutil.copy2(src_file, dst_file)
            print(f'已同步到: {dst_file}')
    print(f'已将 {target_learn_folder} 中全部文件同步到 {final_target}')
if __name__ == '__main__':
    main()