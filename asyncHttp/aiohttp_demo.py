import asyncio
import aiohttp
import time

"""
1.request发起的是同步的网络请求，aiohttp则是异步的
2.aiohttp和asyncio配合使用大约耗时6秒，耗费时间减少了非常多
3.异步遇到阻塞式操作时(如await)，task被挂起，转而执行其他task协程
直到其它协程也挂起或者执行完毕，再执行下一个协程
"""

start = time.time()

async def get(url):
    session = aiohttp.ClientSession()
    response = await session.get(url)
    await response.text()
    await session.close()
    return response

async def request():
    url = 'https://static4.scrape.cuiqingcai.com/'
    print('Waiting for', url)
    response = await get(url)
    print('Get response from', url, 'response')

tasks = [asyncio.ensure_future(request()) for _ in range(100)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

end = time.time()
print('Cost time:', end - start)
