import xml.etree.ElementTree as ET
import os


def find_elements_with_name(file_path, target_name):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # 找到所有 <object> 元素，其 <name> 子元素的文本值为 target_name
        elements = []
        for obj in root.findall("object"):
            name = obj.find("name")
            if name is not None and name.text == target_name:
                elements.append(obj)

        return elements
    except Exception as e:
        print(f"Error parsing file {file_path}: {e}")
        return []


def write_elements_to_file(elements, output_file_path):
    new_root = ET.Element("annotation")  # 创建新的根元素
    for elem in elements:
        new_root.append(elem)

    new_tree = ET.ElementTree(new_root)
    new_tree.write(output_file_path, encoding="utf-8", xml_declaration=True)


input_folder = 'K:\\Greatech\\开源dataset\\VOC2021\\Annotations'  # 替换为你的输入文件夹路径
output_folder = 'K:\\Greatech\\开源dataset\\VOC2021\\output_folder'  # 替换为你的输出文件夹路径
target_name = 'reflective_clothes'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for file_name in os.listdir(input_folder):
    if file_name.endswith('.xml'):
        file_path = os.path.join(input_folder, file_name)
        print(f"Processing file: {file_path}")  # 调试信息
        elements = find_elements_with_name(file_path, target_name)

        if elements:
            output_file_path = os.path.join(output_folder, file_name)
            write_elements_to_file(elements, output_file_path)
            print(f"Filtered elements from {file_name} written to {output_file_path}")
        else:
            print(f"No matching elements found in {file_name}")

print("Processing complete.")
