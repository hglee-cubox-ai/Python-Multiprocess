

from tqdm import tqdm
# from tqdm.contrib.concurrent import thread_map, process_map
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np

target_list = [1] * 10 + [2] * 15 + [3] * 25000000
    
def worker(p_id, num_list):
    result = 0
    if p_id == 0:
        num_list = tqdm(num_list)
    for num in num_list:
        result += num
    
    return result

if __name__ == '__main__':
    print('--- Single Process ---')
    result_1 = 0
    for num in tqdm(target_list):
        result_1 += num
    print(result_1)
    
    print('--- Multi Process ---')  
    num_process = 3
    pool = ProcessPoolExecutor(num_process)
    futures = []
    
    size_list = len(target_list)
    partition = size_list // num_process
    split_list = np.split(target_list, [partition * (idx + 1) for idx in range(num_process-1)])

    result_2 = 0
    for p_id in range(num_process):
        futures.append(pool.submit(worker, p_id, split_list[p_id]))
    for future in as_completed(futures):
        result_2 += future.result()
    
    print(result_2)