# -*- coding: utf-8 -*-
"""
boxデータをx，シックスマン頻度をyとして，RIDGE回帰を適用
"""

import csv
import numpy as np
import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt
import time


if __name__ == "__main__":
    # LASSO に使うデータを作成
    df = pd.read_csv("input_data.csv")  # pandasでcsvを読込
    df = pd.DataFrame(df)               # DataFrame形式にする
    df = df.loc[df["play_time"] >= df["play_time"].median()]  # プレイタイム上位半分のデータを選択
    data_y = df["probability_6man"]     # DataFrameから，yとして使用する列を抽出
    drop_idx = ["player_id", "frag_starting", "play_time", "frag_6man",
                "period", "position", "probability_6man"]  # xとして使用しない列を選択
    data_x = df.drop(drop_idx, axis=1)  # DataFrameから，xとして使用する列を抽出

    data_y = np.array(data_y, dtype=float)  # numpyのarray形式にすることで演算可能になる
    data_x = np.array(data_x, dtype=float)

    data_x = (data_x - data_x.mean(axis=0)) / data_x.std(axis=0)  # xを標準化

    # ハイパーパラメータを交差確認法により推定
    # sklearnのlinear_modelにあるLassoCV（Lassoの交差確認法のひとつ。LassoCVの他にもう一つやり方があったんだけど関数名が出てこない……）を、ridge_cvと定義
    ridge_cv = linear_model.RidgeCV()
    ridge_cv.fit(data_x, data_y)  # data_xとdata_yをlasso_cvにかける

    # alphaとして交差確認法で算出した値を使用
    # lasso = linear_model.Lasso(alpha=lasso_cv.alpha_)
    ridge = linear_model.Ridge(alpha=ridge_cv.alpha_)
    ridge.fit(data_x, data_y)
    c = np.array(ridge.coef_)  # cは係数のベクトル

    # 結果の表示
    print("交差確認法により推定された適切なハイパーパラメータ alpha :")
    print(ridge_cv.alpha_)  # 交差確認法の結果を表示，ハイパーパラメータalphaを返す
    print()  # 1行空ける
    print("LASSO により推定されたパラメータ:")
    print(c)
    print()  # 1行空ける
    print("非ゼロ係数のインデックス:")
    print(np.nonzero(c)[0])
    print()  # 1行空ける
    print("非ゼロ係数の数:")
    print(np.nonzero(c)[0].size)  # 非ゼロ係数の数
    print()  # 1行空ける
    print("モデルの決定係数:")
    print(ridge.score(data_x, data_y))  # モデルの決定係数を算出

    # LASSO Path の表示
    print("Computing regularization path using the LARS ...")
    alphas, _, coefs = linear_model.lars_path(data_x, data_y, method='ridge', verbose=True)

    xx = np.sum(np.abs(coefs.T), axis=1)
    xx /= xx[-1]

    plt.plot(xx, coefs.T)
    ymin, ymax = plt.ylim()
    plt.vlines(xx, ymin, ymax, linestyle='dashed')
    plt.xlabel('|coef| / max|coef|')
    plt.ylabel('Coefficients')
    plt.title('RIDGE Path')
    plt.axis('tight')
    plt.show()

    # 結果の出力
    np.savetxt("indices_6man_ridge.csv", np.nonzero(c)[0], delimiter=",")  # 非ゼロの変数のインデックスをcsvに書き出し
    np.savetxt('coef_6man_ridge.csv', c, delimiter=',')  # 係数ベクトルをcsvに書き出し
