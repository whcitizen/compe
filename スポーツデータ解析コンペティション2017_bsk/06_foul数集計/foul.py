## foul

# データの読込
import numpy as np
import pandas as pd
import codecs
with codecs.open("playbyplay.csv","r","Shift-JIS","ignore") as file:
    df = pd.read_csv(file)
    
# 欠損値を含むプレイデータの削除など
df1 = df.dropna(subset=["試合ID", "ホームアウェイ", "プレイテキスト"])
df2 = df1.ix[:, ["試合ID", "ホームアウェイ","プレイテキスト"]]

# ファウルを含まないプレイデータの削除
df3 = df2[df2['プレイテキスト'].str.contains("#")]
df4 = df3[df3['プレイテキスト'].str.contains("-")]
df5 = df4[df4['プレイテキスト'].str.contains(":")]

# 個人・チームファウル数の洗い出し
foul = np.empty((df5.shape[0], 3))
for i in range(df5.shape[0]):
    test = df5.iloc[i, 2]
    # 累計個人ファウル数
    i1 = test.split("(")
    i2 = i1[1]
    i3 = i2.rsplit("-")
    foul[i, 0] = i3[0]
    # 累計チームファウル数
    t1 = test.split("-")
    t2 = t1[1]
    t3 = t2.rsplit(":")
    foul[i, 1] = t3[0]
    foul[i, 2] = "0"

# 表への変換
foul_df = pd.DataFrame(foul,columns={"I","T","value"}) #大事！
#imx = foul_df[0].max() -> 5
#tmx = foul_df[1].max() -> 16
foul_new = foul_df.groupby(['I','T']).count()
foul_new2 = foul_new.reset_index() #大事！
foul_new3 = pd.DataFrame(foul_new2.pivot_table(index = "I", columns = "T", fill_value = 0))

# csvとして出力
foul_new3.to_csv("foul_new3.csv")