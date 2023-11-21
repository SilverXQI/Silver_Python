# from multiprocessing import Pool, Manager
#
#
# def func(my_list, my_dict):
#     my_list.append(10)
#     my_list.append(11)
#     my_dict['a'] = 1
#     my_dict['b'] = 2
#
#
# if __name__ == '__main__':
#     manager = Manager()
#     my_list = manager.list()
#     my_dict = manager.dict()
#
#     pool = Pool(processes=2)
#     for i in range(0, 2):
#         pool.apply_async(func, (my_list, my_dict))
#     pool.close()
#     pool.join()
#
#     print(my_list)
#     print(my_dict)

# from multiprocessing import Pool
# import time
# def func(i): #返回值只有进程池才有,父子进程没有返回值
#     time.sleep(0.5)
#     return i*i
#
# if __name__ == '__main__':
#     p = Pool(5)
#     ret = p.map(func,range(10))
#     print(ret)
# p = Pool()
# p.map(funcname,iterable) 默认异步的执行任务,且自带close,join功能
# p.apply(), 同步调用进程池的方法
# p.apply_async(),异步调用,和主进程完全异步,需要手动close和join
from multiprocessing import Pool
import time


def func(i):  # 返回值只有进程池才有,父子进程没有返回值
    time.sleep(0.5)
    return i * i


if __name__ == '__main__':
    p = Pool(5)
    res_l = []  # 从异步提交任务获取结果
    for i in range(10):
        # res = p.apply(func,args=(i,)) #apply的结果就是func的返回值,同步提交
        # print(res)

        res = p.apply_async(func, args=(i,))  # apply_sync的结果就是异步获取func的返回值
        res_l.append(res)  # 从异步提交任务获取结果
    for res in res_l:
        print(res.get())  # 等着func的计算结果
