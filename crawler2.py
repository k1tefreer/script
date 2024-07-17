import requests
import json
from urllib import parse
import os
import time

class BaiduImageSpider(object):
    def __init__(self):
        self.json_count = 0  # 请求到的json文件数量（一个json文件包含30个图像文件）
        self.base_url = ''
        self.directory = "K:\\Greatech\\seed\\{}"  # 存储目录  这里需要修改为自己希望保存的目录  {}不要丢
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
        }

    # 创建存储文件夹
    def create_directory(self, name):
        self.directory = self.directory.format(name)
        # 如果目录不存在则创建
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        self.directory += r'\{}'

    # 获取图像链接
    def get_image_link(self, url):
        list_image_link = []
        strhtml = requests.get(url, headers=self.header)  # Get方式获取网页数据
        jsonInfo = json.loads(strhtml.text)
        for item in jsonInfo['data']:
            if 'thumbURL' in item:
                list_image_link.append(item['thumbURL'])
        return list_image_link

    # 下载图片
    def save_image(self, img_link, filename):
        res = requests.get(img_link, headers=self.header)
        if res.status_code == 404:
            print(f"图片{img_link}下载出错------->")
        with open(filename, "wb") as f:
            f.write(res.content)
            print("存储路径：" + filename)

    # 入口函数
    def run(self):
        # searchName = input("查询内容：")
        searchName = "连体制服"
        searchName_parse = parse.quote(searchName)  # 编码

        self.create_directory(searchName)

        pic_number = 0  # 图像数量
        for index in range(self.json_count):
            pn = index * 30
            request_url = self.base_url.format(searchName_parse, searchName_parse, pn)
            list_image_link = self.get_image_link(request_url)
            for link in list_image_link:
                pic_number += 1
                self.save_image(link, self.directory.format(str(pic_number) + '.jpg'))
                time.sleep(2)  # 休眠2秒，防止封ip
        print(searchName + "----图像下载完成--------->")

if __name__ == '__main__':
    spider = BaiduImageSpider()
    spider.json_count = 10   # 定义下载10组图像，也就是三百张
    spider.run()