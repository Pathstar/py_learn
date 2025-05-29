import os
import shutil
from datetime import datetime
import hashlib

def get_all_files(root):
    file_set = set()
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            rel_path = os.path.relpath(os.path.join(dirpath, filename), root)
            file_set.add(rel_path)
    return file_set

def file_hash(filepath, hashfunc='md5', block_size=65536):
    """计算文件内容hash（默认md5）"""
    h = hashlib.new(hashfunc)
    with open(filepath, 'rb') as f:
        while chunk := f.read(block_size):
            h.update(chunk)
    return h.hexdigest()

def main():
    a_root = r'D:\garbages\Python\learn'
    b_root = r'D:\garbages\history\learn'
    today = datetime.now().strftime('%m%d%Y')
    output_base = rf'D:\garbages\Python\history\{today}'
    target_learn_folder = os.path.join(output_base, 'learn')
    os.makedirs(target_learn_folder, exist_ok=True)
    a_files = get_all_files(a_root)
    b_files = get_all_files(b_root)
    # 新文件 = 只在a中有
    extra_files = a_files - b_files
    # 可能被改过的 = 两边都有
    common_files = a_files & b_files
    # 新增文件直接复制
    for rel_file in extra_files:
        src_path = os.path.join(a_root, rel_file)
        dst_path = os.path.join(target_learn_folder, rel_file)
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        shutil.copy2(src_path, dst_path)
        print(f'新增文件：{rel_file} 已复制到：{dst_path}')
    # 被改动的文件：内容不同
    modified_count = 0
    for rel_file in common_files:
        a_path = os.path.join(a_root, rel_file)
        b_path = os.path.join(b_root, rel_file)
        if file_hash(a_path) != file_hash(b_path):
            dst_path = os.path.join(target_learn_folder, rel_file)
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(a_path, dst_path)
            print(f'改动文件：{rel_file} 已复制到：{dst_path}')
            modified_count += 1
    print(f'共新增 {len(extra_files)} 个文件，共有 {modified_count} 个文件内容有更改。')
    # 2. 合并输出的 learn 到 history/learn 中
    final_target = r'D:\garbages\history\learn'
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