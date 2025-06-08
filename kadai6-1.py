# kadai6-1.py
# データ：配偶のある人口（A1401）
# API：e-Stat getStatsData（https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData）
# 方法：HTTP GET、JSON形式で取得

import requests
import pandas as pd

APP_ID = "aad65ac8529166d0b87edbe9742e891aa6514233"
API_URL = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

params = {
    "appId": APP_ID,
    "statsDataId": "0000020201",           # 社会・人口統計指標
    "cdCat01": "A1401",                     # 配偶のある人口
    "cdArea": "12101,12102,12103,12104,12105,12106",  # 千葉市の6区
    "metaGetFlg": "Y",
    "cntGetFlg": "N",
    "explanationGetFlg": "Y",
    "annotationGetFlg": "Y",
    "sectionHeaderFlg": "1",
    "replaceSpChars": "0",
    "lang": "J"
}

# APIリクエスト
response = requests.get(API_URL, params=params)
data = response.json()

# データ取得
values = data['GET_STATS_DATA']['STATISTICAL_DATA']['DATA_INF']['VALUE']
df = pd.DataFrame(values)

# 分類項目をコードから名称に変換
meta_info = data['GET_STATS_DATA']['STATISTICAL_DATA']['CLASS_INF']['CLASS_OBJ']
for class_obj in meta_info:
    column_name = '@' + class_obj['@id']
    id_to_name_dict = {}
    if isinstance(class_obj['CLASS'], list):
        for obj in class_obj['CLASS']:
            id_to_name_dict[obj['@code']] = obj['@name']
    else:
        id_to_name_dict[class_obj['CLASS']['@code']] = class_obj['CLASS']['@name']
    df[column_name] = df[column_name].replace(id_to_name_dict)

# 列名を見やすく変更
col_replace_dict = {'@unit': '単位', '$': '値'}
for class_obj in meta_info:
    org_col = '@' + class_obj['@id']
    new_col = class_obj['@name']
    col_replace_dict[org_col] = new_col
df.columns = [col_replace_dict.get(col, col) for col in df.columns]

# 表示
print(df)
