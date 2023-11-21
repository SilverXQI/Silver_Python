from application.NN.layers import layer as layers
import torch
import torch.nn as nn
import torch.nn.functional as F
from application.NN.model.model_of_layers import ModelOfLayers
class AlexNet(nn.Module):
    def __init__(self):
        super(AlexNet, self).__init__()
        self.conv1 = layers.SecConv2d(1, 32, kernel_size=3, padding=1)  
        self.pool1 = layers.SecMaxPool2d(kernel_size=2, stride=2)  
        self.relu1 = layers.SecReLU()
        self.conv2 = layers.SecConv2d(32, 64, kernel_size=3, stride=1, padding=1)  
        self.pool2 = layers.SecMaxPool2d(kernel_size=2, stride=2)  
        self.relu2 = layers.SecReLU()
        self.conv3 = layers.SecConv2d(64, 128, kernel_size=3, stride=1, padding=1)  
        self.conv4 = layers.SecConv2d(128, 256, kernel_size=3, stride=1, padding=1)  
        self.conv5 = layers.SecConv2d(256, 256, kernel_size=3, stride=1, padding=1)  
        self.pool3 = layers.SecMaxPool2d(kernel_size=2, stride=2)  
        self.relu3 = layers.SecReLU()
        self.fc6 = layers.SecLinear(256 * 3 * 3, 1024)  
        self.fc7 = layers.SecLinear(1024, 512)  
        self.fc8 = layers.SecLinear(512, 10)  
    def forward(self, x):
        x = self.conv1(x)
        x = self.pool1(x)
        x = self.relu1(x)
        x = self.conv2(x)
        x = self.pool2(x)
        x = self.relu2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = self.conv5(x)
        x = self.pool3(x)
        x = self.relu3(x)
        x = x.reshape(-1, 256 * 3 * 3)  
        x = self.fc6(x)
        x = layers.SecReLU(x)
        x = self.fc7(x)
        x = layers.SecReLU(x)
        x = self.fc8(x)
        return x
def print_layer_info(module, input, output):
    print(f"Layer: {module}")
    print(f"Input shape: {str(input[0].shape)}")
    print(f"Output shape: {str(output[0].shape)}")
    print("=" * 50)
def register_hooks(model):
    for layer in model.children():
        layer.register_forward_hook(print_layer_info)
if __name__ == '__main__':
    input = torch.ones(1, 1, 28, 28)
    net = AlexNet()
    traced_model = torch.jit.trace(net, input)
    t = traced_model.graph
    net.load_state_dict(torch.load("application/NN/AlexNet/MNIST_bak.pkl"))
    k = ModelOfLayers()
    k.analyse_graph(net, input)
    print(k.layer_list)
    out = net(input)
    print(out)
