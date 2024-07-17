import os
import yaml

def read_yolo_labels(txt_file_path):
    try:
        with open(txt_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            labels = []
            for line in lines:
                parts = line.strip().split()
                label = {
                    'class': int(parts[0]),
                    'x_center': float(parts[1]),
                    'y_center': float(parts[2]),
                    'width': float(parts[3]),
                    'height': float(parts[4])
                }
                labels.append(label)
            return labels
    except Exception as e:
        print(f"Error reading {txt_file_path}: {e}")
        return []

def contains_class_to_keep(labels, class_to_keep):
    for label in labels:
        if label['class'] == class_to_keep:
            return True
    return False

def process_folder(folder_path, class_to_keep):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                txt_file_path = os.path.join(root, file)
                labels = read_yolo_labels(txt_file_path)
                if contains_class_to_keep(labels, class_to_keep):
                    print(f'Keeping file: {txt_file_path}')
                else:
                    print(f'Deleting file: {txt_file_path}')
                    os.remove(txt_file_path)

def get_class_number_from_yaml(yaml_file_path, target_class_name):
    with open(yaml_file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
        classes = data['names']
        if target_class_name in classes:
            return classes.index(target_class_name)
        else:
            print(f"Class '{target_class_name}' not found in {yaml_file_path}")
            return None

# 指定YAML文件路径和标签名称
yaml_file_path = 'K:/Greatech/标注/反光衣/safety-Helmet-Reflective-Jacket/data.yaml'  # 请根据实际路径修改
target_class_name = 'Reflective-Jacket'

# 获取目标类别的编号
class_to_keep = get_class_number_from_yaml(yaml_file_path, target_class_name)

if class_to_keep is not None:
    # 指定顶级文件夹路径
    folder_path = 'K:/Greatech/标注/反光衣/safety-Helmet-Reflective-Jacket/train/labels'
    process_folder(folder_path, class_to_keep)
