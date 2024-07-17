import argparse
import os
import platform
import sys
from pathlib import Path
import cv2

import torch
from torchvision import transforms
import time

from models.experimental import attempt_load
from utils.general import non_max_suppression

from shapely.geometry import Polygon

# 加载模型

import cv2
import queue
import threading

# import yolov5  # 假设你已经有了一个可以工作的YOLOv5模块

# 假设的RTSP地址列表
rtsp_urls = ['rtsp://admin:jiankong123@192.168.23.17:554/cam/realmonitor?channel=1&subtype=0',
             'rtsp://admin:jiankong123@192.168.23.19:554/cam/realmonitor?channel=1&subtype=0',
             'rtsp://admin:jiankong123@192.168.23.20:554/cam/realmonitor?channel=1&subtype=0',
             'rtsp://admin:jiankong123@192.168.23.22:554/cam/realmonitor?channel=1&subtype=0',
             'rtsp://admin:jiankong123@192.168.23.23:554/cam/realmonitor?channel=1&subtype=0',
             'rtsp://admin:jiankong123@192.168.23.24:554/cam/realmonitor?channel=1&subtype=0',
             'rtsp://admin:jiankong123@192.168.23.25:554/cam/realmonitor?channel=1&subtype=0',
             'rtsp://admin:jiankong123@192.168.23.26:554/cam/realmonitor?channel=1&subtype=0',
             'rtsp://admin:jiankong123@192.168.23.27:554/cam/realmonitor?channel=1&subtype=0',
             'rtsp://admin:jiankong123@192.168.23.31:554/cam/realmonitor?channel=1&subtype=0',
             'rtsp://admin:jiankong123@192.168.23.10:554/Streaming/Channels/101',
             'rtsp://admin:jiankong123@192.168.23.11:554/Streaming/Channels/101',
             'rtsp://admin:jiankong123@192.168.23.12:554/Streaming/Channels/101',
             'rtsp://admin:jiankong123@192.168.23.13:554/Streaming/Channels/101',
             'rtsp://admin:jiankong123@192.168.23.14:554/Streaming/Channels/101',
             'rtsp://admin:jiankong123@192.168.23.15:554/Streaming/Channels/101',
             'rtsp://admin:jiankong123@192.168.23.16:554/Streaming/Channels/101',
             'rtsp://admin:jiankong123@192.168.23.17:554/Streaming/Channels/101',
             'rtsp://admin:jiankong123@192.168.23.18:554/Streaming/Channels/101'
             ]

# 线程安全的队列
image_queue = queue.Queue(64)
task1_queue = queue.Queue(64)
task2_queue = queue.Queue(64)


# 摄像头读取线程函数
def read_camera(rtsp_url, queue1, queue2):
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print(f"Error opening {rtsp_url}")
    while (not cap.isOpened()):
        cap = cv2.VideoCapture(rtsp_url)

    while True:
        time.sleep(0.1)
        ret, frame = cap.read()
        if ret:
            queue1.put_nowait(frame)  # 将帧放入队列
            queue2.put_nowait(frame)
            # print("put: frame:",rtsp_url)
            if '192.168.23.17' in rtsp_url:
                cv2.imshow(rtsp_url, frame)
                cv2.waitKey(40)
        else:
            cap = cv2.VideoCapture(rtsp_url)

        # 批量检测线程函数


def distribute_queue(queue, batch_size=32):
    while True:
        imageslst = []
        for _ in range(batch_size):
            try:
                time.sleep(0.01)
                imageslst.append(queue.get_nowait())  # 尝试非阻塞地获取图片
                print("get: *******************************************", len(imageslst))
            except Exception as e:
                print("no pic")
                break  # 如果队列中没有足够的图片，则退出循环


def batch_test1(queue, model, batch_size=32):
    # model = load_detector('yolov5s.pt', device='cuda:0')
    wallPoints = [(300, 100), (300, 400), (400, 400), (500, 380), (400, 100)]
    thresh_person = 0.1
    inter_ratio = 0.1
    while True:
        imageslst = []
        for _ in range(batch_size):
            try:

                imageslst.append(queue.get_nowait())  # 尝试非阻塞地获取图片
                print("get: *******************************************", len(imageslst))
            except Exception as e:
                # print("no pic")
                break  # 如果队列中没有足够的图片，则退出循环

        if len(imageslst) > 0:
            print("imageslst  ", len(imageslst))
            tensor_images = []
            # 应用转换并转换为张量
            for img in imageslst:
                img = cv2.resize(img, (640, 640))
                img = torch.from_numpy(img).to('cuda:0')
                img = img.float()
                img /= 255
                tensor_images.append(img)
            # 使用torch.stack来创建一个新的维度（batch维度），这要求所有图像具有相同的尺寸
            # 注意：stack会增加一个新的维度（在这里是第一个维度），所以输出张量的形状将是(batch_size, C, H, W)
            batch_tensor = torch.stack(tensor_images, dim=0)
            batch_tensor = batch_tensor.permute(0, 3, 1, 2)
            fanyue_pic(imageslst, batch_tensor, model, wallPoints, thresh_person, inter_ratio, device='cuda:0')


