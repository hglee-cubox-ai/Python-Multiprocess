

from tqdm import tqdm
# from tqdm.contrib.concurrent import thread_map, process_map
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np

str_list_to_print = ['a'] * 10 + ['b'] * 15 + ['c'] * 25000000
    
def worker(p_id, data):
    print(p_id, ' - ', data)
    return data

if __name__ == '__main__':
    print('Single Process')
    result_1 = []
    for str in tqdm(str_list_to_print):
        result_1.append(str)
    print(len(result_1))
    
    print('Multi Process')  
    num_process = 3
    pool = ProcessPoolExecutor(num_process)
    futures = []
    
    size_list = len(str_list_to_print)
    partition = size_list // num_process
    split_list = np.split(str_list_to_print, [partition * (idx + 1) for idx in range(num_process-1)])

    result_2_size = 0
    for p_id in range(num_process):
        futures.append(pool.submit(worker, p_id, split_list[p_id]))
    for future in as_completed(futures):
        result_2_size += len(future.result())
    
    print(result_2_size)