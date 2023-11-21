# AlexNet是深度学习中的一个经典卷积神经网络（CNN）模型，由Alex Krizhevsky、Geoffrey Hinton和Ilya Sutskever等人在2012年的ImageNet图像识别挑战中提出。该模型的设计标志着深度学习在计算机视觉领域的突破，并引发了深度学习在图像识别任务上的广泛应用。
#
# AlexNet是一个包含8个卷积层和3个全连接层的深层神经网络。它的结构相对简单，但在当时来说是非常大规模和先进的模型。它的主要特点包括：
#
# 1. 多层卷积层：AlexNet使用了5层卷积层来提取图像特征，这些卷积层通过卷积、ReLU激活函数和池化操作逐步提取和减小图像特征的尺寸。
#
# 2. 多GPU训练：为了处理大规模的图像数据，AlexNet采用了使用两个GPU进行训练的方法，这在当时是非常先进的技术。
#
# 3. Dropout正则化：AlexNet使用了Dropout技术，以减少过拟合，提高模型的泛化能力。
#
# 4. ReLU激活函数：在AlexNet中，使用ReLU（Rectified Linear Unit）作为激活函数，这一改进使得网络在训练过程中更容易收敛，并且可以避免梯度消失问题。
#
# AlexNet的设计和成功证明了深度学习在图像识别任务上的优势，也为后来更复杂的神经网络模型奠定了基础。随着时间的推移，更多更复杂的深度学习模型出现，但AlexNet仍然被认为是深度学习历史上的重要里程碑。

import torch
import torch.nn as nn
import torch.nn.functional as F

from application.NN.model.model_of_layers import ModelOfLayers


# 定义网络结构
class AlexNet(nn.Module):
    def __init__(self):
        super(AlexNet, self).__init__()

        # 由于MNIST为28x28， 而最初AlexNet的输入图片是227x227的。所以网络层数和参数需要调节
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)  # AlexCONV1(3,96, k=11,s=4,p=0)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)  # AlexPool1(k=3, s=2)
        self.relu1 = nn.ReLU()

        # self.conv2 = nn.Conv2d(96, 256, kernel_size=5,stride=1,padding=2)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)  # AlexCONV2(96, 256,k=5,s=1,p=2)
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)  # AlexPool2(k=3,s=2)
        self.relu2 = nn.ReLU()

        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1)  # AlexCONV3(256,384,k=3,s=1,p=1)
        # self.conv4 = nn.Conv2d(384, 384, kernel_size=3, stride=1, padding=1)
        self.conv4 = nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1)  # AlexCONV4(384, 384, k=3,s=1,p=1)
        self.conv5 = nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1)  # AlexCONV5(384, 256, k=3, s=1,p=1)
        self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2)  # AlexPool3(k=3,s=2)
        self.relu3 = nn.ReLU()

        self.fc6 = nn.Linear(256 * 3 * 3, 1024)  # AlexFC6(256*6*6, 4096)
        self.fc7 = nn.Linear(1024, 512)  # AlexFC6(4096,4096)
        self.fc8 = nn.Linear(512, 10)  # AlexFC6(4096,1000)

    def forward(self, x):
        x = self.conv1(x)
        # print(x)
        x = self.pool1(x)
        # print(x)
        x = self.relu1(x)
        # print(x)
        x = self.conv2(x)
        # print(x)
        x = self.pool2(x)
        # print(x)
        x = self.relu2(x)
        # print(x)
        x = self.conv3(x)
        # print(x)
        x = self.conv4(x)
        # print(x)
        x = self.conv5(x)
        # print(x)
        x = self.pool3(x)
        # print(x)
        x = self.relu3(x)
        # print(x)
        x = x.view(-1, 256 * 3 * 3)  # Alex: x = x.view(-1, 256*6*6) #reshape
        x = self.fc6(x)
        # print(x)
        x = F.relu(x)
        # x = SecReLU(x)
        # print(x)
        x = self.fc7(x)
        # print(x)
        x = F.relu(x)
        # print(x)
        x = self.fc8(x)
        return x


def print_layer_info(module, input, output):
    print(f"Layer: {module}")
    print(f"Input shape: {str(input[0].shape)}")
    print(f"Output shape: {str(output[0].shape)}")
    print("=" * 50)


# 为模型的每一层注册钩子
def register_hooks(model):
    for layer in model.children():
        layer.register_forward_hook(print_layer_info)


if __name__ == '__main__':
    input = torch.ones(1, 1, 28, 28)
    net = AlexNet()

    # register_hooks(net)
    # 跟踪模型
    traced_model = torch.jit.trace(net, input)
    t = traced_model.graph
    # print(traced_model.graph)

    # for node in traced_model.graph.nodes():
    #     print(node.kind())
    # print(spilt_str(traced_model.graph.nodes()))
    # print(inspect.get(net))
    net.load_state_dict(torch.load("application/NN/AlexNet/MNIST_bak.pkl"))

    k = ModelOfLayers()
    k.analyse_graph(net, input)
    print(k.layer_list)
    # print(net.state_dict())
    # for i in k.layer_list:
    #     print(i)

    # print(analyse_graph(net, input))

    # for key, module in net._modules.items():
    #     print(type(key))

    out = net(input)
    print(out)
