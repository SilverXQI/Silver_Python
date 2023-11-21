
"""
本文件定义了安全两方计算情况下分布式比较函数的函数秘密共享
在进行分布式比较函数密钥产生和求值的过程中包含了分布式点函数的相关过程
本文件中的方法定义参考E. Boyle e.t.c. Function Secret Sharing for Mixed-Mode and Fixed-Point Secure Computation.2021
https://link.springer.com/chapter/10.1007/978-3-030-77886-6_30
"""
import threading
# from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Process
from multiprocessing import Pool
import torch
from common.random.PRG import PRG
import random
import time
from config.base_configs import BIT_LEN, LMD, DEVICE, PRG_TYPE
from crypto.tensor.RingTensor import RingTensor
from multiprocessing.pool import Pool


class DPF(object):
    @staticmethod
    def gen(num_of_keys, alpha, b):
        """
        分布式比较函数密钥生成接口
        通过该接口实现多个密钥生成
        分布式比较函数：
            f(x)=b, if x < α; f(x)=0, else

        :param num_of_keys: 需要的密钥个数
        :param alpha: 分布式比较函数的参数α
        :param b: 分布式比较函数参数b
        :return: 各个参与方（两方）的密钥
        """
        key0 = []
        key1 = []
        for t in range(num_of_keys):
            key = dpf_gen(alpha, b)
            k0, k1 = key
            key0.append(k0)
            key1.append(k1)
        return key0, key1
    @staticmethod
    def mutil_thread_gen(num_of_keys, alpha, b):
        """
        分布式比较函数密钥生成接口
        通过该接口实现多个密钥生成
        分布式比较函数：
            f(x)=b, if x < α; f(x)=0, else

        :param num_of_keys: 需要的密钥个数
        :param alpha: 分布式比较函数的参数α
        :param b: 分布式比较函数参数b
        :return: 各个参与方（两方）的密钥
        """
        key0 = []
        key1 = []

        p = Pool(8)
        for i in range(num_of_keys):
            res = p.apply_async(dpf_gen, args=(alpha, target))
            res_l.append(res)
        for res in res_l:
            res_key = res.get()
            key0.append(res_key[0].to_dic())
            key1.append(res_key[1].to_dic())
        return key0, key1

    @staticmethod
    def eval(x, keys, party_id, prg_type=PRG_TYPE):
        return dpf_eval(x, keys, party_id, prg_type)


def multi_thread_temp_gen(alpha, b):
    key = dpf_gen(alpha, b)
    k0, k1 = key
    return k0, k1


class DPFKey(object):
    """
    分布式比较函数的秘密分享密钥

    属性:
        s: DPF产生的树根节点的参数，λ位01串
        cw_list: 校验字列表
        ex_cw_dpf: 额外校验字用于dpf求值
    """

    def __init__(self):
        self.s = None
        self.cw_list = []
        self.ex_cw = None

    def to_dic(self):
        """
        将DPFKey类对象转换为字典
        :return: 表示类对象的字典
        """
        dict = {}
        dict['s'] = self.s
        dict['ex_cw_dpf'] = self.ex_cw
        for i in range(BIT_LEN):
            dict['s_cw_' + str(i)] = self.cw_list[i].s_cw
            dict['t_cw_l_' + str(i)] = self.cw_list[i].t_cw_l
            dict['t_cw_r_' + str(i)] = self.cw_list[i].t_cw_r

        return dict

    @staticmethod
    def dic_to_key(dic):
        """
        将字典转换为类对象
        :param dic: 字典对象
        :return: DCFKey对象
        """
        key = DPFKey()
        key.s = dic['s']
        key.ex_cw = dic['ex_cw_dpf']
        for i in range(BIT_LEN):
            s_cw = dic['s_cw_' + str(i)]
            t_cw_l = dic['t_cw_l_' + str(i)]
            t_cw_r = dic['t_cw_r_' + str(i)]
            cw = DPFCW(s_cw=s_cw, t_cw_l=t_cw_l, t_cw_r=t_cw_r, lmd=LMD)
            key.cw_list.append(cw)

        return key


