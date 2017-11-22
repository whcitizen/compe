## クラスタリング用のデータ整形

# データの読込
import numpy as np
import pandas as pd
import codecs
with codecs.open("BOX.csv","r","Shift-JIS","ignore") as file:
    df = pd.read_csv(file)
    
# 選手ごとのデータが見やすいようにソート
df = df.sort(["選手ID","試合ID","ピリオド区分"])

# ピリオド区分が「前半」「後半」「全て」であるデータを削除
df = df[df["ピリオド区分"] != 15] 
df = df[df["ピリオド区分"] != 16]
df = df[df["ピリオド区分"] != 18] 

# 6manに「1」の値を付与
df["6man"] = 0
sixman = [8471, 8634, 8498, 8499, 8835, 9057, 9034, 8482, 8493, 8593, 9377, 8707, 8844, 8532, 9388]
for i in range(0, 15):
    df.loc[df["選手ID"] == sixman[i], "6man"] = 1

# DNPを0分0秒に変換
df = df.replace("DNP","0:00")

# プレイタイムを秒に変換
df[["playtime1","playtime2"]] = df["プレイタイム"].str.split(":", expand = True)
df["プレイタイム"] = df["playtime1"].astype(np.int) * 60 + df["playtime2"].astype(np.int)
df = df.drop(["playtime1","playtime2"], axis=1)

# 選手がプレイしたピリオドに「1」を付与
df["period"] = df["プレイタイム"].apply( lambda x: 1 if x > 0 else 0 )

# 選手ごとのデータに変更
group = df.groupby("選手ID")

# 合計プレイタイムを算出
df = group.sum()

# 6manの値を調整
df["6man"] = df["6man"].apply( lambda x: 1 if x > 0 else 0 )

# 必要のない列を削除
del df["試合ID"]
del df["ピリオド区分"]

# csv出力
df.to_csv("input_data.csv")