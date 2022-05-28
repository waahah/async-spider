import asyncio
import aiohttp
import time

"""
1.aiohttp是基于acyncio的异步HTTP网络模块，可以支持非常高的并发量，如百万并发
2.测试一下百度并发量分别为1,3,5,10,......,500时的耗时情况
"""

def test(number):
    start = time.time()
    
    async def get(url):
        session = aiohttp.ClientSession()
        
        response = await session.get(url)
        await response.text()
        await session.close()
        return response
    
    async def request():
        url = 'https://www.baidu.com/'
        await get(url)
    
    tasks = [asyncio.ensure_future(request()) for _ in range(number)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    
    end = time.time()
    print('Number:', number, 'Cost time:', end - start)

for number in [1, 3, 5, 10, 15, 30, 50, 75, 100, 200, 500]:
    test(number)