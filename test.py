# print("python is god")
#
# num = 12
# a = "12345"
# if num == 11 :
#     print("num=11")
# elif a == "12345":
#     print("a=12345")
# elif num == 12:
#     print("num=12")
# else:
#     print("else")
# ai = map(str, [5, 2, 3])  # 可迭代对象
# print(list(ai))
# print(list(ai))
# import subprocess
#
#
#
# def convert_ts_to_mp4(ts_file, mp4_file):
#     ffmpeg_command = ['ffmpeg', '-i', ts_file, '-acodec', 'copy', '-vcodec', 'copy', mp4_file]
#     subprocess.run(ffmpeg_command)
#
# # 示例用法
# convert_ts_to_mp4('G:\\Lenovo\\Download\\Video\\1.ts', 'output.mp4')
import os

path = "G:\\BaiduNetdiskDownload\\天国大魔境"
dir=os.listdir(path)
for i in dir:
    print(i)
    add_path = i+"p4"
    old_path = os.path.join(path, i)
    new_path = os.path.join(path, add_path)
    # print(os.path.join(path, new_path))
    print(new_path)
    os.rename(old_path, new_path)
    # print(os.path.isfile)
# print(dir)