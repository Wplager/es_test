import os

def print_file_structure(path, prefix='', is_last=False, hide_hidden=True, output_file=None):
    """
    递归打印文件结构并输出到文本文件
    :param path: 当前路径
    :param prefix: 缩进前缀
    :param is_last: 是否为最后一个子项
    :param hide_hidden: 是否过滤隐藏文件（以.开头）
    :param output_file: 输出文件对象（用于写入文本）
    """
    items = os.listdir(path)
    
    # 过滤隐藏文件和 node_modules 文件夹
    if hide_hidden:
        items = [item for item in items if not item.startswith('.') and item != "dist" and item != 'node_modules' and item != 'back' and item != 'db']
    else:
        items = [item for item in items if item != 'node_modules']
    
    dirs = [item for item in items if os.path.isdir(os.path.join(path, item))]
    files = [item for item in items if os.path.isfile(os.path.join(path, item))]
    items = dirs + files  # 文件夹优先显示
    
    for i, item in enumerate(items):
        current_path = os.path.join(path, item)
        is_dir = os.path.isdir(current_path)
        connector = '└── ' if i == len(items) - 1 else '├── '
        line = f'{prefix}{connector}{item}'
        
        # 输出到控制台和文件
        print(line)
        if output_file:
            output_file.write(line + '\n')
        
        if is_dir and item not in ['.', '..']:  # 跳过当前目录和父目录
            new_prefix = prefix + ('    ' if i == len(items) - 1 else '│   ')
            print_file_structure(current_path, new_prefix, i == len(items) - 1, hide_hidden, output_file)

def main():
    current_dir = os.getcwd()
    output_filename = 'file_structure.txt'  # 输出文件名
    
    # 打开文件并写入内容
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(f'当前目录结构（过滤隐藏文件）：{current_dir}\n')
        print_file_structure(current_dir, hide_hidden=True, output_file=f)
    
    print(f'\n文件结构已输出到：{os.path.abspath(output_filename)}')

if __name__ == '__main__':
    main()