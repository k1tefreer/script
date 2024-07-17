
import os

jpg_folder = "K:/Greatech/标注/反光衣/safety-Helmet-Reflective-Jacket/train/images"
xml_folder = "K:/Greatech/标注/反光衣/safety-Helmet-Reflective-Jacket/train/labels"

jpg_files = os.listdir(jpg_folder)
xml_files = os.listdir(xml_folder)

for jpg_file in jpg_files:
    xml_file = os.path.join(xml_folder, os.path.splitext(jpg_file)[0] + ".txt")
    if not os.path.exists(xml_file):
        jpg_file_path = os.path.join(jpg_folder, jpg_file)
        os.remove(jpg_file_path)
        print(f"Deleted {jpg_file_path}")
