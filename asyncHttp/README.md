### *说明*
1. **Synchronize.py** 使用同步请求目标服务器约1.2秒返回一次XML
2. **Coroutines.py** 用异步操作实现*Synchronize.py*
### 目的
- 将 **Coroutines.py** 文件所用的异步协程请求与 **Synchronize.py** 文件所使用的同步请求爬取效率做对比
- 异步协程非常适合高频率**IO阻塞**，可自行测试两者间的爬取效率
