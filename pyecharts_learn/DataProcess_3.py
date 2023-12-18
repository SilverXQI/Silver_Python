import subprocess
import pandas as pd
import numpy as np

# Java程序的绝对路径（假设Java类名为GeoCity）
java_class_path = "E:\\Computer_Programming\\Programing\\Java\\geo-city-master\\target\\classes\\cn\\learning\\ProcessCSV.class"
java_class_name = "ProcessCSV"


# 调用Java程序以获取省市区信息
def call_java_geocoder(lat, lon):
    try:
        # 注意：这里的命令部分可能需要根据您的具体环境进行调整
        result = subprocess.run(['java', '-cp', java_class_path, java_class_name, str(lat), str(lon)], check=True,
                                text=True, capture_output=True)
        output = result.stdout.strip()
        parts = output.split(', ')
        return parts[0], parts[1], parts[2] if parts[2] != 'null' else ''
    except subprocess.CalledProcessError as e:
        print("Error calling Java program:", e)
        return '', '', ''


# AQI计算函数
print(call_java_geocoder(42.74481320560531, 93.12168009045864))
