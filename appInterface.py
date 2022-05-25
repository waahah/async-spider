from urllib import request,error
from urllib import parse
#import lxml.etree
import random
import json
import time
import os	
import sys

def get_requset(num):
    
    base_url = 'http://service.picasso.adesk.com/v1/vertical/category/4e4d610cdf714d2966000000/vertical?'
    date = {
        'limit':30,  #每页固定返回30条
        'skip':num,
        'first':0,
        'order':'hot' #热图爬完可将此参数替换为new(hot组大约有640个)
    }
    head = {
        #有时请求头信息不够，所以访问不成功，（UA，Cookie...等在请求标头里）
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'
    }
    word = parse.urlencode(date)
    new_url = base_url+word
    #请求对象的定制
    re = request.Request(url=new_url,headers=head)#post请求data传参使用Request且需进行编解码
    proxies_pool = [
        {'http' : '122.9.101.6:8888'}, #快代理免费IP，容易失效报错
        {'http' : '101.132.186.175:9090'}, #上海联通
        {'http' : '183.247.211.50:30001'} #浙江台州
    ]
    proxies = random.choice(proxies_pool)#简单随机代理，也可用redis缓存数据库
    headler = request.ProxyHandler(proxies=proxies)
    opener = request.build_opener(headler)
    args = (re,opener)#元组
    return args

def get_respponse(re,opener):
    response = opener.open(re)
    content = response.read()#字节类型
    obj_json = json.loads(content)#字典类型
    return obj_json
 
def down_load(obj_json):
    #print(obj_json['res'])
    num_list = obj_json['res']['vertical']#列表
    print(type(num_list))
    #html_tree = etree.HTML(content) 解析服务器响应的文件 本地文件用etree.parse()
    #nameList = html_tree.xpath('//div[@id="container"]//a/img/@alt')
    for i in range(len(num_list)):
        global k
        k+=1
        name = num_list[i]['id']
        src = num_list[i]['img']
        if name == '' and src == '':
            print('此组下载完毕')
            break
        request.urlretrieve(url=src,filename=f'{path}/{str(name)}.jpg')
        print(f'打印 {str(name)}完成！已下载{str(k)}张')
        time.sleep(1)
    
    
if __name__ == '__main__':
    
    path = sys.path[0] + '\\ImgPic'	#获取文件夹路径
    #判断文件夹是否存在，如果不存在则新建
    if not os.path.exists(path):
        os.mkdir(path)
    os.chdir(path)						#切换到Path目录
    #start_page = int(input('请输入开始页码:'))
    end_page = int(input('请输入要打印的页码（一页三十张）:'))
    k = 0
    for num in range(0,end_page):
        jishu = num*30
        try:
            request_obj = get_requset(jishu)
            #使用*号解包元组
            content_obj = get_respponse(*request_obj)
        except error.HTTPError as e:
            print(e.getcode(),e.code,sep='\n')
        except error.URLError as e:
            print(f'出错啦！{e.reason}')
        else:
            down_load(content_obj)
    print('爬取完毕！！!')