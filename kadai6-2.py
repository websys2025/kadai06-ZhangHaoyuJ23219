# kadai6-2.py
# データ：Open-Meteo 天気予報（https://open-meteo.com）
# API：forecastエンドポイント（https://api.open-meteo.com/v1/forecast）
# 方法：HTTP GET、JSON形式、登録不要

import requests
import pandas as pd

latitude = 35.6073        # 緯度
longitude = 140.1063      # 経度
API_URL = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": latitude,
    "longitude": longitude,
    "hourly": "temperature_2m,weathercode,windspeed_10m",
    "timezone": "Asia/Tokyo"
}

# APIリクエスト
response = requests.get(API_URL, params=params)
data = response.json()

# データ取得
times = data["hourly"]["time"]
temps = data["hourly"]["temperature_2m"]
codes = data["hourly"]["weathercode"]
winds = data["hourly"]["windspeed_10m"]

# DataFrameに変換
df = pd.DataFrame({
    "時刻": times,
    "気温(℃)": temps,
    "天気コード": codes,
    "風速(m/s)": winds
})

# 表示（24時間分）
print(df.head(24))
