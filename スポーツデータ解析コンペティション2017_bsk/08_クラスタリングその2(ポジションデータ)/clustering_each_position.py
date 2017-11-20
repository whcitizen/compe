###クラスタリングの出力図を各ポジションで色分け

# データの読込
import numpy as np
import pandas as pd
import codecs
with codecs.open("input_data.csv","r","Shift-JIS","ignore") as file:
    df = pd.read_csv(file)
with codecs.open("input_data.csv","r","Shift-JIS","ignore") as file2:
    df2 = pd.read_csv(file2)
    
# プレイタイム上位半分のデータを選択
median = df["プレイタイム"].median()
df = df.loc[df["プレイタイム"] >= median]

# ポジションデータを一旦消去
del df["position"]

# データの正規化
df_st = df.apply(lambda x: (x-x.mean())/x.std(), axis=0).fillna(0)

# 選手IDと6manのデータの変更
df_st["選手ID"] = df["選手ID"]
df_st["6man"] = df["6man"]
df_st["position"] = df2["position"]

# 行番号の振り直し
df_st = df_st.reset_index(drop = True)

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

with codecs.open("clustering_data.csv","r","Shift-JIS","ignore") as file:
    playerdf = pd.read_csv(file)
    
# 選手ID,6man,ポジション情報を削除
del playerdf["選手ID"]
del playerdf["6man"]
del playerdf["position"]

# dfをarrayに変換
player = playerdf.as_matrix()

# 行番号を削除
player = np.delete(player,0,1)

# 最適(ということにする)クラスタ数でのクラスタリング
km = KMeans(n_clusters=5).fit_predict(player) 

# PCAで次元削減
pca = PCA(n_components=2)
player_r = pca.fit_transform(player)

# ポジションのデータフレームを作成
dfpos = df_st["position"]

# 結果を散布図にプロット
position = "C"
position_color = "purple"

if "/" in position:
    dataname = position.replace("/", "or")
else:
    dataname = position

plt.figure()
for i in range(0, len(km)):
    if dfpos[i] == position:
        plt.scatter(player_r[i, 0], player_r[i, 1], c= position_color)

plt.title("player clustering " + position)
plt.xlim([-7,15])
plt.ylim([-6,7])

sixman = [22, 28, 31, 32, 52, 85, 158, 165, 172, 181, 217, 223]
for i in range(0, len(sixman)):
    if dfpos[sixman[i]] == position:
        plt.plot(player_r[sixman[i],0], player_r[sixman[i],1], color = position_color, marker = "*", markersize = 15)
        
# 画像として保存
plt.savefig("clustering_" + dataname + ".png")