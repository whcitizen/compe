## �N���X�^�����O�p�̃f�[�^���`

# �f�[�^�̓Ǎ�
import numpy as np
import pandas as pd
import codecs
with codecs.open("BOX.csv","r","Shift-JIS","ignore") as file:
    df = pd.read_csv(file)
    
# �I�育�Ƃ̃f�[�^�����₷���悤�Ƀ\�[�g
df = df.sort(["�I��ID","����ID","�s���I�h�敪"])

# �s���I�h�敪���u�O���v�u�㔼�v�u�S�āv�ł���f�[�^���폜
df = df[df["�s���I�h�敪"] != 15] 
df = df[df["�s���I�h�敪"] != 16]
df = df[df["�s���I�h�敪"] != 18] 

# 6man�Ɂu1�v�̒l��t�^
df["6man"] = 0
sixman = [8471, 8634, 8498, 8499, 8835, 9057, 9034, 8482, 8493, 8593, 9377, 8707, 8844, 8532, 9388]
for i in range(0, 15):
    df.loc[df["�I��ID"] == sixman[i], "6man"] = 1

# DNP��0��0�b�ɕϊ�
df = df.replace("DNP","0:00")

# �v���C�^�C����b�ɕϊ�
df[["playtime1","playtime2"]] = df["�v���C�^�C��"].str.split(":", expand = True)
df["�v���C�^�C��"] = df["playtime1"].astype(np.int) * 60 + df["playtime2"].astype(np.int)
df = df.drop(["playtime1","playtime2"], axis=1)

# �I�肪�v���C�����s���I�h�Ɂu1�v��t�^
df["period"] = df["�v���C�^�C��"].apply( lambda x: 1 if x > 0 else 0 )

# �I�育�Ƃ̃f�[�^�ɕύX
group = df.groupby("�I��ID")

# ���v�v���C�^�C�����Z�o
df = group.sum()

# 6man�̒l�𒲐�
df["6man"] = df["6man"].apply( lambda x: 1 if x > 0 else 0 )

# �K�v�̂Ȃ�����폜
del df["����ID"]
del df["�s���I�h�敪"]

# csv�o��
df.to_csv("input_data.csv")