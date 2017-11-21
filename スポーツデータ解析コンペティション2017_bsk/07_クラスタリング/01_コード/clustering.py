###clustering

##�f�[�^���`

# �f�[�^�̓Ǎ�
import numpy as np
import pandas as pd
import codecs
with codecs.open("input_data.csv","r","Shift-JIS","ignore") as file:
    df = pd.read_csv(file)
    
# �v���C�^�C����ʔ����̃f�[�^��I��
median = df["�v���C�^�C��"].median()
df = df.loc[df["�v���C�^�C��"] >= median]

# �f�[�^�̐��K��
df_st = df.apply(lambda x: (x-x.mean())/x.std(), axis=0).fillna(0)

# �I��ID��6man�̃f�[�^�̕ύX
df_st["�I��ID"] = df["�I��ID"]
df_st["6man"] = df["6man"]

# �s�ԍ��̐U�蒼��
df_st = df_st.reset_index(drop = True)

# csv�Ƃ��ďo��
df_st.to_csv("clustering_data.csv")



## �œK�ȃN���X�^���̌v�Z

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

with codecs.open("clustering_data.csv","r","Shift-JIS","ignore") as file:
    playerdf = pd.read_csv(file)
    
# �I��ID���폜
del playerdf["�I��ID"]
del playerdf["6man"]

# df��array�ɕϊ�
player = playerdf.as_matrix()

# �s�ԍ����폜
player = np.delete(player,0,1)

# �œK�ȃN���X�^���̌v�Z
distortions = []

for i  in range(1,21):               
    km = KMeans(n_clusters=i).fit(player) 
    distortions.append(km.inertia_)   

# �N���X�^���덷�����a�̃O���t�\��
plt.plot(range(1,21),distortions,marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('Distortion')

# �摜�Ƃ��ĕۑ�
plt.savefig("clustering_k.png")



## �N���X�^�����O

# �œK(�Ƃ������Ƃɂ���)�N���X�^���ł̃N���X�^�����O
km = KMeans(n_clusters=5).fit_predict(player) 

# PCA�Ŏ����팸
pca = PCA(n_components=2)
player_r = pca.fit_transform(player)

# ���ʂ��U�z�}�Ƀv���b�g
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
        
# �摜�Ƃ��ĕۑ�
plt.savefig("clustering_output.png")

# �v���C���[�f�[�^�ɑI��ID,�N���X�^�ԍ�,6man��ǉ�
playerdf["clusterid"] = km
playerdf["�I��ID"] = df_st["�I��ID"]
del playerdf["Unnamed: 0"]
playerdf["6man"] = df_st["6man"]

# csv�Ƃ��ďo��
playerdf.to_csv("clustering_result_data.csv")



## �e�N���X�^�̓����c��

# �f�[�^�ҏW
player_c = playerdf
del player_c["�I��ID"]
del player_c["6man"]

# �e�N���X�^�̓���
c0 = player_c[player_c['clusterid']==0].mean()
c1 = player_c[player_c['clusterid']==1].mean()
c2 = player_c[player_c['clusterid']==2].mean()
c3 = player_c[player_c['clusterid']==3].mean()
c4 = player_c[player_c['clusterid']==4].mean()

# csv�Ƃ��ďo��
c0.to_csv("cluster0.csv")
c1.to_csv("cluster1.csv")
c2.to_csv("cluster2.csv")
c3.to_csv("cluster3.csv")
c4.to_csv("cluster4.csv")
