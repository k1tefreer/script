import cv2
import os
# 获取当前目录下所有的.mp4文件
#video_folder = os.getcwd()  # 获取当前工作目录
video_folder = 'help'
#print(video_folder)
video_files = [f for f in os.listdir(video_folder) if f.endswith('.mp4')]

i=0
for video_filename in video_files:
    if i==2:
        break
    # 构造视频文件的完整路径
    video_path = os.path.join(video_folder, video_filename)
    # 构造保存帧的目录名，与视频文件名相同
    frames_folder = os.path.join(video_folder, video_filename.split('.')[0])
    os.makedirs(frames_folder, exist_ok=True)  # 创建文件夹，如果已存在则不创建


    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    frame_id = 0
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
            # 构造每帧图片的保存路径
            frame_save_path = os.path.join(frames_folder, f'{frame_id}.jpg')
            cv2.imwrite(frame_save_path, frame)  # 保存帧为图片
            #print(frame_save_path)
            #print(frame_id)
            frame_id += 24    #操作frame_id增加值可以控制帧间隔
        else:
            break  # 视频读取完毕或发生错误，退出循环
    #i=i+1
    cap.release()  # 释放视频对象
    print(video_filename+'完成')