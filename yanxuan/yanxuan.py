from alive_progress import alive_bar
from urllib import request, error
from lxml import etree
from fpdf import FPDF
import warnings
import time
import json
import ssl
import sys
import re
import os


class PDF(FPDF):

    """
    覆盖footer方法
    """
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('helvetica', 'I', 10)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


def is_contains_chinese(strs):
    """
    :param strs: str
    :return: boolean
    """
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False

def find_string(strs):
    """
    :param strs: str
    :return: boolean
    """
    re = 'zhuanlan.zhihu.com/p/'
    flag = re in strs
    return flag

def SSL_ignore():
    """
    忽略局部SSL证书鉴证(不忽略有时会报错)
    :return: object
    """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def mkdir():
    try:
        """
        解决打包后无法获取当前路径的问题
        检查应用程序是作为脚本还是作为冻结的可执行程序运行
        """
        if getattr(sys, 'frozen', False):
            route = os.path.dirname(sys.executable)
        elif __file__:
            route = os.path.dirname(__file__)
        # route = sys.path[0]
        dict = {
            # 获取文件夹路径
            'dl_path': f'{route}\\Download',
            'rs_path': f'{route}\\Resources'
        }
        for path in dict:
            # 判断文件夹是否存在，如果不存在则新建
            if not os.path.exists(dict[path]):
                os.mkdir(dict[path])
        os.chdir(route)
    except FileNotFoundError as e:
        print(f'errno：{e.args}')
    except FileExistsError as e:
        print(f'errno：{e.args}')

def get_header(link):
    """
    :param link: str or int
    :return: dict
    """
    if isinstance(link, int):
        type = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        Content_Type = ''
    else:
        type = 'application/json, text/javascript, */*; q=0.01'
        Content_Type = 'application/x-www-form-urlencoded; charset=UTF-8'

    head = {

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26',
        'Accept': f'{type}',
        #'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Content_Type': f'{Content_Type}',
        #'Cookie': '_ga=GA1.1.2113798598.1667634833; _ga_8FFK39NHRM=GS1.1.1669041218.13.1.1669041219.0.0.0',
        'Host': 'mfyx.top',
        'original_text_for': 'https://mfyx.top',
        'Referer': 'https://mfyx.top/',
        'sec-ch-ua': '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "Windows",
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'

    }
    return head


def requset_POST(link):
    """
    封装定制的POST请求对象
    :param link: str
    :return: object
    """
    base_url = 'https://mfyx.top/api/search'

    data = {
        "url": [f"{link}"]
    }

    data = json.dumps(data)
    new_data = data.encode("ascii")

    head = get_header(link)

    # 请求对象的定制
    obj_request = request.Request(url=base_url, data=new_data, headers=head)  # post请求传参使用Request
    return obj_request


def requset_GET(id):
    """
    封装定制的GET请求对象
    :param id: int
    :return: object
    """
    if isinstance(id, int):
        base_url = f"https://mfyx.top/archives/{id}"  
        head = get_header(id)
        methed = 'GET'
        obj_request = request.Request(url=base_url, headers=head)
        return obj_request


def get_response(obj_request, ctx):
    """
    封装定制的response对象
    :param obj_request: object
    :param ctx: object
    :return: str
    """
    response = request.urlopen(obj_request, context=ctx)
    content = response.read().decode('utf-8')
    # print(content)
    return content


def import_img(pdf, i, x, tp):
    """
    :param pdf: object
    :param i: int
    :param x: str
    :param tp: str
    """
    # x = x.split('?')[0]
    request.urlretrieve(url=x, filename=f'./Download/{str(i)}.{tp}')#
    pdf.image(f'./Download/{str(i)}.{tp}', w=182, type=f'{tp}')  # 一个显式尺寸
    os.remove(f'./Download/{str(i)}.{tp}')
    pdf.ln(1.0)


