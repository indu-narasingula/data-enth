# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 18:32:26 2022

@author: johan
"""

#import os
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from loader.dataset import Dataset

#os.environ['TZ'] = 'Europe/Amsterdam'

data_obj = Dataset()
data_obj.update()


def get_data():
    data_obj.update()
    return


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename="./logs/main.log",
                        format='%(asctime)s:%(levelname)s:%(message)s')
    # logging.basicConfig(level=logging.INFO, filename="./main.log",
    #                    format='%(asctime)s:%(levelname)s:%(message)s')
    scheduler = BlockingScheduler(timezone='Europe/Amsterdam')
    scheduler.add_job(get_data, 'cron', minute='00',
                      hour='04', day='*', year='*', month='*')
    scheduler.add_job(get_data, 'cron', minute='00',
                      hour='16', day='*', year='*', month='*')
    scheduler.start()
