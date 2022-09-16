from urllib import request,error
#import xml.etree.ElementTree
import xml.dom.minidom
import time

"""
1.实现进度条,进度更清晰
2.使用urllib.request同步请求与aiohttp的异步协程请求做对比
"""

def get_requset(count):
    
    base_url = f'https://profile-counter.glitch.me/waahah/count.svg?count={count}'#防止浏览器缓存
    
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'
    }
    #请求对象的定制
    obj_request = request.Request(url=base_url,headers=head)#post请求data传参使用Request
    return obj_request

def get_respponse(obj_request):
    response = request.urlopen(obj_request,timeout=7.0)
    content = response.read().decode('utf-8')
    return content

def down_load(content,count):
    # 使用minidom解析器打开服务器响应的 XML 文档
    DOMTree = xml.dom.minidom.parseString(content)
    collection = DOMTree.documentElement
    #使用xml模块提供的”getElementsByTagName“接口找到需要的节点
    NodeList = collection.getElementsByTagName("tspan")
    global strings     #'实时访问次数为:'
    strings = ',text:'
    for span in NodeList:
        strings = strings + str(span.childNodes[0].data)
        #print (f"span: {str(span.childNodes[0].data)}")
    #print(strings)
    #request.urlretrieve(url=src,filename=f'D:/desktop_backup/DOCX/code/spyter/py/git/{str(count+1)}.svg')
    
if __name__ == '__main__':
    end_count = int(input('请输入访问次数:'))
    print("**************任务进度条**************")
    start = time.perf_counter()
    for count in range(0,end_count):
        try:
            request_obj = get_requset(count)
            content_obj = get_respponse(request_obj)
            down_load(content_obj,count)
        except error.HTTPError as e: #子类写上面
            print(e.getcode(),e.code,sep='\n')
        except error.URLError as e:
            print()
            print(e.reason)
            count-=1
        except TimeoutError as e:
            print(e.winerror)
        finsh = "▓" * round(((count + 1) / end_count) * 80)
        need_do = "-" * round((1- (count + 1) / end_count) * 80)
        progress = ((count + 1) / end_count) * 100
        dur = time.perf_counter() - start
        print("\r{:^3.0f}%[{}->{}]{:.2f}次/s {}/{}{}".format(progress, finsh, need_do, (count+1) /dur,count+1,end_count,strings), end="")
    print()
    print('爬取完毕！！')
