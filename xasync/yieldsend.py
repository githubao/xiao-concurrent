#!/usr/bin/env python
# encoding: utf-8

"""
@description: yield & send

@author: baoqiang
@time: 2019-05-05 17:12
"""

import asyncio


def jumping_range(up_to):
    """
    next(iter): 调用iter进入函数运行到yield index，返回index跳出iter
    iter.send(data), 唤起调用函数，把send的值赋值给右边的数
    """
    index = 0
    while index < up_to:
        print("enter")
        jump = yield index
        if jump is None:
            jump = 1
        index += jump


def send_demo():
    iterator = jumping_range(5)
    print(next(iterator))  # 0
    print(iterator.send(2))  # 2
    print(next(iterator))  # 3
    print(iterator.send(-1))  # 2
    for x in iterator:
        print(x)  # 3, 4


@asyncio.coroutine
def countdown(name, n):
    while n > 0:
        print('T-minus: [{}], {}'.format(name, n))
        yield from asyncio.sleep(1)
        n -= 1


async def countdown2(name, n):
    while n > 0:
        print('T-minus: [{}], {}'.format(name, n))
        # await asyncio.sleep(1)
        await asyncio.sleep(1)
        n -= 1


def asyncio_demo():
    loop = asyncio.get_event_loop()
    tasks = [
        # asyncio.ensure_future(countdown("A", 2)),
        # asyncio.ensure_future(countdown("B", 3)),
        asyncio.ensure_future(countdown2("A", 2)),
        asyncio.ensure_future(countdown2("B", 3)),
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


if __name__ == '__main__':
    # send_demo()
    asyncio_demo()