def batch_test2(queue, model, batch_size=32):
    # model = load_detector('yolov5s.pt', device='cuda:0')
    wallPoints = [(300, 100), (300, 400), (400, 400), (500, 380), (400, 100)]
    thresh_person = 0.1
    inter_ratio = 0.1
    while True:
        imageslst = []
        for _ in range(batch_size):
            try:

                imageslst.append(queue.get_nowait())  # 尝试非阻塞地获取图片
                print("get: *******************************************", len(imageslst))
            except Exception as e:
                # print("no pic")
                break  # 如果队列中没有足够的图片，则退出循环

        if len(imageslst) > 0:
            print("imageslst  ", len(imageslst))
            tensor_images = []
            # 应用转换并转换为张量
            for img in imageslst:
                img = cv2.resize(img, (640, 640))
                img = torch.from_numpy(img).to('cuda:0')
                img = img.float()
                img /= 255
                tensor_images.append(img)
            # 使用torch.stack来创建一个新的维度（batch维度），这要求所有图像具有相同的尺寸
            # 注意：stack会增加一个新的维度（在这里是第一个维度），所以输出张量的形状将是(batch_size, C, H, W)
            batch_tensor = torch.stack(tensor_images, dim=0)
            batch_tensor = batch_tensor.permute(0, 3, 1, 2)
            fanyue_pic(imageslst, batch_tensor, model, wallPoints, thresh_person, inter_ratio, device='cuda:0')


def fanyue_batch(queue, batch_size=3):
    # model = load_detector('yolov5s.pt', device='cuda:0')
    wallPoints = [(10, 10), (10, 600), (600, 600), (600, 10)]
    thresh_person = 0.25
    inter_ratio = 0.1
    while True:
        imageslst = []
        for _ in range(batch_size):
            # try:
            imageslst.append(queue.get_nowait())  # 尝试非阻塞地获取图片
            # except queue.empty():
            #     continue  # 如果队列中没有足够的图片，则退出循环

        if imageslst:
            tensor_images = []
            # 应用转换并转换为张量
            for img in imageslst:
                img = cv2.resize(img, (640, 640))
                img = torch.from_numpy(img).to('cuda:0')
                img = img.float()
                img /= 255
                tensor_images.append(img)
            # 使用torch.stack来创建一个新的维度（batch维度），这要求所有图像具有相同的尺寸
            # 注意：stack会增加一个新的维度（在这里是第一个维度），所以输出张量的形状将是(batch_size, C, H, W)
            batch_tensor = torch.stack(tensor_images, dim=0)
            batch_tensor = batch_tensor.permute(0, 3, 1, 2)

            # img = torch.from_numpy(batch_tensor).to('cuda:0')
            # img = img.float()  # uint8 to fp16/32
            # img /= 255
            # 使用YOLOv5进行批量检测
            # results = yolov5.detect(images)  # 假设detect函数接受一个图片列表并返回结果列表
            fanyue_pic(batch_tensor, model, wallPoints, thresh_person, inter_ratio, device='cuda:0')
            # 处理结果...


def load_detector(model_path, device='cpu'):
    model = attempt_load(model_path, device)
    model.eval()
    return model


def calculate_intersection_ratio(polygon_a_vertices, polygon_b_vertices):
    # 创建多边形A和B的shapely对象
    polygon_a = Polygon(polygon_a_vertices)
    polygon_b = Polygon(polygon_b_vertices)

    # 计算交集多边形C
    # intersection_polygon = intersection(polygon_a, polygon_b)
    intersection_polygon = polygon_a.intersection(polygon_b)
    # 检查是否有交集
    if intersection_polygon.is_empty:
        return 0.00  # 没有交集，返回0

    # 计算多边形B的面积和交集C的面积
    area_b = polygon_b.area
    area_intersection = intersection_polygon.area

    # 计算交集占多边形B的比例
    ratio = area_intersection / area_b

    # 保留两位小数
    return round(ratio, 2)


