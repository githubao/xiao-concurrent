#!/usr/bin/env python
# encoding: utf-8

"""
@description: 用threadpool实现并发

@author: baoqiang
@time: 2019-04-29 11:09
"""

import logging
from concurrent import futures

POOL_SIZE = 20

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class MultiRun:
    def __init__(self, tasks):
        self.tasks = tasks
        self.logger = logging.getLogger(self.__class__.__name__)

    def run_many(self):
        with futures.ThreadPoolExecutor(max_workers=POOL_SIZE) as executor:
            to_do = []
            for task in self.tasks:
                future = executor.submit(self.run_one, task)
                to_do.append(future)
                # msg = 'Scheduled for {}: {}'
                # print(msg.format(cc, future))

            results = []
            for future in futures.as_completed(to_do):
                res = future.result()
                msg = '{} result: {!r}'
                self.logger.info(msg.format(future, res))
                results.append(res)

        return results

    def run_one(self, dic):
        raise NotImplementedError

    def run_one_sample(self, dic):
        result = ''
        try:
            result = 'updated: {}'.format(dic['src'])
        except Exception as e:
            self.logger.error("err occur: {}".format(e))

        dic['result'] = result

        return dic


class MultiHello(MultiRun):
    def run_one(self, dic):
        return self.run_one_sample(dic)


def build_tasks():
    tasks = []

    for i in range(1000):
        dic = {
            'id': i,
            'src': 'req: {}'.format(i),
        }

        tasks.append(dic)

    return tasks


def hello_run():
    tasks = build_tasks()

    schedule = MultiHello(tasks)
    results = schedule.run_many()

    for dic in results:
        print(dic)


if __name__ == '__main__':
    hello_run()