class DPFCW(object):
    """
    校验字(Correction Words, CW)

    属性:
        lmd: 安全参数
        s_cw: 参数s的校验字
        t_cw_l: 左孩子节点参数t的校验字
        t_cw_r: 右孩子节点参数t的校验字
    """

    def __init__(self, s_cw, t_cw_l, t_cw_r, lmd):
        self.lmd = lmd
        self.s_cw = s_cw
        self.t_cw_l = t_cw_l
        self.t_cw_r = t_cw_r


def dpf_gen(alpha: RingTensor, b):
    """
    通过伪随机数生成器产生各参与方的dpf密钥

    :param alpha: 分布式点函数的参数α
    :param b: 分布式比较函数的参数b
    :return: 各参与方的密钥
    """

    # 产生伪随机数产生器的种子
    seed_0 = torch.tensor([random.randint(0, 1000)], device=DEVICE)
    seed_1 = torch.tensor([random.randint(0, 1000)], device=DEVICE)

    prg = PRG(PRG_TYPE, device=DEVICE)
    prg.set_seeds(seed_0)
    s_0_0 = prg.gen_N_nit_random_number(LMD)[0]
    prg.set_seeds(seed_1)
    s_0_1 = prg.gen_N_nit_random_number(LMD)[0]
    k0 = DPFKey()
    k1 = DPFKey()

    k0.s = s_0_0
    k1.s = s_0_1

    t0 = torch.tensor(0, device=DEVICE)
    t1 = torch.tensor(1, device=DEVICE)

    s_last_0 = s_0_0
    s_last_1 = s_0_1

    t_last_0 = t0
    t_last_1 = t1

    for i in range(alpha.bit_len):
        s_l_0, _, t_l_0, s_r_0, _, t_r_0 = prg.gen_DCF_keys(s_last_0[0], LMD)
        s_l_1, _, t_l_1, s_r_1, _, t_r_1 = prg.gen_DCF_keys(s_last_1[0], LMD)

        s_l_0, t_l_0, s_l_1, t_l_1 = s_l_0[0], t_l_0[0].squeeze(), s_l_1[0], t_l_1[0].squeeze()
        s_r_0, t_r_0, s_r_1, t_r_1 = s_r_0[0], t_r_0[0].squeeze(), s_r_1[0], t_r_1[0].squeeze()

        if alpha.get_bit(alpha.bit_len - 1 - i) == 0:
            s_keep_0, t_keep_0, s_keep_1, t_keep_1 = s_l_0, t_l_0, s_l_1, t_l_1
            s_lose_0, t_lose_0, s_lose_1, t_lose_1 = s_r_0, t_r_0, s_r_1, t_r_1

        else:
            s_keep_0, t_keep_0, s_keep_1, t_keep_1 = s_r_0, t_r_0, s_r_1, t_r_1
            s_lose_0, t_lose_0, s_lose_1, t_lose_1 = s_l_0, t_l_0, s_l_1, t_l_1

        s_cw = s_lose_0 ^ s_lose_1

        t_l_cw = t_l_0 ^ t_l_1 ^ alpha.get_bit(alpha.bit_len - 1 - i) ^ 1
        t_r_cw = t_r_0 ^ t_r_1 ^ alpha.get_bit(alpha.bit_len - 1 - i)

        cw = DPFCW(s_cw=s_cw, t_cw_l=t_l_cw, t_cw_r=t_r_cw, lmd=LMD)

        k0.cw_list.append(cw)
        k1.cw_list.append(cw)

        if alpha.get_bit(alpha.bit_len - 1 - i) == 0:
            t_keep_cw = t_l_cw

        else:
            t_keep_cw = t_r_cw

        s_last_0 = s_keep_0 ^ t_last_0 * s_cw
        s_last_1 = s_keep_1 ^ t_last_1 * s_cw

        t_last_0 = t_keep_0 ^ t_last_0 * t_keep_cw
        t_last_1 = t_keep_1 ^ t_last_1 * t_keep_cw

    k0.ex_cw = pow(-1, t_last_1) * (b.tensor - convert(s_last_0, BIT_LEN)[0] + convert(s_last_1, BIT_LEN)[0])
    k1.ex_cw = pow(-1, t_last_1) * (b.tensor - convert(s_last_0, BIT_LEN)[0] + convert(s_last_1, BIT_LEN)[0])

    return k0, k1


