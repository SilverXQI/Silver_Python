import re

layers = ["Conv2d", "MaxPool2d", "ReLU", "Linear", "AvgPool2d", "AdaptiveAvgPool2d", "BatchNorm2d"]


# 删除注释
def delete_annotation(line):
    if line.find("#") != -1:
        return line[:line.find("#")] + "\n"
    else:
        return line


def delete_none(line):
    if re.match("\s*\n", line):
        return ""
    else:
        return line


# 神经网络安全层转化
def torch_2_sec_torch(line):
    for layer in layers:
        if line.find(layer) != -1:
            layer_index = line.find(layer)
            if line[:layer_index].find("=") != -1:
                equal_index = line.find("=")
                newline = line[:equal_index + 1] + " layers.Sec" + layer + line[layer_index + len(layer):]
                return newline
    return line


"""
1.删除注释
"""


def as_initial_judge(line):
    # torch.nn 是否改名
    # torch.nn.functional 是否改名
    line = line.strip()
    torch_nn_as_flag = False
    torch_nn_functional_as_flag = False
    torch_nn_as_name = ""
    torch_nn_functional_as_name = ""
    if line.find("import") != -1:
        if line.find("torch.nn") != -1:
            if line.find("torch.nn.functional") != -1:
                if line.find("as") != -1:
                    torch_nn_functional_as_flag = True
                    torch_nn_functional_as_name = line[line.find("as") + 3:]
            else:
                if line.find("as") != -1:
                    torch_nn_as_flag = True
                    torch_nn_as_name = line[line.find("as") + 3:]

    return torch_nn_as_flag, torch_nn_functional_as_flag, torch_nn_as_name, torch_nn_functional_as_name


def as_name_change(line, as_name_relu):
    for as_name in as_name_relu:
        if line.find(as_name) != -1:
            line = line.replace(as_name, "layers.SecReLU")
    return line


def view2reshape(line):
    if line.find("view"):
        line = line.replace("view", "reshape")
    return line


def sec_format(filepath):
    model_file = open(filepath, "r", encoding="UTF-8")
    res = "from application.NN.layers import ModelLayer as layers\n"
    torch_nn_as_flag = False
    torch_nn_functional_as_flag = False
    as_name_relu = ["torch.nn.functional.relu"]
    for line in model_file:
        if line.find("import") != -1:
            temp_torch_nn_as_flag, temp_torch_nn_functional_as_flag, torch_nn_as_name, torch_nn_functional_as_name = as_initial_judge(
                line)
            if temp_torch_nn_as_flag:
                as_name_relu.append(f"{torch_nn_as_name}.functional.relu")
            if temp_torch_nn_functional_as_flag:
                as_name_relu.append(f"{torch_nn_functional_as_name}.relu")
            torch_nn_as_flag = temp_torch_nn_as_flag | torch_nn_as_flag
            torch_nn_functional_as_flag = temp_torch_nn_functional_as_flag | torch_nn_functional_as_flag
        else:
            line = as_name_change(line, as_name_relu)
            line = torch_2_sec_torch(line)
            line = view2reshape(line)
            line = delete_annotation(line)
            line = delete_none(line)
        res = res + line
    model_file.close()
    return res


if __name__ == '__main__':
    res_str = sec_format("Alexnet.py")

    print(res_str)
