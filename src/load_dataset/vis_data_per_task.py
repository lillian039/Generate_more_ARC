#!/usr/bin/env python
# coding=utf-8

import os
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, Normalize
import numpy as np
import json
from PIL import Image

COLORS = {
    0: '#000000', # default
    1: '#0074D9', # blue
    2: '#FF4136', # red
    3: '#2ECC40', # green
    4: '#FFDC00', # yellow
    5: '#AAAAAA', # gray
    6: '#F012BE', # magenta
    7: '#FF851B', # orange
    8: '#7FDBFF', # aqua
    9: '#870C25', # maroon
} # from https://flatuicolors.com/
cmap = ListedColormap([COLORS[i] for i in range(len(COLORS))])
norm = Normalize(vmin=0, vmax=len(COLORS)-1)

def plot_matrix(matrix, root, fn, mode, i, name):
    imgdir = os.path.join(root, 'img')
    os.makedirs(imgdir, exist_ok=True)
    # print(matrix)
    os.makedirs(imgdir, exist_ok=True)
    plt.imshow(matrix, cmap=cmap, norm=norm)

    
    plt.xticks(np.arange(-0.5, np.array(matrix).shape[1], 1), minor=True)
    plt.yticks(np.arange(-0.5, np.array(matrix).shape[0], 1), minor=True)
    

    # plt.grid(which='minor', color='white', linestyle='-', linewidth=1)
    plt.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False)
    plt.savefig(os.path.join(imgdir, '{}_{}_{}_{}.png'.format(str(fn).replace('.json', ''), mode, i, name)), bbox_inches='tight')
    plt.close()

def plot_data(data, root, fn, mode, i):
    assert tuple(sorted(list(data.keys()))) == ('input', 'output')
    input_matrix = data['input']
    output_matrix = data['output']
    plot_matrix(input_matrix, root, fn, mode, i, 'input')
    plot_matrix(output_matrix, root, fn, mode, i, 'output')

def synthesize_data(root, fn, train_data, generate_number):
    syn_img_dir = os.path.join(root, 'syn_img')
    os.makedirs(syn_img_dir, exist_ok=True)
    imgdir = os.path.join(root, 'img')
    os.makedirs(syn_img_dir, exist_ok=True)
    for i, train_data_i in enumerate(train_data):
        img_input_path = os.path.join(imgdir, '{}_{}_{}_{}.png'.format(str(fn).replace('.json', ''), generate_number, i, "input"))
        img_output_path = os.path.join(imgdir, '{}_{}_{}_{}.png'.format(str(fn).replace('.json', ''), generate_number, i, "output"))
        
        img_input = Image.open(img_input_path)
        img_output = Image.open(img_output_path)
        
        max_height = max(img_input.height, img_output.height)

        # 定义白边的宽度
        padding_width = 10

        # 计算最终图片的宽度和高度
        total_width = img_input.width + padding_width + img_output.width
        total_height = max_height

        # 创建一个新的大画布
        result = Image.new('RGB', (total_width, total_height), color='white')

        # 在合适的位置拼接图片和白边
        result.paste(img_input, (0, 0))
        result.paste(Image.new('RGB', (padding_width, total_height), color='white'), (img_input.width, 0))
        result.paste(img_output, (img_input.width + padding_width, 0))
        
        result.save(os.path.join(syn_img_dir, '{}_{}_{}_{}.png'.format(str(fn).replace('.json', ''), generate_number, i, "syn")))
        
def concatenate_all_data(root, fn, train_data, generate_number):
    cat_img_dir = os.path.join(root, 'cat_img')
    syn_img_dir = os.path.join(root, 'syn_img')
    os.makedirs(cat_img_dir, exist_ok=True)
    img_list = []
    for i, train_data_i in enumerate(train_data):
        syn_img_path = os.path.join(syn_img_dir, '{}_{}_{}_{}.png'.format(str(fn).replace('.json', ''), generate_number, i, "syn"))
        syn_img = Image.open(syn_img_path)
        img_list.append(syn_img)
    
    max_width = max(img.width for img in img_list)
    padding_height = 10
    total_height = sum(img.height for img in img_list) + (len(img_list) - 1) * padding_height
    total_width = max_width

    result = Image.new('RGB', (total_width, total_height), color='white')
    y_offset = 0
    for img in img_list:
        result.paste(img, (0, y_offset))
        y_offset += img.height + padding_height

    result.save(os.path.join(cat_img_dir, '{}_{}_{}.png'.format(str(fn).replace('.json', ''), generate_number, "cat")))


def visualize_data(data_set, name, generate_number):
    root = 'result/vis/'
    os.makedirs(root, exist_ok=True)
    for i, data in enumerate(data_set):
        plot_data(data, root, name, generate_number, i)
    synthesize_data(root, name, data_set, generate_number)
    concatenate_all_data(root, name, data_set, generate_number)