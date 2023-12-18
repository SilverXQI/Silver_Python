import random

import pandas as pd

# # 创建一个简单的 DataFrame
# data = {'Column1': [1, 2, 3, 4], 'Column2': ['A', 'B', 'C', 'D']}
# df = pd.DataFrame(data)
#
# # 将 DataFrame 输出到 xlsx 文件
# df.to_excel("output.xlsx", index=False)
import pandas as pd

# 读取 xlsx 文件到 DataFrame
df = pd.read_excel('Data.xlsx', sheet_name='Student')

# 打印 DataFrame 的内容
# print(len(df))
Sid = []
Cid = []
Tid = []
Grade = []
IsPassed = []
for i in range(len(df)):
    sid = df['Sid'][i]
    sdept = df['Sdept'][i]
    for i in range(17):
        Sid.append(sid)
        Cid.append(str(i + 1))
        Tid.append(str(i+6675))
        grade = random.randint(55, 100)
        Grade.append(grade)
        IsPassed.append(1 if grade >= 60 else 0)
    if sdept == 'CS_SE':
        Sid.append(sid)
        Cid.append('18')
        Tid.append('6692')
        grade = random.randint(55, 100)
        Grade.append(grade)
        IsPassed.append(1 if grade>=60 else 0)
    elif sdept == 'CS_AI':
        Sid.append(sid)
        Cid.append('19')
        Tid.append('6693')
        grade = random.randint(55, 100)
        Grade.append(grade)
        IsPassed.append(1 if grade >= 60 else 0)
    elif sdept == 'CS_ES':
        Sid.append(sid)
        Cid.append('20')
        Tid.append('6694')
        grade = random.randint(55, 100)
        Grade.append(grade)
        IsPassed.append(1 if grade >= 60 else 0)
    elif sdept == 'CS_NS':
        Sid.append(sid)
        Cid.append('21')
        Tid.append('6695')
        grade = random.randint(55, 100)
        Grade.append(grade)
        IsPassed.append(1 if grade >= 60 else 0)

data = {'Sid': Sid, 'Cid': Cid, 'Tid': Tid, 'Grade': Grade, 'IsPassed': IsPassed}
df = pd.DataFrame(data)
df.to_excel("SC.xlsx", index=False)