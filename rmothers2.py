import os

jpg_folder = "K:\\Greatech\\标注\\xielou\\ip5(1)"
xml_folder = "K:\\Greatech\\标注\\xielou\\输出"

jpg_files = os.listdir(jpg_folder)
xml_files = os.listdir(xml_folder)

for xml_file in xml_files:
    jpg_file = os.path.join(jpg_folder, os.path.splitext(xml_file)[0] + ".jpg")
    if not os.path.exists(jpg_file):
        xml_file_path = os.path.join(xml_folder, xml_file)
        os.remove(xml_file_path)
        print(f"Deleted {xml_file_path}")

for jpg_file in jpg_files:
    xml_file = os.path.join(xml_folder, os.path.splitext(jpg_file)[0] + ".xml")
    if not os.path.exists(xml_file):
        jpg_file_path = os.path.join(jpg_folder, jpg_file)
        os.remove(jpg_file_path)
        print(f"Deleted {jpg_file_path}")