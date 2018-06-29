# _*_ coding : utf-8 _*_
# 数値計算用モジュール
import numpy as np
import scipy as sp
import math

# 高速化用モジュール
from numba import jit

# 汎用モジュール
import os
import time
import datetime
from tqdm import tqdm
import subprocess


# 実験用パラメータ
# --------------------------------------------------------------
particles_number = 1000     # 粒子数
particles_velocity = 1.0    # 粒子の速さ
search_radius = 1.0         # 粒子の探査半径 


timestep = 1000             # シミュレーションの時間
# --------------------------------------------------------------

today = datetime.date.today()
today = today.strftime("%Y%m%d")
data_path = "./data/{}"
