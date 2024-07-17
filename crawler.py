import requests
import json
from urllib import parse
import os
import time

class BaiduImageSpider(object):
    def __init__(self):
        self.json_count = 0  # 请求到的json文件数量（一个json文件包含30个图像文件）
        self.base_url = 'https://image.baidu.com/search/acjson?tn=resu' \
                        'ltjson_com&logid=10578788687989489736&ipn=rj&ct=20' \
                        '1326592&is=&fp=result&fr=&word=%E5%88%B6%E6%9C%8D%E5' \
                        '%B7%A5%E5%9C%B0%E5%A5%97%E8%A3%85&queryWord=%E5%88%B6' \
                        '%E6%9C%8D%E5%B7%A5%E5%9C%B0%E5%A5%97%E8%A3%85&cl=2&lm=&' \
                        'ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&co' \
                        'pyright=&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&' \
                        'nc=1&expermode=&nojc=&isAsync=&pn=180&rn=30&gsm=b4&172049' \
                        '5720170='
        self.directory = "K:\\Greatech\\seed\\{}"  # 存储目录  这里需要修改为自己希望保存的目录  {}不要丢
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
        }

    # 创建存储文件夹
    def create_directory(self, name):
        self.directory = self.directory.format(name)
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        self.directory += r'\{}'

    # 获取图像链接
    def get_image_link(self, url):
        list_image_link = []
        response = requests.get(url, headers=self.header)
        if response.status_code != 200:
            print(f"请求失败，状态码：{response.status_code}")
            return list_image_link
        try:
            json_info = response.json()
        except json.JSONDecodeError:
            print("JSONDecodeError: 响应内容不是有效的JSON")
            return list_image_link

        for data in json_info.get('data', []):
            if 'thumbURL' in data:
                list_image_link.append(data['thumbURL'])
        return list_image_link

    # 下载图片
    def save_image(self, img_link, filename):
        try:
            response = requests.get(img_link, headers=self.header)
            if response.status_code == 200:
                with open(filename, "wb") as f:
                    f.write(response.content)
                    print("存储路径：" + filename)
            else:
                print(f"图片{img_link}下载出错，状态码：{response.status_code}")
        except Exception as e:
            print(f"下载图片{img_link}时出错：{e}")

    # 入口函数
    def run(self):
        search_name = "帅哥24"
        search_name_parse = parse.quote(search_name)

        self.create_directory(search_name)

        pic_number = 0  # 图像数量
        for index in range(self.json_count):
            pn = index * 30  # 每次增加30
            request_url = self.base_url.format(search_name_parse, search_name_parse, pn)
            list_image_link = self.get_image_link(request_url)
            for link in list_image_link:
                if link:  # 确保链接不为空
                    pic_number += 1
                    self.save_image(link, self.directory.format(str(pic_number) + '.jpg'))
                    time.sleep(2)  # 休眠2秒，防止封ip
        print(search_name + "----图像下载完成--------->")

if __name__ == '__main__':
    spider = BaiduImageSpider()
    spider.json_count = 10  # 定义下载10组图像，也就是300张
    spider.run()
