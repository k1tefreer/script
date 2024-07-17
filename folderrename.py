import os

def rename_images(root_dir, new_name_prefix):
    count = 1
    for foldername in os.listdir(root_dir):
        folderpath = os.path.join(root_dir, foldername)
        if os.path.isdir(folderpath):
            for filename in os.listdir(folderpath):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    old_filepath = os.path.join(folderpath, filename)
                    extension = os.path.splitext(filename)[1]
                    new_filename = f"{new_name_prefix}_{count:03}{extension}"
                    new_filepath = os.path.join(folderpath, new_filename)
                    os.rename(old_filepath, new_filepath)
                    count += 1

# Example usage:
root_directory = 'K:\Greatech\seed\新建文件夹'  # 修改成你的大文件夹的路径
new_prefix = 'new_image'  # 修改成你想要的新文件名前缀

rename_images(root_directory, new_prefix)
