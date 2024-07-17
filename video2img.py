import cv2
import os

def video_to_images(video_path, output_folder, base_name, start_index):
    """
    将MP4视频转换为每秒一张照片，确保不覆盖以前的图片

    :param video_path: 输入视频文件路径
    :param output_folder: 输出图片文件夹路径
    :param base_name: 输出图片文件的基础名称
    :param start_index: 起始图片编号
    :return: 处理后最后的图片编号
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)

    # 获取视频的帧率
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps

    print(f"视频帧率: {fps} FPS")
    print(f"视频总帧数: {frame_count}")
    print(f"视频时长: {duration:.2f} 秒")

    frame_number = 0
    image_index = start_index

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 每秒保存一帧
        if frame_number % fps == 0:
            image_path = os.path.join(output_folder, f"{base_name}{image_index}.jpg")
            cv2.imwrite(image_path, frame)
            print(f"保存: {image_path}")
            image_index += 1

        frame_number += 1

    cap.release()
    print("转换完成！")
    return image_index


if __name__ == "__main__":
    video_folder = "ip4"  # 替换为您的视频文件夹路径
    output_folder = "op4"  # 替换为您希望保存图片的文件夹路径
    base_name = "hcy"  # 基础名称

    # 获取文件夹中所有的MP4文件
    video_files = [f for f in os.listdir(video_folder) if f.endswith('.mp4')]

    current_index = 1

    for video_file in video_files:
        video_path = os.path.join(video_folder, video_file)
        print(f"正在处理视频: {video_path}")
        current_index = video_to_images(video_path, output_folder, base_name, current_index)
