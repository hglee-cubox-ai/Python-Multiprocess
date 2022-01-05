from multiprocessing import Pool, Value
from functools import partial
import time

from tqdm import tqdm
# from tqdm.contrib.concurrent import thread_map, process_map
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np


target_list = list(range(9))
    
def worker(x):
    print(x)
    time.sleep(1)


if __name__ == '__main__':
    num_process = 3
    
    print('--- Single Process ---')
    for num in target_list:
        print(num)
        time.sleep(1)

    print('--- Multi Process 2 ---')
    with Pool(num_process) as pool:
        for num in pool.imap_unordered(worker, target_list):
            pass
