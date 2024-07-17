import cv2
import os
import shutil


def draw_boxes_on_image(image_path, label_path, output_path):
    # 读取图像
    image = cv2.imread(image_path)
    print(image_path)
    if image is None:
        print(f"Failed to load image from {image_path}")
        return

    # 读取并解析标注数据
    boxes = []
    with open(label_path, 'r') as file:
        for line in file:
            # 分割每一行的数据，转换为浮点数
            data = [float(num) for num in line.strip().split()]
            boxes.append(data)

    # 处理每一个标注框
    for box in boxes:
        class_id, x_center, y_center, width, height = box
        x_center *= image.shape[1]
        y_center *= image.shape[0]
        width *= image.shape[1]
        height *= image.shape[0]
        xmin = int(x_center - width / 2)
        ymin = int(y_center - height / 2)
        xmax = int(x_center + width / 2)
        ymax = int(y_center + height / 2)
        print(xmin, ymin, xmax, ymax)

        # 绘制矩形和标签
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        # cv2.putText(image, str(int(class_id)), (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # 保存或显示图像
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    cv2.imwrite(os.path.join(output_path, os.path.basename(image_path)), image)
    print(f"Annotated image saved to {output_path}")


def process_images(output_folder):
    # img_files = sorted(os.listdir(img_folder))
    # label_files = sorted(os.listdir(label_folder))

    # for img_file, label_file in zip(img_files, label_files):
    # print(img_file)
    # print(label_file)
    #     image_path = os.path.join(img_folder, img_file)
    #     label_path = os.path.join(label_folder, label_file)
    #     draw_boxes_on_image(image_path, label_path, output_folder)
    image_folder = r""
    label_folder = r""
    target_image_folder = r''
    target_label_folder = r''
    for id in range(2396):
        formatted_id = f"{id:06d}"
        img_file = os.path.join(image_folder, f"{formatted_id}.jpg")
        label_path = os.path.join(label_folder, f"{formatted_id}.txt")

        if os.path.exists(img_file) and os.path.exists(label_path):
            draw_boxes_on_image(img_file, label_path, output_folder)
            shutil.move(img_file, os.path.join(target_image_folder, f"{id}.jpg"))
            shutil.move(label_path, os.path.join(target_label_folder, f"{id}.txt"))
            print(img_file)
            print(label_path)


# 设置路径

output_folder = r""

# 处理图像
process_images(output_folder)
