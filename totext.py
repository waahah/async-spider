# coding=utf-8
'''
爬取百度文库文档的文字部分
1. 文档网页
2. 提取出每页的数据url
3. 请求每页的数据url(json), 提取其中所有"c"的值
'''

import json
from random import random
from time import sleep
from typing import Optional

import requests as r
from jsonpath import jsonpath


URL = input("请输入文档的网址:\n").strip().split("?")[0]
# SAVE_PATH = "d:/downloads/文档内容.txt"
SAVE_PATH = "文档内容.txt"
# PROXIE = ("127.0.0.1", 7890)
PROXIE = input('请输入代理【如: ("127.0.0.1", 7890)】, 无需则直接回车:\n')
PROXIE = eval(PROXIE) if PROXIE else None


def wait():
    """休眠 0.5-2 秒"""
    sleep(0.5 + 1.5*random())


def genProxies(proxy: Optional[tuple[str, int]]) -> dict[str, str]:
    """生成代理字典"""
    if (not proxy) or (proxy == ("", 0)):
        return {}
    
    h = "http"
    p = "{}://{}:{}".format(h, *proxy)
    return {
        f"{h}": p,
        f"{h}s": p
    }


class WenkuSpider:
    """百度文库文字爬虫"""
    
    headers = {
        'Connection': 'keep-alive',
        'DNT': '1',
        'Pragma': 'no-cache',
        'Referer': 'https://wenku.baidu.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'
    }
    
    def __init__(self, url: str, save_path: str, proxy: Optional[tuple[str, int]]=("", 0)):
        """初始化.

        Args:
            url (str): 百度文库页面的 url
            save_path (str): 文本导出路径 (xxx.txt)
            proxy (tuple[str, int], optional): 代理 (主机, 端口). Defaults to ("", 0).
        """
        # 数据容器
        self.data: list[str] = []
        self.urls: list[str] = []
        self.save_path = save_path
        # 目标网址
        self.url = url
        # 会话对象
        self.s = r.Session()
        self.proxies = genProxies(proxy)
        self.s.headers.update(self.headers)
        
    def getUrlsFromIndex(self):
        """请求主页的 html, 提取出每页的 url 到 self.urls"""
        resp = self.s.get(self.url, proxies=self.proxies)
        resp.raise_for_status()
        
        html = resp.text
        begin = html.index('"htmlUrls":') 
        end = html.index(',"freePage"')
        
        urls_str = html[begin: end].replace('"htmlUrls":', "")
        urls_json = json.loads(urls_str)
        urls = jsonpath(urls_json, r"$..[pageLoadUrl]")
        
        assert urls, f"urls 提取失败, 请检查:\n{urls_str}"
        self.urls = urls
    
    def getTextFromPage(self, url: str):
        """请求一页内容的 url, 提取出文本到 self.data"""
        resp = self.s.get(url, proxies=self.proxies)
        resp.raise_for_status()
        
        doc_str = resp.text
        begin = doc_str.index("(") + 1
        end = doc_str.rindex(")")
        
        doc_str = doc_str[begin: end]
        doc_json = json.loads(doc_str)
        texts = jsonpath(doc_json, r"$..[c]")
        
        assert texts, f"texts 提取失败, 请检查:\n{doc_str}"
        # 过滤掉非字符串的元素
        texts = filter(lambda item: type(item) == str, texts)
        self.data.append("".join(texts))
    
    def export(self):
        """导出 self.data 中的文本到文件"""
        with open(self.save_path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.data))
        print(f"文本已导出至: {self.save_path}")
    
    def fetch(self):
        """请求并提取一份百度文档的文本, 保存到指定路径"""
        print(f"开始请求文档:\n{self.url}")
        self.getUrlsFromIndex()
        print("文档主页请求完毕")
        wait()
        
        size = len(self.urls)
        for i, url in enumerate(self.urls):
            try:
                self.getTextFromPage(url)
            except Exception as e:
                print("\r\n发生异常!")
                print(repr(e))
                break
            # 打印进度并等待
            print(f"\r处理中: 第 {i+1} 页, 共 {size} 页", end=" " * 4)
            wait()
        print()
        
        self.export()


def main():
    global URL, SAVE_PATH, PROXIE

    spider = WenkuSpider(URL, SAVE_PATH, PROXIE)
    spider.fetch()


if __name__ == "__main__":
    main()
