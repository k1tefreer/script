from utils import record_video_increment_name

"""
根据所给的rtsp流来录制视频
假如给定./data_dir/xxx.mp4，自动创建./data_dir文件夹
视频保存为./data_dir文件夹下的xxx.mp4，若xxx.mp4存在，则保存为xxx_1.mp4
依次递增xxx_2.mp4、xxx_3.mp4。。。
"""

if __name__ == "__main__":
    rtsp_url = ""
    # rtsp_url = "rtsp://admin:great123@192.168.8.201:554/qStreaming/Channels/101"
    rtsp_url = "rtsp://admin:jiankong123@192.168.23.22/cam/realmonitor?channel=1&subtype=0"
    write_name = "./paomaodilou_2ban1lou/paomaodilou.mp4"

    record_video_increment_name(rtsp_url, write_name)