# 推理然后判断是否和墙有交集
def fanyue_pic(imageslst, imgs, model, wallPoints, thresh_person, inter_ratio, device='cpu'):
    # 前向传播
    # while 1:

    pred = model(imgs)[0]  # 前向传播，只获取预测结果（因为我们只预测一张图片）

    # 非极大值抑制（NMS）
    pred = non_max_suppression(pred, conf_thres=0.1, iou_thres=0.5)  # 你可以调整 conf_thres 和 iou_thres

    # condition = pred[:, -1] == 0
    # # 使用布尔索引来选择满足条件的行
    # pred = pred[condition]
    # 解析预测结果
    for ba, pic in zip(pred, imageslst):
        for det in ba:  # det 是一个列表，每个元素是一个字典，表示一个检测到的物体
            per = det.cpu().numpy()
            x1, y1, x2, y2, score, cls = per
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            if score > thresh_person and cls == 0:
                # polygon_a_vertices = wallPoints
                polygon_person = [(x1, y1), (x1, y2), (x2, y2), (x2, y1)]
                ratio = calculate_intersection_ratio(wallPoints, polygon_person)
                # print(per)
                print("ratio:  ", ratio)
                # pic = cv2.resize(pic, (640, 640))
                # cv2.rectangle(pic, (x1,y1), (x2,y2), (255, 0, 0), 3)
                # cv2.imshow('roi', pic)
                # cv2.waitKey(5)
                # cv2.rectangle(img_org, (x1,y1), (x2,y2), (255, 0, 0), 3)
                # for i in range(len(wallPoints)-1):
                #     cv2.line(img_org,wallPoints[i],wallPoints[i+1], (255, 255, 0), 5)
                # cv2.line(img_org, wallPoints[0], wallPoints[- 1], (255, 255, 0), 5)

        # cv2.imshow('fuck',img_org)
        # cv2.waitKey(0)
        # 这里可以根据你的需要添加更多逻辑，比如绘制边界框等
        # 368 180     460 536


def old_main():
    img = cv2.imread('friday.png')
    img = cv2.resize(img, (640, 640), interpolation=cv2.INTER_LINEAR)
    wallPoints = [(300, 100), (300, 400), (400, 400), (500, 380), (400, 100)]
    print(wallPoints[0])
    polygon_a_vertices = '[(0, 0), (1, 0), (1, 1), (0, 1)]'
    polygon_a_vertices.strip()
    print(polygon_a_vertices)
    polygon_b_vertices = '[(0.5, 0.5), (1.5, 0.5), (1.5, 1.5), (0.5, 1.5)]'

    thresh_person = 0.25
    inter_ratio = 0.05

    model = load_detector('yolov5s.pt', device='cuda:0')

    img_org = img
    img = torch.from_numpy(img).to('cuda:0')
    img = img.float()  # uint8 to fp16/32
    img /= 255

    img = img.unsqueeze(0).permute(0, 3, 1, 2)  # 添加批次维度，因为我们只预测一张图片
    imgs = img.repeat(64, 1, 1, 1)
    # rtsp = ''
    # cap = cv2.VideoCapture(rtsp)
    while True:
        t1 = time.time()

        inputimg = imgs

        # ret, frame = cap.read()
        # img = cv2.resize(imgs, (640, 640), interpolation=cv2.INTER_LINEAR)
        # img = torch.from_numpy(img).to('cuda:0')
        # img = img.float()  # uint8 to fp16/32
        # img /= 255

        fanyue_pic(inputimg, model, wallPoints, thresh_person, inter_ratio, device='cuda:0')
        t2 = time.time()
        print(t2 - t1)
        # time.sleep(3)


if __name__ == '__main__':

    model1 = load_detector('yolov5s.pt', device='cuda:0')
    model2 = load_detector('yolov5s.pt', device='cuda:0')
    # 创建摄像头读取线程
    threads = []
    for k in range(1):
        for rtsp_url in rtsp_urls:
            time.sleep(0.1)
            t = threading.Thread(target=read_camera, args=(rtsp_url, task1_queue, task2_queue))
            t.start()
            threads.append(t)

    # 创建批量检测线程（可以是一个单独的线程，也可以是多个线程来并行处理）
    batch_size = 64
    detect_thread1 = threading.Thread(target=batch_test1, args=(task1_queue, model1, batch_size))
    detect_thread1.start()
    detect_thread2 = threading.Thread(target=batch_test2, args=(task2_queue, model2, batch_size))
    detect_thread2.start()

    # 等待所有线程完成（注意：这里只是一个示例，实际中你可能需要更复杂的线程管理）
    for t in threads:
        t.join()
    detect_thread1.join()
    detect_thread2.join()
