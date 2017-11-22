#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

df_all = pd.read_csv('start_and_sub.csv')
df_start = pd.read_csv('starding.csv')

df = pd.merge(df_all, df_start, how='left')
df = df.replace(np.NaN, 0.0)
df.to_csv("starting_possibility.csv",index=False)