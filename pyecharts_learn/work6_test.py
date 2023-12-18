import os
import pandas as pd
import numpy as np

# AQI计算函数
def calculate_aqi(data):
    qua = [0, 50, 100, 150, 200, 300, 400, 500]
    # 根据您的数据文件调整这里的列名
    data_array = data[['PM2.5(微克每立方米)', 'PM10(微克每立方米)', 'SO2(微克每立方米)', 'NO2(微克每立方米)', 'CO(毫克每立方米)', 'O3(微克每立方米)']].to_numpy()

    Idata = [
        [0, 35, 75, 115, 150, 250, 350, 500],
        [0, 50, 150, 250, 350, 420, 500, 600],
        [0,150,500,650,800],
        [0,100,200,700,1200,2340,3090,3840],
        [0,5,10,35,60,90,120,150],
        [0,160,200,300,400,800,1000,1200]
    ]

    IAQI = np.zeros(len(data))
    for i in range(len(Idata)):
        T_data = data_array[:, i]
        T_Idata = Idata[i]
        for j in range(len(T_data)):
            T_IA = 0
            for k in range(1, len(T_Idata)):
                if T_Idata[k] > T_data[j]:
                    break
            if k == (len(T_Idata) - 1) and T_Idata[k] < T_data[j]:
                T_IA = T_Idata[k]
            else:
                T_IA = int(round((((qua[k] - qua[k - 1]) / (T_Idata[k] - T_Idata[k - 1])) * (T_data[j] - T_Idata[k - 1]) + qua[k - 1]) + 0.5))
            if T_IA > IAQI[j]:
                IAQI[j] = T_IA
    return IAQI

# 处理单个文件的函数
def process_aqi_data(file_path):
    data = pd.read_csv(file_path)

    # 清除列名前后的空格
    data.columns = data.columns.str.strip()

    # 过滤掉省份为空的记录
    data = data.dropna(subset=['Province'])

    # 如果需要，清除省份名称前后的空格
    data['Province'] = data['Province'].str.strip()
    # data.columns = data.columns.str.strip()
    data['AQI'] = calculate_aqi(data)
    data_cleaned = data.dropna(subset=['Province'])
    province_aqi_avg = data_cleaned.groupby('Province')['AQI'].mean().reset_index()
    return province_aqi_avg

# 处理文件夹中的数据
def process_year_month_folders(base_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for folder_name in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder_name)
        if os.path.isdir(folder_path):
            monthly_aqi_data = pd.DataFrame()

            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):
                    monthly_data = process_aqi_data(file_path)
                    monthly_aqi_data = pd.concat([monthly_aqi_data, monthly_data])

            if not monthly_aqi_data.empty:
                monthly_avg_aqi = monthly_aqi_data.groupby('Province')['AQI'].mean().reset_index()
                output_file_path = os.path.join(output_folder, folder_name + '.csv')
                monthly_avg_aqi.to_csv(output_file_path, index=False)
                print(f"Monthly AQI data saved to {output_file_path}")

base_folder = 'G:\\Data\\OutFirst'  # 包含所有年月子文件夹的基础文件夹路径
output_folder = 'G:\\Data\\OutSecond'  # 存储输出文件的文件夹路径
process_year_month_folders(base_folder, output_folder)
