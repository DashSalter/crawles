import asyncio
import os

import aiofiles
import aiohttp


class ImageSave:
    """图片异步存储"""

    def __init__(self):
        self.__semaphore = None
        self.kwargs = None
        self.image_dict = {}
        self.loop = asyncio.get_event_loop()
        self.timeout = aiohttp.ClientTimeout(total=10)

    @staticmethod
    def __create_path(image_path):  # 路径创建
        path = os.path.split(image_path)[0]
        if path:
            os.makedirs(path, exist_ok=True)

    async def __job(self, url, path):
        async with self.__semaphore:  # 数量锁
            for i in range(3):
                try:
                    async with aiohttp.ClientSession(timeout=self.timeout) as session:
                        async with session.get(url, **self.kwargs) as response:
                            self.__create_path(path)  # 创建图片路径
                            async with aiofiles.open(str(path), 'wb') as f:
                                await f.write(await response.read())
                    break
                except asyncio.TimeoutError:
                    pass
            else:
                print(f'{url} 请求超时')

    def __create_loop(self, url_dict):
        """创建任务队列  为一组进行运行"""
        tasks = [self.loop.create_task(self.__job(url, path)) for url, path in url_dict.items()]  # 建立所有任务
        self.loop.run_until_complete(asyncio.gather(*tasks))

    def image_save(self, image_dict, concurrent=100, timeout=10, **kwargs):
        """多张图片保存{链接:文件保存地址}"""
        self.kwargs = kwargs  # 请求头等信息
        self.timeout = aiohttp.ClientTimeout(total=timeout)  # 超时检测
        self.__semaphore = asyncio.Semaphore(concurrent)  # 最大并发数量
        self.__data_detection(image_dict)  # 数据格式检测
        self.__create_loop(image_dict)  # 协程建立

    @staticmethod
    def __data_detection(iteration_data):
        for url_url, url_path in dict(iteration_data).items():
            if not url_url.startswith('http'):
                raise ValueError(f'数据中的第一个参数不是一个链接，因为它没有携带http协议:{url_url}')


image_save = ImageSave().image_save
# {链接: 文件保存地址, 链接: 文件保存地址}
