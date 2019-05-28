#!/usr/bin/env python
# encoding: utf-8

"""
@description: 模拟下载

@author: baoqiang
@time: 2019-05-28 17:10
"""

import aiohttp
from xasync.coroutinepool import MultiRun
import time

out_path = '/Users/baoqiang/Downloads/pics'

"""
2019-05-28 17:24:56,358 - MultiDownload - INFO - tasks len: 4
download [https://httpbin.org/image/svg] elapsed: 2.093970
download [https://httpbin.org/image/webp] elapsed: 2.134838
download [https://httpbin.org/image/png] elapsed: 2.136627
download [https://httpbin.org/image/jpeg] elapsed: 2.681041
2019-05-28 17:24:59,040 - MultiDownload - INFO - take total elapsed: 2.682030
{'id': 1, 'req': 'https://httpbin.org/image/jpeg', 'filename': '/Users/baoqiang/Downloads/pics/1.jpeg'}
{'id': 2, 'req': 'https://httpbin.org/image/png', 'filename': '/Users/baoqiang/Downloads/pics/2.png'}
{'id': 3, 'req': 'https://httpbin.org/image/svg', 'filename': '/Users/baoqiang/Downloads/pics/3.svg'}
{'id': 4, 'req': 'https://httpbin.org/image/webp', 'filename': '/Users/baoqiang/Downloads/pics/4.webp'}
"""


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            # print(resp.status)
            return await resp.read()


class MultiDownload(MultiRun):
    async def run_one(self, dic):
        start = time.time()
        resp = await fetch(dic['req'])
        print('download [{}] elapsed: {:.6f}'.format(dic['req'], time.time() - start))

        filename = self.build_filename(dic)
        dic['filename'] = filename

        with open(filename, 'wb') as fw:
            fw.write(resp)

        return dic

    def build_filename(self, dic):
        url = dic['req']

        suffix = url[url.rfind('/') + 1:]

        filename = '{}/{}.{}'.format(out_path, dic['id'], suffix)

        return filename


def build_tasks():
    tasks = []

    for i in range(10):
        dic = {
            'id': i,
            'src': 'req: {}'.format(i),
        }

        tasks.append(dic)

    return tasks


# 主运行函数
def multi_download():
    # 构建任务
    tasks = [
        {'id': 1, 'req': 'https://httpbin.org/image/jpeg'},
        {'id': 2, 'req': 'https://httpbin.org/image/png'},
        {'id': 3, 'req': 'https://httpbin.org/image/svg'},
        {'id': 4, 'req': 'https://httpbin.org/image/webp'}
    ]

    # 运行任务并等待结果
    schedule = MultiDownload(tasks)
    results = schedule.run_many()

    # 输出结果
    for dic in results:
        print(dic)


if __name__ == '__main__':
    multi_download()
