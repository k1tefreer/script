import os
import shutil

def copy_images_to_single_folder(root_dir, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for foldername in os.listdir(root_dir):
        folderpath = os.path.join(root_dir, foldername)
        if os.path.isdir(folderpath):
            for filename in os.listdir(folderpath):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    source_file = os.path.join(folderpath, filename)
                    target_file = os.path.join(target_dir, filename)
                    if not os.path.exists(target_file):
                        shutil.copy2(source_file, target_file)

# Example usage:
root_directory = 'K:\Greatech\seed\新建文件夹'  # 修改成你的大文件夹的路径
target_directory = 'K:\\Greatech\\seed\\新建文件夹\\all'  # 修改成你想要放置所有图片的目标文件夹路径

copy_images_to_single_folder(root_directory, target_directory)
