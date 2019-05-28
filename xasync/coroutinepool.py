#!/usr/bin/env python
# encoding: utf-8

"""
@description: 实现一个线程池框架

@author: baoqiang
@time: 2019-05-28 16:41
"""

import asyncio
import logging
import random
import time

RETRY_TIMES = 3

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def now():
    return time.time()


class MultiRun:
    def __init__(self, datas):
        self.datas = datas
        self.logger = logging.getLogger(self.__class__.__name__)

    def run_many(self):
        self.logger.info("tasks len: {}".format(len(self.datas)))
        start = now()

        # cos
        cos = [self.safe_one(dic) for dic in self.datas]

        # run tasks
        tasks = [asyncio.ensure_future(co) for co in cos]

        # event loop
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))

        # time elapsed
        self.logger.info('take total elapsed: {:.6f}'.format(now() - start))

        for task in tasks:
            yield task.result()

    async def safe_one(self, dic):
        for _ in range(RETRY_TIMES):
            try:
                return await self.run_one(dic)
            except Exception as e:
                self.logger.exception("[{}] err occur: {}".format(dic, e))

        self.logger.error("fail to execute: {}".format(dic))

        return None

    async def run_one_sample(self, dic):
        sleep_time = random.random()
        await asyncio.sleep(sleep_time)

        if sleep_time > 0.8:
            raise Exception("TIME OUT")

        result = 'updated: {}'.format(dic['id'])
        dic['res'] = result

        self.logger.info('[{}] sleeped: {:.6f}'.format(dic, sleep_time))

        return dic

    async def run_one(self, dic):
        raise NotImplementedError


# 实现类，需要继承multirun，并重新run_one实现具体的耗时逻辑，把结果放在dic里面
class MultiHello(MultiRun):
    async def run_one(self, dic):
        return await self.run_one_sample(dic)


# 构建任务队列
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
def multi_hello_run():
    # 构建任务
    tasks = build_tasks()

    # 运行任务并等待结果
    schedule = MultiHello(tasks)
    results = schedule.run_many()

    # 输出结果
    for dic in results:
        print(dic)


if __name__ == '__main__':
    multi_hello_run()
