# -*- coding: utf-8 -*-
## スタメンデータ

# データの読込
import pandas as pd
#import codecs
#with codecs.open("BOX.csv","r","Shift-JIS","ignore") as file:
#    df = pd.read_csv(file)
    
df = pd.read_csv('BOX.csv')
# 必要のない列を削除
del df['homeaway']
del df['team']
del df['team_eng']
del df['uni_no']
del df['player_name']

##starting###
# startingを取り出す
df1 = df[df["period"]==1]
df1 = df1[df1["starting"]==1]

# 選手ごとに集計
group = df1.groupby("player_id")
df1 = group.sum()

# csv出力
df1 = df1.loc[:,['starting']]
df1.to_csv("starding.csv")


##statining + sub##
df2 = df[df["period"]==1]
a = df2['player_id'].value_counts()
a.to_csv('star_and_sub.csv')
#
#df = pd.read_csv('starding.csv')
#n_player = df.shape[0]
#player_mst = pd.read_csv("player_master.csv")
#
#res = pd.merge(df, player_mst, on='player_id')
##移籍したメンバーは除く
#iseki_id = [8511,9026,9053,9061,9067,9071,9356,9374,9381,9385,9404,9454]
#for i in iseki_id:
#    res = res[res["player_id"] != i]
#
#res.to_csv("res.csv",index=False)