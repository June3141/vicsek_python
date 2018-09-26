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

noise_power = 0.20
timestep = 1000             # シミュレーションの時間


boundary_radius = 12.0
boundary_delta = 12.0
# --------------------------------------------------------------

center_r = [  boundary_delta / 2, 0]
center_l = [- boundary_delta / 2, 0]

today = datetime.date.today()
today = today.strftime("%Y%m%d")
data_path = "./data/{}".format(today)


def cal_distance(r1, r2):
    diff = np.sqrt((r1[0] - r2[0]) ** 2 + (r1[1] - r2[1]) ** 2)
    return diff
    
def diff_right_center(r1):
    diff = np.sqrt((r1[0] - boundary_delta / 2) ** 2 + r[1] ** 2)
    return diff

def diff_left_center(r2):
    diff = np.sqrt((r1[0] + boundary_delta / 2) ** 2 + r[1] ** 2)
    return diff


def position_update(particles_old, particles_new):
    theta = [particles_old[i, 2] for i in range(particles_number)]    
    x_new = [particles_old[i, 0] + particles_velocity * np.cos(theta[i]) \
            for i in range(particles_number)]
    y_new = [particles_old[i, 1] + particles_velocity * np.sin(theta[i]) \
            for i in range(particles_number)]

    for i in range(particles_number):
        particles_new[i, 0] = x_new[i]
        particles_new[i, 1] = y_new[i]
        
    return particles_new


def theta_update(particles_old, particles_new):
    for i in range(particles_number):
        particles_i = particles_old[i]
        diff_from_i = [cal_distance(particles_i, particles_old[j]) for j in range(particles_number)]
        
        theta_new = 0
        count = 0

        for j in range(particles_number):
            if diff_from_i[j] <= search_radius:
                theta_new += particles_old
                count += 1

        particles_new[i, 2] = theta_new / count + noise_power * np.random.randn()

    return particles_new


#粒子の初期化（初期条件としてランダムに配置）
def particles_init():
    #ピーナツ型境界が接する形で箱型の領域を考える．
    #適当に箱型領域内に粒子をセット．境界内に入るまでランダムな振り分けを繰り返す．
    box_x = 2 * boundary_radius + boundary_delta
    box_y = 2 * boundary_radius
    
    particles = np.zeros((particles_number, 3))

    for i in range(particles_number):
        x = box_x * np.random.rand() - box_x / 2
        y = box_y * np.random.rand() - box_y / 2

        #左右の円の中心からの距離を測定する．
        diff_r_center = np.sqrt((x - boundary_delta / 2) ** 2 + y ** 2)
        diff_l_center = np.sqrt((x + boundary_delta / 2) ** 2 + y ** 2)
        
        # 境界内に入りきれなかった場合
        while diff_l_center >= boundary_radius and diff_r_center >= boundary_radius:
            x = box_x * np.random.rand() - box_x / 2
            y = box_y * np.random.rand() - box_y / 2

            diff_r_center = np.sqrt((x - boundary_delta / 2) ** 2 + y ** 2)
            diff_l_center = np.sqrt((x + boundary_delta / 2) ** 2 + y ** 2)

        particles[i, 0] = x
        particles[i, 0] = y
        particles[i, 0] = 2 * np.pi * np.random.rand() - np.pi

    return particles

def correct_position():

    return x, y

def check_boudary(particles_old, particles_new):
    diff_r_list = [diff_right_center(particles_new[i]) for i in range(particles_new)]
    diff_l_list = [diff_left_center(particles_new[i]) for i in range(particles_new)]

    for i in range(particles_number):
        if diff_r_list[i] >= boundary_radius and diff_l_list[i] >= boundary_radius:
            x_diff, y_diff = correct_position(particles_new[i])

        elif :

        
        particles_new[i, 0] = particles_old[i, 0] + x_diff
        particles_new[i, 1] = particles_old[i, 1] + y_diff

    
    return particles_new


if __name__ == '__main__':
    
    old_particles = particles_init()
    new_particles = np.zeros((particles_number, 3))

    for t in tqdm(range(timestep)):
        new_particles = position_update(old_particles, new_particles)
        new_particles = theta_update(old_particles, new_particles)
        new_particles = check_boudary(old_particles, new_particles)

        save_path = data_path + "/{0:3d}/{1:02d}/{2:05d}.dat".format(boundary_delta, noise_power * 100, t)
        np.savetxt(save_path, old_particles, delimiter=", ")

        # t -> t+1 の更新
        old_particles = new_particles