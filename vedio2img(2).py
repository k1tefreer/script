import cv2
import os
import time


def video_to_images(video_path, output_folder):
    """
    将MP4视频转换为每秒一张照片，确保不覆盖以前的图片

    :param video_path: 输入视频文件路径
    :param output_folder: 输出图片文件夹路径
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

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 每秒保存一帧
        if frame_number % fps == 0:
            timestamp = int(time.time() * 1000)
            image_path = os.path.join(output_folder, f"frame_{timestamp}.jpg")
            cv2.imwrite(image_path, frame)
            print(f"保存: {image_path}")

        frame_number += 1

    cap.release()
    print("转换完成！")


if __name__ == "__main__":
    video_folder = ""  # 替换为您的视频文件夹路径
    output_folder = ""  # 替换为您希望保存图片的文件夹路径

    # 获取文件夹中所有的MP4文件
    video_files = [f for f in os.listdir(video_folder) if f.endswith('.mp4')]

    for video_file in video_files:
        video_path = os.path.join(video_folder, video_file)
        print(f"正在处理视频: {video_path}")
        video_to_images(video_path, output_folder)