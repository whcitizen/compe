###�N���X�^�����O�̏o�͐}���e�|�W�V�����ŐF����

# �f�[�^�̓Ǎ�
import numpy as np
import pandas as pd
import codecs
with codecs.open("input_data.csv","r","Shift-JIS","ignore") as file:
    df = pd.read_csv(file)
with codecs.open("input_data.csv","r","Shift-JIS","ignore") as file2:
    df2 = pd.read_csv(file2)
    
# �v���C�^�C����ʔ����̃f�[�^��I��
median = df["�v���C�^�C��"].median()
df = df.loc[df["�v���C�^�C��"] >= median]

# �|�W�V�����f�[�^����U����
del df["position"]

# �f�[�^�̐��K��
df_st = df.apply(lambda x: (x-x.mean())/x.std(), axis=0).fillna(0)

# �I��ID��6man�̃f�[�^�̕ύX
df_st["�I��ID"] = df["�I��ID"]
df_st["6man"] = df["6man"]
df_st["position"] = df2["position"]

# �s�ԍ��̐U�蒼��
df_st = df_st.reset_index(drop = True)

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

with codecs.open("clustering_data.csv","r","Shift-JIS","ignore") as file:
    playerdf = pd.read_csv(file)
    
# �I��ID,6man,�|�W�V���������폜
del playerdf["�I��ID"]
del playerdf["6man"]
del playerdf["position"]

# df��array�ɕϊ�
player = playerdf.as_matrix()

# �s�ԍ����폜
player = np.delete(player,0,1)

# �œK(�Ƃ������Ƃɂ���)�N���X�^���ł̃N���X�^�����O
km = KMeans(n_clusters=5).fit_predict(player) 

# PCA�Ŏ����팸
pca = PCA(n_components=2)
player_r = pca.fit_transform(player)

# �|�W�V�����̃f�[�^�t���[�����쐬
dfpos = df_st["position"]

# ���ʂ��U�z�}�Ƀv���b�g
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
        
# �摜�Ƃ��ĕۑ�
plt.savefig("clustering_" + dataname + ".png")