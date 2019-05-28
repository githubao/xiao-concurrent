#!/usr/bin/env python
# encoding: utf-8

"""
@description: 使用协程count总数

@author: baoqiang
@time: 2019-05-28 16:28
"""

import asyncio
import time

now = lambda: time.time()


# 平方操作
async def exp2(x):
    # 模拟耗时操作
    # await asyncio.sleep(x)
    await time_task(x)

    return x * x


# 某个耗时的工作
async def time_task(x):
    # 每一步耗时工作都要异步io
    await asyncio.sleep(x)
    return x * x


def run():
    """
    total: 14
    elapsed: 3.0034842491149902
    :return:
    """

    start = now()

    # cos
    cos = [exp2(i) for i in range(1, 4)]

    # run tasks
    tasks = [asyncio.ensure_future(co) for co in cos]

    # event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

    # print result
    total = sum(task.result() for task in tasks)
    print('total: {}'.format(total))

    # time elapsed
    print('elapsed: {}'.format(now() - start))


if __name__ == '__main__':
    run()
