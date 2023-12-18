import pandas as pd
import numpy as np
import requests

# 读取CSV文件
csv_file_path = 'G:\\Lenovo\\Documents\\OneDrive\\University\\Education\\2023秋\\数据可视化\\201301\\CN-Reanalysis-daily-2013010100.csv'  # 替换为您的CSV文件路径
df = pd.read_csv(csv_file_path)

# 修正列名，消除前后的空格
df.columns = df.columns.str.strip()

# AQI计算的阈值
Idata = [
    [0, 35, 75, 115, 150, 250, 350, 500],  # PM2.5 24小时平均
    [0, 50, 150, 250, 350, 420, 500, 600],  # PM10 24小时平均
    [0, 150, 500, 650, 800],  # SO2
    [0, 100, 200, 700, 1200, 2340, 3090, 3840],  # NO2
    [0, 5, 10, 35, 60, 90, 120, 150],  # CO
    [0, 160, 200, 300, 400, 800, 1000, 1200]  # O3
]
qua = [0, 50, 100, 150, 200, 300, 400, 500]

# 计算AQI的函数
def calculate_aqi(data, idata, qua):
    IAQI = np.zeros(len(data))
    for i in range(len(data)):
        for k in range(1, len(idata)):
            if idata[k] > data[i]:
                IAQI[i] = int(round((((qua[k] - qua[k - 1]) / (idata[k] - idata[k - 1])) * (data[i] - idata[k - 1]) + qua[k - 1]) + 0.5))
                break
    return IAQI

# 应用AQI计算
df['AQI_PM2.5'] = calculate_aqi(df['PM2.5(微克每立方米)'], Idata[0], qua)
df['AQI_PM10'] = calculate_aqi(df['PM10(微克每立方米)'], Idata[1], qua)
df['AQI_SO2'] = calculate_aqi(df['SO2(微克每立方米)'], Idata[2], qua)
df['AQI_NO2'] = calculate_aqi(df['NO2(微克每立方米)'], Idata[3], qua)
df['AQI_CO'] = calculate_aqi(df['CO(毫克每立方米)'], Idata[4], qua)
df['AQI_O3'] = calculate_aqi(df['O3(微克每立方米)'], Idata[5], qua)

# 取各污染物AQI的最大值为该点的AQI值
df['AQI'] = df[['AQI_PM2.5', 'AQI_PM10', 'AQI_SO2', 'AQI_NO2', 'AQI_CO', 'AQI_O3']].max(axis=1)

# 获取省市区信息的函数
AMAP_KEY = '6281fd12a4d1945f725906f41553df3d'  # 替换为您的API密钥
AMAP_API_URL = 'https://restapi.amap.com/v3/geocode/regeo'

def get_location_info(lat, lon, key=AMAP_KEY):
    params = {
        'location': f'{lon},{lat}',
        'key': key,
        'radius': 1000,
        'extensions': 'all',
        'batch': 'false',
        'roadlevel': 0
    }
    response = requests.get(AMAP_API_URL, params=params)
    if response.status_code == 200:
        json_data = response.json()
        if json_data.get('status') == '1' and json_data.get('regeocode'):
            address_info = json_data.get('regeocode').get('addressComponent')
            province = address_info.get('province', '')
            city = address_info.get('city', '')
            district = address_info.get('district', '')
            return province, city, district
    return None, None, None

# 添加省市区信息
for index, row in df.iterrows():
    lat = row['lat']
    lon = row['lon']
    province, city, district = get_location_info(lat, lon)
    df.at[index, 'Province'] = province
    df.at[index, 'City'] = city
    df.at[index, 'District'] = district
# 遍历所有列，将列表转换为字符串
for col in df.columns:
    df[col] = df[col].apply(lambda x: ','.join(x) if isinstance(x, list) else x)

# 再次尝试计算每个省市区的AQI平均值
try:
    aqi_avg = df.groupby(['Province', 'City', 'District'])['AQI'].mean().reset_index()
    print(aqi_avg.head())  # 显示前几行结果
except Exception as e:
    print(f"An error occurred: {e}")


# 处理省市区信息中的列表
df['City'] = df['City'].apply(lambda x: ','.join(x) if isinstance(x, list) else x)

# 计算每个省市区的AQI平均值
aqi_avg = df.groupby(['Province', 'City', 'District'])['AQI'].mean().reset_index()

# 清洗数据：移除省市区字段为空的行
cleaned_aqi_avg = aqi_avg[(aqi_avg['Province'] != '') & (aqi_avg['City'] != '') & (aqi_avg['District'] != '')]

# 输出清洗后的数据
print(cleaned_aqi_avg.head())

# 如果需要，保存结果到文件
output_file_path = 'aqi_average.csv'  # 替换为您想保存的文件路径
cleaned_aqi_avg.to_csv(output_file_path, index=False)
