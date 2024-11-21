import argparse

def remove_column(file_path, output_path=None):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    header = lines[0].strip().split('\t')
    try:
        total_index = header.index('Total')
    except ValueError:
        print("没有找到名为'Total'的列")
        return

    modified_lines = []
    for line in lines:
        parts = line.strip().split('\t')
        if len(parts) > total_index:
            del parts[total_index]
        modified_lines.append('\t'.join(parts) + '\n')

    output_file = output_path if output_path else file_path
    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(modified_lines)
    return output_file

def process_file(input_file, output_file=None):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    modified_lines = []
    for i, line in enumerate(lines):
        if i == 0:
            modified_lines.append(line)
            continue

        parts = line.strip().split('\t')
        first_column = parts[0]

        for j in range(1, len(parts)):
            if parts[j] != '0':
                parts[j] = first_column

        modified_lines.append('\t'.join(parts) + '\n')

    output_file = output_file if output_file else input_file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(modified_lines)
    return output_file

def remove_first_column(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    modified_lines = []
    for line in lines:
        columns = line.strip().split('\t')
        if len(columns) > 1:
            new_line = '\t'.join(columns[1:]) + '\n'
            modified_lines.append(new_line)
        else:
            modified_lines.append(line)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(modified_lines)
    return output_file

def replace_zeros_with_empty(line):
    parts = line.strip().split('\t')
    parts = ['' if part == '0' else part for part in parts]
    return '\t'.join(parts) + '\n'

def process_file1(input_filename, output_filename=None):
    if not output_filename:
        output_filename = input_filename

    with open(input_filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(output_filename, 'w', encoding='utf-8') as file:
        for line in lines:
            file.write(replace_zeros_with_empty(line))
    return output_filename

def main():
    parser = argparse.ArgumentParser(description="处理基因计数文件以生成Venn图输入文件")
    parser.add_argument("input_file", help="输入文件路径")
    parser.add_argument("output_file", help="输出文件路径")
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file

    # 第一步：删除 "Total" 列
    input_file = remove_column(input_file, output_file)

    # 第二步：处理文件，将非零值替换为第一列的值
    input_file = process_file(input_file, output_file)

    # 第三步：删除第一列
    input_file = remove_first_column(input_file, output_file)

    # 第四步：将所有 '0' 替换为空字符串
    input_file = process_file1(input_file, output_file)

#python GeneCount_to_VennFile_windows.py Orthogroups.GeneCount.tsv VennDraw.txt

if __name__ == "__main__":
    main()
