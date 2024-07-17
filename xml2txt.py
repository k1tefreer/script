import xml.etree.ElementTree as ET
import glob

names = ['yes','no']


def convert_box(size, box):
    dw, dh = 1. / size[0], 1. / size[1]
    x, y, w, h = (box[0] + box[1]) / 2.0 - 1, (box[2] + box[3]) / 2.0 - 1, box[1] - box[0], box[3] - box[2]
    return x * dw, y * dh, w * dw, h * dh


def xml2txt(xml_path, txt_path):
    in_file = open(xml_path,encoding='utf-8') #报错GBK的时候在这里加 ,encoding='utf-8'
    out_file = open(txt_path, 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    # names list
    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls in names and int(obj.find('difficult').text) != 1:
            xmlbox = obj.find('bndbox')
            bb = convert_box((w, h), [float(xmlbox.find(x).text) for x in ('xmin', 'xmax', 'ymin', 'ymax')])
            cls_id = names.index(cls)  # class id
            out_file.write(" ".join([str(a) for a in (cls_id, *bb)]) + '\n')


xml_paths = glob.glob('K:\\Greatech\\标注\\安全带\\part2\\op2\\'+ '*.xml')
for xml_path in xml_paths:
    txt_path = xml_path.replace('.xml', '.txt')
    xml2txt(xml_path, txt_path)
