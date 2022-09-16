import asyncio
import requests
import time

"""
1.下面url网站服务器强制等待5秒才返回响应
2.此程序大约耗时66秒，使用协程常犯错误示例，其他正确示例作为对比
3.http协程仅将涉及IO操作的代码封装到async修饰的方法里是不可行的
4.只有使用支持异步操作的请求方式才可以实现真正的异步（如aiohttp异步请求库）
"""

start = time.time()


async def get(url):
    return requests.get(url)


async def request():
    url = 'https://static4.scrape.cuiqingcai.com/'
    print('Waiting for', url)
    response = await get(url)
    print('Get response from', url, 'response', response)


tasks = [asyncio.ensure_future(request()) for _ in range(10)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

end = time.time()
print('Cost time:', end - start)
