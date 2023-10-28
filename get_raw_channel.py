import glob
import os
import rawpy
import numpy as np

def rgbtobayer(data):
    R, G, B = data[..., 0:1], data[..., 1:2], data[..., 2:3]
    R = R[0::2, 0::2]
    G0 = G[0::2, 0::2]
    G1 = G[1::2, 1::2]
    B = B[0::2, 0::2]
    reset_img = np.concatenate([R, G0, B, G1], axis=-1)
    return reset_img

def traverse_dir(path):
    files = glob.glob(os.path.join(path, "*"))

    for file in files:
        if os.path.isdir(file):
            print("文件夹：", file)
            traverse_dir(file)
        else:
            print("读取文件：", file)
            rawim = rawpy.imread(file)
            img_rgb = rawim.postprocess(use_camera_wb=True, half_size=False, no_auto_bright=True, output_bps=16)
            img = rgbtobayer(img_rgb)
            print("shape:", img.shape)
            mean_4c = np.mean(img, axis=(0, 1))
            func(mean_4c)

def write_result(data, name):
    with open(name, "a") as f:
        for i in data:
            f.write(f"{i}\n")

def func(c4):
    list_ = [[], [], [], []]
    for idx, per_elem in enumerate(c4):
        list_[idx].append(per_elem)

    write_result(list_[0], "r.txt")
    write_result(list_[1], "g0.txt")
    write_result(list_[2], "b.txt")
    write_result(list_[3], "g1.txt")

# 图像文件路径
dir_path = "dir1"
traverse_dir(dir_path)
