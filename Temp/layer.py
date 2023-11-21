import math

import torch
import torch.nn.functional as F
import crypto.primitives.arithmetic_secret_sharing.arithmetic_secret_sharing as ass
from config.base_configs import *
from crypto.primitives.arithmetic_secret_sharing.arithmetic_secret_sharing import ArithmeticSecretSharing
from crypto.tensor.RingTensor import RingTensor


class Layer(object):
    def __init__(self, input_name=None, output_name=None, name=None):
        self.input_name = input_name
        self.output_name = output_name
        self.name = name

    def get_name(self):
        return self.name

    def set_input_and_output(self, input_name, output_name):
        self.input_name = input_name
        self.output_name = output_name


class SecConv2d(Layer):

    def __init__(self, weight, stride=(1, 1), padding=(0, 0), bias=None, device=DEVICE, name="Conv2D"):
        """

        :param weight: 权重
        :param stride:步幅
        :param padding:填充
        :param bias:偏置单元（偏斜量）
        :param device:运行设备
        :param name:函数名
        """
        super(SecConv2d, self).__init__(name=name)
        # 判断输入数据是否是元组或列表，是则将第一个元素赋值给对应的属性
        # 此举是方便用户输入，可以输入一个元组或列表来定义该层的内核大小等参数
        # 也可以只输入一个数
        self.weight = weight
        self.kernel_shape = None
        if type(stride) in (tuple, list):
            self.stride = stride[0]
        else:
            self.stride = stride
        if type(padding) in (tuple, list):
            padding = padding[0]
        else:
            padding = padding
        self.padding = padding
        self.name = name
        self.input = None
        self.out_shape = None
        self.bias = bias
        self.device = device
        if self.device == "cuda":
            self.weight = self.weight.to(device)
            self.bias = self.bias.to(device)

    def get_out_shape(self, x: ArithmeticSecretSharing):
        n, img_c, img_h, img_w = x.shape
        kn, kc, kh, kw = self.kernel_shape
        out_h = math.ceil((img_h - self.kernel_shape[2] + 2 * self.padding) // self.stride) + 1
        out_w = math.ceil((img_w - self.kernel_shape[2] + 2 * self.padding) // self.stride) + 1

        return n, kn, out_h, out_w

    def forward(self, x: ArithmeticSecretSharing):
        # 首先得到最终输出的形状
        self.kernel_shape = self.weight.shape
        self.out_shape = self.get_out_shape(x)

        # 对输入进来的图像进行padding操作
        padding = self.padding
        x = x.pad((padding, padding, padding, padding), mode="constant", value=0)

        weight = ArithmeticSecretSharing(self.weight, x.party)
        kN, kC, ksize, _ = self.kernel_shape

        # 处理图片和卷积核的形状问题
        x = ass.img2col_for_conv(x, ksize, self.stride, self.device).transpose(1, 2)

        weight = weight.reshape((kN, kC * ksize * ksize))
        weight = weight.T()

        # 将图片和卷积核送入到函数中进行计算,最后的结果加上bias
        output = x @ weight

        bias = ArithmeticSecretSharing(self.bias, x.party)

        # 处理bias
        if bias is None:
            pass
        else:
            output = output + bias

        return output.transpose(1, 2).reshape(self.out_shape)

    def __call__(self, x: ArithmeticSecretSharing):
        # 复制一份，防止x可能被修改
        x_copy = ArithmeticSecretSharing(x.ring_tensor, x.party)
        return self.forward(x_copy)


class SecLinear(Layer):
    def __init__(self, weight, bias, name="SecLinear"):
        super(SecLinear, self).__init__(name=name)
        self.weight = weight
        self.bias = bias

    def forward(self, x: ArithmeticSecretSharing):
        weight = ArithmeticSecretSharing(self.weight, x.party)
        weight = weight.T()
        bias = ArithmeticSecretSharing(self.bias, x.party)
        x = x.reshape(x.shape[0])
        z = x @ weight + bias
        return z

    def __call__(self, *args, x: ArithmeticSecretSharing):
        x_copy = ArithmeticSecretSharing(x.ring_tensor, x.party)
        return self.forward(x_copy)


class SecReLu(Layer):
    def __init__(self, name="SecReLu"):
        super(SecReLu, self).__init__(name=name)

    def forward(self, x: ArithmeticSecretSharing):
        zero = torch.zeros(x.shape, dtype=torch.long)
        zero = RingTensor(zero, x.ring_tensor.dtype, x.ring_tensor.scale)
        zero = ArithmeticSecretSharing(zero, x.party)

        z = x > zero
        z = z * x
        return z

    def __call__(self, x: ArithmeticSecretSharing):
        x_copy = ArithmeticSecretSharing(x.ring_tensor, x.party)
        return self.forward(x_copy)


class SecMaxPool2D(Layer):
    def __init__(self, kernel_shape, stride, padding=(0, 0), device=DEVICE, name="SecMaxPool2D"):
        super(SecMaxPool2D, self).__init__(name=name)
        if type(kernel_shape) in (tuple, list):
            self.kernel_shape = kernel_shape[0]
        else:
            self.kernel_shape = kernel_shape
        if type(stride) in (tuple, list):
            self.stride = stride[0]
        else:
            self.stride = stride
        if type(padding) in (tuple, list):
            self.padding = padding[0]
        else:
            self.padding = padding
        self.device = device

    def get_out_shape(self, x: ArithmeticSecretSharing):
        n, img_c, img_h, img_w = x.shape
        out_h = math.ceil((img_h - self.kernel_shape + 2 * self.padding) // self.stride) + 1
        out_w = math.ceil((img_w - self.kernel_shape + 2 * self.padding) // self.stride) + 1

        return n, img_c, out_h, out_w

    def sec_max(self, z, party, dtype, scale):
        def max_(z):
            if z.shape[1] == 1:
                return z
            if z.shape[1] % 2 == 1:
                z_ = z[:, -1:, :]
                z = torch.cat((z, z_), dim=1)
            z0 = ArithmeticSecretSharing(RingTensor(z[:, 0::2, :], dtype, scale), party)
            z1 = ArithmeticSecretSharing(RingTensor(z[:, 1::2, :], dtype, scale), party)
            z0.to(self.device)
            z1.to(self.device)

            b0 = z0 >= z1
            # b1 = z1 > z0
            b1 = (b0 - RingTensor(torch.ones(b0.shape, dtype=torch.int64, device=b0.device) * scale, dtype,
                                  scale)) * -1

            b0 = b0 * z0
            b1 = b1 * z1

            return (b0.ring_tensor.tensor + b1.ring_tensor.tensor) % RING_MAX

        if z.shape[1] == 1:
            return z
        else:
            z = max_(z)
        return self.sec_max(z, party, dtype, scale)

    def forward(self, x: ArithmeticSecretSharing):
        N, C, W, H = x.shape
        k_size = self.kernel_shape
        out_shape = self.get_out_shape(x)

        # 对输入进来的图像进行padding操作
        padding = self.padding

        x = x.pad((padding, padding, padding, padding), mode="constant", value=0)

        x = ass.img2col_for_conv(x, k_size, self.stride, self.device)
        xs = []

        for i in range(0, C):
            xs.append(self.sec_max(x.ring_tensor.tensor[:, i * k_size * k_size:(i + 1) * k_size * k_size, :], x.party,
                                   x.ring_tensor.dtype, x.ring_tensor.scale))
        xs = torch.cat(xs, dim=1).reshape(out_shape).to(self.device)

        return ArithmeticSecretSharing(RingTensor(xs, x.ring_tensor.dtype, x.ring_tensor.scale), x.party)

    def __call__(self, x: ArithmeticSecretSharing):
        x_copy = ArithmeticSecretSharing(x.ring_tensor, x.party)
        x_copy = x_copy.to(DEVICE)
        return self.forward(x_copy)


class SecReshape(Layer):
    def __init__(self, name="SecReshape"):
        super(SecReshape, self).__init__(name=name)

    def __call__(self, x: ArithmeticSecretSharing, shape):
        return x.reshape(tuple(shape.ring_tensor.tensor.tolist()))


class SecGemm(Layer):
    def __init__(self, weight, bias, device=DEVICE, name="SecGemm"):
        super(SecGemm, self).__init__(name=name)
        self.device = device
        self.weight = weight.T()
        self.bias = bias

    def forward(self, x):
        weight = ArithmeticSecretSharing(self.weight, x.party)
        bias = ArithmeticSecretSharing(self.bias, x.party)
        z = (x @ weight) + bias
        return z

    def __call__(self, x: ArithmeticSecretSharing):
        return self.forward(x)


class SecAvgPool2D(Layer):
    def __init__(self, kernel_shape, stride, padding=(0, 0), device=DEVICE, name="SecAvgPool2D"):
        super(SecAvgPool2D, self).__init__(name=name)
        if type(kernel_shape) in (tuple, list):
            self.kernel_shape = kernel_shape[0]
        else:
            self.kernel_shape = kernel_shape
        if type(stride) in (tuple, list):
            stride = stride[0]
        else:
            stride = stride
        self.stride = stride
        if type(padding) in (tuple, list):
            padding = padding[0]
        else:
            padding = padding
        self.padding = padding
        self.device = device

    def get_out_shape(self, x: ArithmeticSecretSharing):
        n, img_c, img_h, img_w = x.shape
        out_h = math.ceil((img_h - self.kernel_shape + 2 * self.padding) // self.stride) + 1
        out_w = math.ceil((img_w - self.kernel_shape + 2 * self.padding) // self.stride) + 1
        return n, img_c, out_h, out_w

    def forward(self, x: ArithmeticSecretSharing):
        # 对图像进行padding处理
        padding = self.padding
        x = x.pad((padding, padding, padding, padding), mode="constant", value=0)

        k_size = self.kernel_shape
        out_shape = self.get_out_shape(x)

        x = ass.img2col_for_pool(x, k_size, self.stride, self.device).transpose(2, 3)

        # 平均池化相当于用一个权重为1/n的权重做一次卷积
        # TODO: 只支持两方，后续weight的产生，分发需要修改
        if x.party.party_id == 0:
            weight = ArithmeticSecretSharing(
                RingTensor.convert_to_ring(torch.ones(x.shape[3], 1) / (k_size * k_size)), x.party)
        else:
            weight = ArithmeticSecretSharing(
                RingTensor.convert_to_ring(torch.zeros(x.shape[3], 1)), x.party)

        res = x @ weight

        return res.reshape(out_shape)

    def __call__(self, x: ArithmeticSecretSharing):
        x_copy = ArithmeticSecretSharing(x.ring_tensor, x.party)
        x_copy = x_copy.to(DEVICE)
        return self.forward(x_copy)


class SecPad(Layer):
    def __init__(self, mode, value=0, name="SecPad"):
        super(SecPad, self).__init__(name=name)
        self.mode = mode
        self.value = value

    def forward(self, x, pad):
        return x.pad(pad.ring_tensor.tensor.tolist(), self.mode, self.value)

    def __call__(self, x: ArithmeticSecretSharing, pad):
        return self.forward(x, pad)


class SecMatMul(Layer):
    def __init__(self, name="SecMatMul"):
        super(SecMatMul, self).__init__(name=name)

    def __call__(self, x: ArithmeticSecretSharing, y: ArithmeticSecretSharing):
        z = x + y
        return z


class SecADD(Layer):
    def __init__(self, name="SecADD"):
        super(SecADD, self).__init__(name=name)

    def __call__(self, x: ArithmeticSecretSharing, y: ArithmeticSecretSharing):
        z = x + y
        return z


class SecTranspose(Layer):
    # TODO:这里weight权重变量在哪里定义的？
    def __init__(self, weight: ArithmeticSecretSharing, name="SecTranspose"):
        super(SecTranspose, self).__init__(name=name)
        self.weight = weight

    def __call__(self):
        y = self.weight.ring_tensor.T
        return ArithmeticSecretSharing(y, self.weight.party, self.weight.device)


class SecUnsqueeze(Layer):
    def __init__(self, dim, name="SecUnsqueeze"):
        super(SecUnsqueeze, self).__init__(name=name)
        self.dim = dim

    def forward(self, x):
        y = torch.unsqueeze(x.ring_tensor, self.dim.ring.item())
        return ArithmeticSecretSharing(RingTensor(y), x.party, x.device)

    def __call__(self, x: ArithmeticSecretSharing):
        return self.forward(x)


class SecConcat(Layer):
    def __init__(self, axis, name="SecConcat"):
        super(SecConcat, self).__init__(name=name)
        self.axis = axis

    def forward(self, x, y):
        z = torch.cat((x.ring_tensor, y.ring_tensor), dim=self.axis)
        return ArithmeticSecretSharing(z, x.party, x.device)

    def __call__(self, x: ArithmeticSecretSharing, y: ArithmeticSecretSharing):
        return self.forward(x, y)


class SecCopy(Layer):
    def __init__(self, name="SecCopy"):
        super().__init__(name=name)

    def forward(self, x):
        y = ArithmeticSecretSharing(x.ring_tensor, x.party, x.device)
        return y

    def __call__(self, x: ArithmeticSecretSharing):
        return self.forward(x)


class SecBN2d(Layer):
    def __init__(self, gamma, beta, running_mean: ArithmeticSecretSharing, running_var, epsilon, name="SecBN2d"):
        super().__init__(name=name)
        self.gamma = gamma
        self.beta = beta
        self.running_mean = running_mean
        self.running_var = running_var
        self.epsilon = epsilon

    def forward(self,
                x: ArithmeticSecretSharing):  # # Y = (X - running_mean) / sqrt(running_var + eps) * gamma + beta # #

        self.running_mean.ring_tensor = self.running_mean.ring_tensor.unsqueeze(1)
        self.running_mean.ring_tensor = self.running_mean.ring_tensor.unsqueeze(2)
        self.running_mean.ring_tensor = self.running_mean.ring_tensor.repeat(1, x.ring_tensor.shape[2], x.ring_tensor.shape[3])

        self.running_var = self.running_var.unsqueeze(1)
        self.running_var = self.running_var.unsqueeze(2)
        # TODO: 这里的debug没转移过来，注释了
        # ArithmeticSecretSharing.debug(x)

        x = x - self.running_mean

        divide = torch.floor(self.running_var + self.epsilon).long()
        print(divide)
        print(x.ring_tensor)
        # x.value = torch.floor(x.value / (self.running_var + self.epsilon))
        x.ring_tensor = torch.floor(torch.true_divide(x.ring_tensor, divide).long())
        print(x.ring_tensor)
        # ArithmeticSecretSharing.debug(x)

        self.gamma.ring_tensor = self.gamma.ring_tensor.unsqueeze(1)
        self.gamma.ring_tensor = self.gamma.ring_tensor.unsqueeze(2)

        self.beta.ring_tensor = self.beta.ring_tensor.unsqueeze(1)
        self.beta.ring_tensor = self.beta.ring_tensor.unsqueeze(2)

        x = x * self.gamma
        x = x + self.beta

        return x

    def __call__(self, x: ArithmeticSecretSharing):
        x_ = ArithmeticSecretSharing(x.ring_tensor, x.party, x.device)
        return self.forward(x_)
