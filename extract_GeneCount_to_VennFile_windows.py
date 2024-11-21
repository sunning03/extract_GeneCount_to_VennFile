def remove_column(file_path, output_path=None):
    # 1. 读取TXT文件的内容
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 2. 确定哪一列是"Total"列
    header = lines[0].strip().split('\t')  # 假设列之间用制表符分隔
    try:
        total_index = header.index('Total')
    except ValueError:
        print("没有找到名为'Total'的列")
        return

    # 3. 删除这一列
    modified_lines = []
    for line in lines:
        parts = line.strip().split('\t')
        if len(parts) > total_index:  # 防止某些行缺少'Total'列
            del parts[total_index]
        modified_lines.append('\t'.join(parts) + '\n')

    # 4. 将处理后的数据写回新的TXT文件或覆盖原文件
    output_file = output_path if output_path else file_path
    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(modified_lines)
    return output_file  # 返回输出文件路径

def process_file(input_file, output_file=None):
    # 1. 读取TXT文件的内容
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 处理每一行
    modified_lines = []
    for i, line in enumerate(lines):
        if i == 0:  # 跳过第一行（标题行）
            modified_lines.append(line)
            continue

        parts = line.strip().split('\t')
        first_column = parts[0]  # 获取第一列数据

        # 从第二列开始检查
        for j in range(1, len(parts)):
            if parts[j] != '0':
                parts[j] = first_column

        # 删除第一列
        # del parts[0]

        # # 将所有 '0' 替换为空字符串
        # parts = [part if part != '0' else '\t' for part in parts]

        modified_lines.append('\t'.join(parts) + '\n')

    # 4. 将处理后的数据写回新的TXT文件或覆盖原文件
    output_file = output_file if output_file else input_file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(modified_lines)
    return output_file  # 返回输出文件路径

def remove_first_column(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 处理每一行，移除第一列
    modified_lines = []
    for line in lines:
        # 使用制表符分割每一行
        columns = line.strip().split('\t')
        if len(columns) > 1:
            # 跳过第一列，连接剩余部分
            new_line = '\t'.join(columns[1:]) + '\n'
            modified_lines.append(new_line)
        else:
            modified_lines.append(line)  # 如果只有一列，保留原样

    # 写入新文件
    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(modified_lines)
    return output_file  # 返回输出文件路径

def replace_zeros_with_empty(line):
    """将一行中的所有 '0' 替换为空字符串"""
    parts = line.strip().split('\t')
    # 替换 '0' 为 ''
    parts = ['' if part == '0' else part for part in parts]
    return '\t'.join(parts) + '\n'

def process_file1(input_filename, output_filename=None):
    """
    处理文件，将所有 '0' 替换为空字符串。
    
    如果 output_filename 未指定，则覆盖原文件。
    """
    if not output_filename:
        output_filename = input_filename

    with open(input_filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(output_filename, 'w', encoding='utf-8') as file:
        for line in lines:
            file.write(replace_zeros_with_empty(line))
    return output_filename  # 返回输出文件路径

# 使用函数
input_file = 'Orthogroups.GeneCount.tsv'
output_file = 'VennDraw.txt'  # 可选，如果不想覆盖原文件

# 第一步：删除 "Total" 列
input_file = remove_column(input_file, output_file)

# 第二步：处理文件，将非零值替换为第一列的值
input_file = process_file(input_file, output_file)

# 第三步：删除第一列
input_file = remove_first_column(input_file, output_file)

# 第四步：将所有 '0' 替换为空字符串
input_file = process_file1(input_file, output_file)