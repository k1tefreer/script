import os
import xml.etree.ElementTree as ET

# XML文件夹路径
xml_folder = "K:\\Greatech\\标注\\标注02\\帮未穿工服和安全帽\\kkk3\\op1"

# obj
object_name = 'person'

# 初始化计数器
total_count = 0

# 遍历XML文件夹中的每个文件
for filename in os.listdir(xml_folder):
    if filename.endswith('.xml'):
        # 解析XML文件
        tree = ET.parse(os.path.join(xml_folder, filename))
        root = tree.getroot()

        # 在当前文件中初始化计数器
        count = 0

        # 查找当前文件中所有名为'person'的对象并计数
        for obj in root.findall('.//object[name="{}"]'.format(object_name)):
            count += 1

        # 打印当前文件的计数结果
        print("文件 '{}' 中找到了 {} 个名为'{}'的对象。".format(filename, count,object_name))

        # 更新总计数器
        total_count += count

# 打印整个文件夹中的总计数结果
print("整个文件夹中总共找到了 {} 个名为'{}'的对象。".format(total_count,object_name))