def save_pdf(article, title):
    """
    :param article: list
    :param title: str
    """

    config = {
        'font_path': './Resources/simfang.ttf',
        'orientation': "P",  # 纸张方向
        'unit': "mm",  # 纸张大小单位
        'format': "A4",
        'font_family': 'simfang',
        'font_weight': "B",
        'font_size': 13,
        'title_size': 15,
        'cell_width': 182,
        'cell_height': 13,
        'text_align': 'L',
        'title_align': 'C',
        'cell_left_margin': 15
    }

    pdf = PDF(config['orientation'], config['unit'], config['format'])
    pdf.alias_nb_pages()
    pdf.add_page()  # Add a page
    try:
        pdf.add_font(config['font_family'], config['font_weight'], config['font_path'], uni=True)
        #pdf.set_font(config['font_family'], config['font_weight'], config['font_size'])  # set style and size of font
        pdf.set_left_margin(config['cell_left_margin'])
        pdf.set_title('waahah')
        pdf.set_font(config['font_family'], config['font_weight'], config['title_size'])
        pdf.multi_cell(w=config['cell_width'], h=config['cell_height'], txt=f'{title}', align=config['title_align'])
        pdf.ln(5)
        pdf.set_font(config['font_family'], config['font_weight'], config['font_size'])
        # insert the texts in pdf
        k = 0
        with alive_bar(100, ctrl_c=False, title=f'下载中 ', bar='halloween', spinner='elements') as bar:
            for x in article:
                if '.png' in x:
                    k += 1
                    import_img(pdf, k, x, 'png')
                elif '.jpg' in x or '.jpeg' in x:
                    k += 1
                    import_img(pdf, k, x, 'jpg')
                else:
                    pdf.multi_cell(w=config['cell_width'], h=config['cell_height'], txt=x, align=config['text_align'])
                bar()
        # pdf.output("path where you want to store pdf file\\file_name.pdf")
        warnings.filterwarnings("ignore")
        pdf.output(f"./Download/{title}.pdf", 'F')
        print(f'已为小主保存为PDF，共有{pdf.page_no()}页')
        warnings.filterwarnings('default')
    except RuntimeError as e:
        print(f'error：{e.args}')
    except PermissionError as e:
        if e.errno is 13:
            print(f'{e.filename} 正在被占用，请暂时关闭占用程序', f'错误信息 errno：{e.args}',sep='\n')
        else:
            print(f'保存时出现错误 errno：{e.args}')


def down_load(content, ctx):
    """
    :param content: str
    :param ctx: object
    """
    print(type(content))
    obj_dict = json.loads(content)
    code = obj_dict['code']
    message = obj_dict['message']
    if code is 0:
        id = obj_dict['id']
        title = obj_dict['title']
        title = re.sub('[\/:：*&？?“"，,。.（）()》|《！!]','',title)
        description = obj_dict['description']
        print()
        print(f"主题：「{title}」", f"简介：{description}", sep='\n')
        print()
        print('正在解析,时间过长请重新尝试...')
        res = requset_GET(id)
        req = get_response(res, ctx)
        html_tree = etree.HTML(req)
        # 获取相应的数据
        article = html_tree.xpath("//div[@class='article']/div[@id='lightgallery']/p/text()|//div[@id='lightgallery']/p/img/@src")
        save_pdf(article,title)
    elif code is -1:
        print()
        print(message)


if __name__ == '__main__':
    print('''
                             /\ \              /\ \        
 __  __  __     __       __  \ \ \___      __  \ \ \___    
/\ \/\ \/\ \  /'__`\   /'__`\ \ \  _ `\  /'__`\ \ \  _ `\  
\ \ \_/ \_/ \/\ \L\.\_/\ \L\.\_\ \ \ \ \/\ \L\.\_\ \ \ \ \ 
 \ \___x___/'\ \__/.\_\ \__/.\_\\ \_\ \_\ \__/.\_\\ \_\ \_\
 by——吾爱破解waahah                                                        
''')
    while True:
        url = input('请输入分享链接：')#"https://www.zhihu.com/market/paid_column/1515058050263834624/section/1515418851320066048"
        start = time.perf_counter()
        boolean = is_contains_chinese(url)
        zhi = find_string(url)
        if boolean is not True and zhi is False:
            try:
                mkdir()
                request_obj = requset_POST(url)
                sslContext = SSL_ignore()
                content_obj = get_response(request_obj, sslContext)
                down_load(content_obj, sslContext)
            except error.HTTPError as e:  # 子类写上面
                print(f'连接出现了点问题呢,错误代码：{e.getcode()}', f'错误原因：{e.reason}', sep='\n')
            except error.URLError as e:
                print()
                print(f'控制台日志：{e.reason}')
            except TimeoutError as e:
                print(f"响应超时,请重新尝试；{e.winerror}")
        else:
            print("输入的格式不正确!")
        dur = time.perf_counter() - start
        print()
        print('共耗费小主{:.2f}秒，Goodbye！'.format(dur))
