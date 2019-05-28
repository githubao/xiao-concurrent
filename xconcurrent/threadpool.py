#!/usr/bin/env python
# encoding: utf-8

"""
@description: 用threadpool实现并发

@author: baoqiang
@time: 2019-04-29 11:09
"""

import logging
from concurrent import futures
import threading
import traceback

POOL_SIZE = 500

# 加入重试机制
RETRY_TIMES = 3

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# 框架类
class MultiRun:
    def __init__(self, tasks):
        """
        导入方式：
        1. site-package目录，添加custom_path.pth文件，把路径加上
        2. 硬编码sys.path.append(path)
        """
        self.tasks = tasks
        self.logger = logging.getLogger(self.__class__.__name__)

    def run_many(self):
        with futures.ThreadPoolExecutor(max_workers=POOL_SIZE) as executor:
            to_do = []
            for task in self.tasks:
                future = executor.submit(self.safe_one, task)
                to_do.append(future)
                # msg = 'Scheduled for {}: {}'
                # print(msg.format(cc, future))

            results = []
            for future in futures.as_completed(to_do):
                res = future.result()
                msg = '{} result: {!r}'
                self.logger.info(msg.format(future, res))
                results.append(res)

                if len(results) % 100 == 0:
                    # if len(results) % 1 == 0:
                    self.logger.info("process cnt: {}/{}".format(len(results), len(self.tasks)))

                yield res

        # return results

    def safe_one(self, dic):
        for _ in range(RETRY_TIMES):
            try:
                return self.run_one(dic)
            except Exception as e:
                self.logger.exception("[{}] err occur: {}".format(dic, traceback.format_exc()))

        self.logger.error("faile to execute: {}".format(dic))

        return None

    def run_one(self, dic):
        raise NotImplementedError

    def run_one_sample(self, dic):
        result = 'updated: {}'.format(dic['id'])
        dic['res'] = result

        return dic


# 实现类，需要继承multirun，并重新run_one实现具体的耗时逻辑，把结果放在dic里面
class MultiHello(MultiRun):
    def run_one(self, dic):
        return self.run_one_sample(dic)


# 构建任务队列
def build_tasks():
    tasks = []

    for i in range(1000):
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
