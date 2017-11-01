#�f�[�^�̓Ǎ�
import numpy as np
import pandas as pd
import codecs
with codecs.open("playbyplay.csv","r","Shift-JIS","ignore") as file:
    df = pd.read_csv(file)

#�����l���܂ރv���C�f�[�^�̍폜�Ȃ�
df1 = df.dropna(subset=["����ID", "�z�[���A�E�F�C", "�v���C�e�L�X�g"])
df2 = df1.ix[:, ["����ID", "�z�[���A�E�F�C","�v���C�e�L�X�g"]]

#�t�@�E�����܂܂Ȃ��v���C�f�[�^�̍폜
df3 = df2[df2['�v���C�e�L�X�g'].str.contains("#")]
df4 = df3[df3['�v���C�e�L�X�g'].str.contains("-")]
df5 = df4[df4['�v���C�e�L�X�g'].str.contains(":")]
df5

#�l�E�`�[���t�@�E�����̐􂢏o��
foul = np.empty((df5.shape[0], 3))
for i in range(df5.shape[0]):
    test = df5.iloc[i, 2]
    #�݌v�l�t�@�E����
    i1 = test.split("(")
    i2 = i1[1]
    i3 = i2.rsplit("-")
    foul[i, 0] = i3[0]
    #�݌v�`�[���t�@�E����
    t1 = test.split("-")
    t2 = t1[1]
    t3 = t2.rsplit(":")
    foul[i, 1] = t3[0]
    foul[i, 2] = "0"
foul

foul_df = pd.DataFrame(foul,columns={"I","T","value"}) #�厖�I
#imx = foul_df[0].max() -> 5
#tmx = foul_df[1].max() -> 16
foul_new = foul_df.groupby(['I','T']).count()
foul_new2 = foul_new.reset_index() #�厖�I
foul_new3 = pd.DataFrame(foul_new2.pivot_table(index = "I", columns = "T", fill_value = 0))
foul_new3

foul_new3.to_csv("foul_new3.csv")