#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SDC2017bsk
アクション分析用
@author: moritahitomi
"""
import pandas as pd
#import numpy as np

#各試合のアクションの総数を出力する
#action : タイムアウト、ピリオド数、試合終了などチームに関係ないものもカウントされている(この場合teamID=0)
#shoot : action1 = 1~8
#shoot_success : action1 = 1,3,4,7
#foul: action1 = 20~26

def count_action(save=True):
    play_data = pd.read_csv("/Users/moritahitomi/Desktop/SDC2017bsk/data/play-by-play.csv")
    play_data = play_data.loc[:,['game_ID','game_action_cound',
                                         'team_ID','home_score', 'away_score',
                                         'action1', 'action2', 'action3', 'home']]
    result_df = pd.DataFrame(columns=["game_ID","home_win", "home_all_action",
                                      "home_shoot", "home_shoot_success",
                                      "home_foul", "away_win","away_all_action",
                                      "away_shoot","away_shoot_success","away_foul"])
    
    game_ID_list = get_game_ID_list()
    for i in game_ID_list:     
        #get game info
        game_info = get_game_info(game_ID=i)
        
        #get teaminfo
        hometeam_ID = game_info.loc[[i],["hometeam_ID"]].values[0][0]
        #hometeam_ID = game_info["hometeam_ID"][0]
        awayteam_ID = game_info.loc[[i],["awayteam_ID"]].values[0][0]
        #awayteama_ID = game_info["awayteam_ID"][0]
        #if game_info["home_sore"][0] == game_info["away_score"][0]: #draw
        if game_info.loc[[i],["home_sore"]].values[0][0] == game_info.loc[[i],["away_score"]].values[0][0]:
            home_win = -1
            away_win = -1
        elif game_info.loc[[i],["home_sore"]].values[0][0] > game_info.loc[[i],["away_score"]].values[0][0]:
            home_win = 1
            away_win = 0
        else:
            home_win = 0
            away_win = 1
            
        #get play data
        game_df = play_data[play_data['game_ID'].isin([i])]#extract : game_ID=i
        
        #extract home team play data
        home_game_df = game_df[game_df["team_ID"].isin([hometeam_ID])]
        home_shoot_df = home_game_df[home_game_df["action1"].isin([i for i in range(1,9)])]
        home_shoot_success_df = home_game_df[home_game_df["action1"].isin([1,3,4,7])]
        home_foul_df = home_game_df[home_game_df["action1"].isin([i for i in range(20,27)])]
        
        home_all_action = home_game_df.shape[0]
        home_shoot = home_shoot_df.shape[0]
        home_shoot_success = home_shoot_success_df.shape[0]
        home_foul = home_foul_df.shape[0]
        
        #extract away team play data
        away_game_df = game_df[game_df["team_ID"].isin([awayteam_ID])]
        away_shoot_df = away_game_df[away_game_df["action1"].isin([i for i in range(1,9)])]
        away_shoot_success_df = away_game_df[away_game_df["action1"].isin([1,3,4,7])]
        away_foul_df = away_game_df[away_game_df["action1"].isin([i for i in range(20,27)])]
        
        away_all_action = away_game_df.shape[0]
        away_shoot = away_shoot_df.shape[0]
        away_shoot_success = away_shoot_success_df.shape[0]
        away_foul = away_foul_df.shape[0]
        
        if i%10 ==0:
            print("now counting : game " +str(i))
        
        #result
        result_sub = pd.DataFrame({"game_ID": i,
                                   "home_win" : home_win,
                                   "home_all_action" : home_all_action,
                                   "home_shoot" : home_shoot,
                                   "home_shoot_success" : home_shoot_success,
                                   "home_foul" : home_foul,
                                   "away_win" : away_win,
                                   "away_all_action" : away_all_action,
                                   "away_shoot" : away_shoot,
                                   "away_shoot_success" : away_shoot_success,
                                   "away_foul" : away_foul},
                                    index=[""])
        result_df = pd.concat([result_df,result_sub])
        
    #save csv file
    if save==True:
        result_df.to_csv("/Users/moritahitomi/Desktop/SDC2017bsk//output/action_count_per_game.csv", index=None)
        

#game_data.csvからgame_ID=iの情報を取り出す
def get_game_info(game_ID): #get info of the game i
    game_data = pd.read_csv("/Users/moritahitomi/Desktop/SDC2017bsk/data/game_data.csv")
    game_all_info = game_data[game_data['game_ID'].isin([game_ID])]
    #game_all_info : DataFrame whose columns are
    #['game_ID', 'game_day', 'cup_ID', 'cup_name', 'max_period', 'stage',
      #'awayteam_ID', 'hometeam_name', 'awayteam_ID', 'awayteam_name',
      #'studiam_ID', 'studiam_name', 'start_time', 'end_time', 'spectator',
      #'home_sore', 'away_score', 'main_unpire_ID', 'main_umpire_name',
      #'sub_umpire_ID1', 'sub_umpire_name1', 'sub_umpire_ID2',
      #'sub_umpire_name2', 'weather', 'temperture', 'humidity', 'No.']
    
    if game_all_info.shape[0]==1:
        game_info = game_all_info.loc[:,['game_ID','hometeam_ID','awayteam_ID',
                                         'home_sore','away_score']] #DataFrame of shape(1,5)
        game_info.index=[game_ID]
        return game_info
    else:
        pass
    
def get_game_ID_list():
    game_data = pd.read_csv("/Users/moritahitomi/Desktop/SDC2017bsk/data/game_data.csv")
    game_ID_df = game_data["game_ID"]
    game_ID_list = list(game_ID_df)
    return game_ID_list
    

     
if __name__ == "__main__":
    count_action(save=True)
