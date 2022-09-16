import asyncio
import aiohttp
import time

"""
1.此文件是使用aiohttp基于acyncio的异步HTTP网络模块，支持非常高的并发量
2.与request的同步请求做对比
"""

def test(number):
    start = time.time()
    
    async def get(url,concurrency,total):
        data = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'
        }
        #并发限制,避免网站被瞬间爬挂掉
        semaphore = asyncio.Semaphore(concurrency)
        #使用信号量上下文对象控制进入的最大协程数量
        async with semaphore:
            #超时设置,响应超时则抛出TimeoutError异常,不再等待
            timeout = aiohttp.ClientTimeout(total=total)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url,data=data) as response:
                #response = await session.get(url,data=data)
                    await response.text()
                    await session.close()
                    return response
    
    async def request():
        url = 'https://profile-counter.glitch.me/waahah/count.svg'
        #并发量
        bingfacount = 50
        #超时时间s
        sec = 20
        await get(url,bingfacount,sec)
    #多任务协程列表
    tasks = [asyncio.ensure_future(request()) for _ in range(number)]
    #创建事件循环
    loop = asyncio.get_event_loop()
    #注册到事件循环并运行
    loop.run_until_complete(asyncio.wait(tasks))
    
    end = time.time()
    print('Number:', number, 'Cost time:', end - start)

for number in [10,30,100,150,200,500]:
    try:   
        test(number)
    except aiohttp.ClientError as e:
        print(e.with_traceback())
    except asyncio.TimeoutError as e:
        print("响应超时")