def dpf_eval(x: RingTensor, keys: DPFKey, party_id, prg_type):
    """
    分布式点函数EVAL过程
    根据输入x，参与方在本地计算函数值，即原函数f(x)的分享值

    :param x: 输入变量值x
    :param keys: 参与方关于函数分享的密钥
    :param party_id: 参与方编号
    :param prg_type: 伪随机数产生器的类型
    :return: 分布式点函数的结果
    """
    # flatten the input tensor and reshape it back after computation
    shape = x.tensor.shape
    x.tensor = x.tensor.flatten()

    level_seed = keys.s

    prg = PRG(prg_type, DEVICE)

    t_last = torch.tensor([party_id], device=DEVICE).unsqueeze(0).repeat_interleave(len(x.tensor), dim=0)
    s_last = level_seed
    key_time = 0

    for i in range(x.bit_len):
        cw = keys.cw_list[i]

        s_cw = cw.s_cw
        t_cw_l = cw.t_cw_l
        t_cw_r = cw.t_cw_r

        s_l, _, t_l, s_r, _, t_r = prg.gen_DCF_keys(s_last[:, 0], LMD)

        s1_l = s_l ^ (s_cw * t_last)
        t1_l = t_l ^ (t_cw_l * t_last)
        s1_r = s_r ^ (s_cw * t_last)
        t1_r = t_r ^ (t_cw_r * t_last)

        x_shift_bit = x.get_bit(x.bit_len - 1 - i).unsqueeze(1)

        s_last = s1_r * x_shift_bit + s1_l * (1 - x_shift_bit)
        t_last = t1_r * x_shift_bit + t1_l * (1 - x_shift_bit)

    dpf_result = pow(-1, party_id) * (convert_tensor(s_last, BIT_LEN).unsqueeze(1) + t_last * keys.ex_cw)
    dpf_result = dpf_result.squeeze().view(shape)

    return dpf_result


def convert(num, k):
    res = num % (2 ** k)
    return res


def convert_tensor(tensor, k):
    res = tensor[:, 0] % (2 ** k)
    return res


def printt(i: int, j):
    print(i)


def test():
    pass


if __name__ == '__main__':
    alpha = RingTensor.convert_to_ring(torch.tensor(5))
    target = RingTensor.convert_to_ring(torch.tensor(1))
    start = time.time()
    result0,result1 = DPF.gen(500, alpha, target)
    # for i in range(10):
    #     print(result0[i].to_dic())
    # print(result0,result1)
    end = time.time()
    print(f"time{end - start}")
    # start = time.time()
    # result0, result1 = DPF.mutil_thread_gen(10, alpha, target)
    # print(result0)
    # # for i in range(100):
    # #     print(result0[i].to_dic())
    # end = time.time()
    # print(f"time{end - start}")
    # print(dpf_gen(alpha, target))
    key0 = []
    key1 = []

    # nums = []
    # for i in range(10):
    #     nums.append((alpha, target))
    # print([alpha, target])
    # with ProcessPoolExecutor() as pool:
    #     ret = pool.map(dpf_gen, [(alpha, target), (alpha, target)])

    # print(ret)
    # for i in ret:
    #     key0.append(i[0])
    #     key1.append(i[1])
    # print(key0)
    start= time.time()
    res_l=[]
    p = Pool(8)
    for i in range(500):
        res = p.apply_async(dpf_gen, args=(alpha, target))
        res_l.append(res)
    for res in res_l:
        res_key= res.get()
        key0.append(res_key[0].to_dic())
        key1.append(res_key[1].to_dic())
    # print(key0)
    # print(key1)
    end = time.time()
    print(f"time{end - start}")