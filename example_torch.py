import sys


from tqdm import tqdm
# from tqdm.contrib.concurrent import thread_map, process_map
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
import torch
import torch.nn as nn


def worker(p_id, tensor_list):
    device = torch.device(f'cuda:{p_id}')
    torch.cuda.set_device(device)
    
    net = nn.Linear(5, 1)
    
    result = 0
    
    if p_id == 0:
        tensor_list = tqdm(tensor_list)
        
    for input_tensor in tensor_list:
        output_tensor = net(input_tensor)
        result += 1
        
    return result


if __name__ == '__main__':
    torch.multiprocessing.set_start_method('spawn') # Need for Using Cuda in Multiprocessing
    batch = 4
    input_tensors = [torch.ones(batch, 5)] * 1000000
    
    print('--- Single Process ---')
    device = torch.device('cuda:0')
    torch.cuda.set_device(device)
    
    net = nn.Linear(5, 1)
    result_1 = []
    for input_tensor in tqdm(input_tensors):
        output_tensor = net(input_tensor)
        result_1.append(output_tensor.shape)
    
    print(len(result_1))
        
    print('--- Multi Process ---')  
    num_process = 2
    pool = ProcessPoolExecutor(num_process)
    futures = []
    
    if num_process > torch.cuda.device_count():
        print('Not Enough GPUs..')
        sys.exit()
    if num_process < 2:
        print("It's not MultiProcessing")
        sys.exit()
    
    size_list = len(input_tensors)
    partition = size_list // num_process
    split_list = np.split(input_tensors, [partition * (idx + 1) for idx in range(num_process-1)])
    
    result_2 = 0
    for p_id in range(num_process):
        futures.append(pool.submit(worker, p_id, split_list[p_id]))
    for future in as_completed(futures):
        result_2 += future.result()
    
    print(result_2)