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
        result = subprocess.run(['java', '-cp', java_class_path, java_class_name, str(lat), str(lon)], check=True, text=True, capture_output=True)
        output = result.stdout.strip()
        parts = output.split(', ')
        return parts[0], parts[1], parts[2] if parts[2] != 'null' else ''
    except subprocess.CalledProcessError as e:
        print("Error calling Java program:", e)
        return '', '', ''

# AQI计算函数
def calculate_aqi(row):
    qua = [0, 50, 100, 150, 200, 300, 400, 500]
    Idata = [
        [0, 35, 75, 115, 150, 250, 350, 500],  # PM2.5 24小时平均
        [0, 50, 150, 250, 350, 420, 500, 600],  # PM10 24小时平均
        [0, 150, 500, 650, 800],  # SO2
        [0, 100, 200, 700, 1200, 2340, 3090, 3840],  # NO2
        [0, 5, 10, 35, 60, 90, 120, 150],  # CO
        [0, 160, 200, 300, 400, 800, 1000, 1200]  # O3
    ]
    T_IA = 0
    pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    for i, pollutant in enumerate(pollutants):
        concentration = row[pollutant]
        for k in range(1, len(Idata[i])):
            if Idata[i][k] > concentration:
                break
        if k == (len(Idata[i]) - 1) and Idata[i][k] < concentration:
            T_IA = Idata[i][k]
        else:
            T_IA = int(round((((qua[k] - qua[k-1]) / (Idata[i][k] - Idata[i][k-1])) * (concentration - Idata[i][k-1]) + qua[k-1]) + 0.5))
        if T_IA > row['AQI']:
            row['AQI'] = T_IA
    return row['AQI']

# 读取CSV文件
csv_file_path = 'CN-Reanalysis2013010100.csv'
df = pd.read_csv(csv_file_path)

# 初始化AQI列
df['AQI'] = 0

# 计算AQI值
df['AQI'] = df.apply(calculate_aqi, axis=1)

# 应用Java地理编码器
df[['Province', 'City', 'District']] = df.apply(lambda row: call_java_geocoder(row['lat'], row['lon']), axis=1, result_type='expand')

# 计算每个省市区的AQI平均值
aqi_avg = df.groupby(['Province', 'City', 'District'])['AQI'].mean().reset_index()

# 保存结果到CSV文件
output_file_path = 'aqi_average2.csv'
aqi_avg.to_csv(output_file_path, index=False)
