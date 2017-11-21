###clustering

##データ整形

# データの読込
import numpy as np
import pandas as pd
import codecs
with codecs.open("input_data.csv","r","Shift-JIS","ignore") as file:
    df = pd.read_csv(file)
    
# プレイタイム上位半分のデータを選択
median = df["プレイタイム"].median()
df = df.loc[df["プレイタイム"] >= median]

# データの正規化
df_st = df.apply(lambda x: (x-x.mean())/x.std(), axis=0).fillna(0)

# 選手IDと6manのデータの変更
df_st["選手ID"] = df["選手ID"]
df_st["6man"] = df["6man"]

# 行番号の振り直し
df_st = df_st.reset_index(drop = True)

# csvとして出力
df_st.to_csv("clustering_data.csv")



## 最適なクラスタ数の計算

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

with codecs.open("clustering_data.csv","r","Shift-JIS","ignore") as file:
    playerdf = pd.read_csv(file)
    
# 選手IDを削除
del playerdf["選手ID"]
del playerdf["6man"]

# dfをarrayに変換
player = playerdf.as_matrix()

# 行番号を削除
player = np.delete(player,0,1)

# 最適なクラスタ数の計算
distortions = []

for i  in range(1,21):               
    km = KMeans(n_clusters=i).fit(player) 
    distortions.append(km.inertia_)   

# クラスタ内誤差平方和のグラフ表示
plt.plot(range(1,21),distortions,marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('Distortion')

# 画像として保存
plt.savefig("clustering_k.png")



## クラスタリング

# 最適(ということにする)クラスタ数でのクラスタリング
km = KMeans(n_clusters=5).fit_predict(player) 

# PCAで次元削減
pca = PCA(n_components=2)
player_r = pca.fit_transform(player)

# 結果を散布図にプロット
plt.figure()
for i in range(0, len(km)):
    if km[i] == 0:
        plt.scatter(player_r[i, 0], player_r[i, 1], c='red')
    elif km[i] == 1:
        plt.scatter(player_r[i, 0], player_r[i, 1], c='green')
    elif km[i] == 2:
        plt.scatter(player_r[i, 0], player_r[i, 1], c='Cyan')
    elif km[i] == 3:
        plt.scatter(player_r[i, 0], player_r[i, 1], c='orange')
    elif km[i] == 4:
        plt.scatter(player_r[i, 0], player_r[i, 1], c='pink')

plt.title("player clustering")
        
sixman = [22, 28, 31, 32, 52, 85, 158, 165, 172, 181, 217, 223]
for i in range(0, len(sixman)):
    plt.plot(player_r[sixman[i],0], player_r[sixman[i],1], color = "blue", marker = "*", markersize = 15)
        
# 画像として保存
plt.savefig("clustering_output.png")

# プレイヤーデータに選手ID,クラスタ番号,6manを追加
playerdf["clusterid"] = km
playerdf["選手ID"] = df_st["選手ID"]
del playerdf["Unnamed: 0"]
playerdf["6man"] = df_st["6man"]

# csvとして出力
playerdf.to_csv("clustering_result_data.csv")



## 各クラスタの特徴把握

# データ編集
player_c = playerdf
del player_c["選手ID"]
del player_c["6man"]

# 各クラスタの特徴
c0 = player_c[player_c['clusterid']==0].mean()
c1 = player_c[player_c['clusterid']==1].mean()
c2 = player_c[player_c['clusterid']==2].mean()
c3 = player_c[player_c['clusterid']==3].mean()
c4 = player_c[player_c['clusterid']==4].mean()

# csvとして出力
c0.to_csv("cluster0.csv")
c1.to_csv("cluster1.csv")
c2.to_csv("cluster2.csv")
c3.to_csv("cluster3.csv")
c4.to_csv("cluster4.csv")
