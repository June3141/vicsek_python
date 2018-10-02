# _*_ coding: utf-8 _*_
import matplotlib.pyplot as plt
import numpy as np

import glob
import datetime
import os
from tqdm import tqdm


L = 24

noise_init = 0.20
noise_repeat = 1
noise_width = 0.10

delta_init = 12.0
delta_repeat = 1
delta_width = 1.0

today = datetime.date.today()
today = today.strftime("%Y%m%d")
data_path = "./data/{}".format(today)

if __name__ == "__main__":
    
    for dx in range(delta_repeat):
        delta_path = data_path + "/{0:03d}".format(int(delta_init + dx * delta_width))

        for q in range(delta_repeat):
            noise_path = data_path + "/{0:03d}/{1:03d}".format(int(delta_init + dx * delta_width), int((noise_init + q * noise_width) * 100))
            data_list = glob.glob(noise_path + "/*.dat")
            data_list.sort()

            fig_path = "./figure/{}".format(today)
            fig_delta = fig_path + "/{0:03d}".format(int(delta_init + dx * delta_width))
            fig_noise = fig_path + "/{0:03d}/{1:03d}".format(int(delta_init + dx * delta_width), int((noise_init + q * noise_width) * 100))

            # ディレクトリの作成
            if not os.path.isdir(fig_path):
                os.makedirs(fig_path)
            
            if not os.path.isdir(fig_delta):
                os.makedirs(fig_delta)
            
            if not os.path.isdir(fig_noise):
                os.makedirs(fig_noise)
            else:
                png_list = glob.glob(fig_noise + "/*.png")
                for i in range(len(png_list)):
                    os.remove(png_list[i])

        for time in tqdm(range(len(data_list))):
            file_path = data_list[time]
            particles = np.loadtxt(file_path, delimiter = ",")
            
            x = particles[:, 0]
            y = particles[:, 1]
            theta = particles[:, 2]
            
            u = np.cos(theta)
            v = np.sin(theta)
            
            fig = plt.figure(figsize = (8, 8))
            plt.xlim([-L, L])
            plt.ylim([-L, L])        
            plt.grid()
            
            plt.rcParams["font.size"] = 18
            plt.title("time = {0:05d}".format(time), loc = 'center')
            plt.tight_layout()
            
            plt.quiver(x, y, u, v, angles = "xy", scale_units = "xy", scale = 0.4)
            plt.draw()

            plt.savefig(fig_noise + "/{0:05d}.png".format(time))
            plt.close()