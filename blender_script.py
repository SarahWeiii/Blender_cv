#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import bpy
import sys
import math
import random
import numpy as np
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dep_paths = [
	BASE_DIR,
	os.path.join(BASE_DIR, 'blcv')
]
for p in dep_paths:
	sys.path.append(p)


import blcv.tools as bct

def get_images_for_model(model_dir, view_params, save_img_dir):
    syn_images_folder = os.path.join(save_img_dir, model_dir.split('/')[-2])
    
    if not os.path.exists(syn_images_folder):
        os.makedirs(syn_images_folder)

    model_id = bct.import_obj(model_dir)
    model = bct.BcObject(model_id)

    scene = bct.BcScene()
    scene.set_render_mode('TRANSPARENT')

    cam = bct.BcCamera('Camera')

    x, y, z = model.get_loc()
    model.set_loc(x+0.5, y, z)
    x, y, z = model.get_rot()
    model.set_rot(x, y+30, z)
    x, y, z = model.get_scale()
    model.set_scale(x, y, z)

    for param in view_params:
        azimuth_deg = param[0]
        elevation_deg = param[1]
        theta_deg = param[2]
        dist = param[3]

        cam.set_camera_to_center(dist, azimuth_deg, elevation_deg, theta_deg)

        theta_deg = (-1*theta_deg)%360
        syn_image_file = './{:03d}_{:03d}_{:03d}_{:03d}.png'.format(round(azimuth_deg), round(elevation_deg), round(theta_deg), round(dist))
        scene.get_img(os.path.join(syn_images_folder, syn_image_file))

    model.destroy()


def main():
    model_dir = 'examples/1/model.obj'
    models = glob.glob(model_dir)
    view_params = [[0, 30, 0, 2.0], [45, 30, 0, 2.0], [90, 30, 0, 2.0], [135, 30, 0, 2.0], [180, 30, 0, 2.0],
                    [225, 30, 0, 2.0], [270, 30, 0, 2.0], [315, 30, 0, 2.0], [0, 60, 0, 2.0], [45, 60, 0, 2.0],
                    [90, 60, 0, 2.0], [135, 60, 0, 2.0], [180, 60, 0, 2.0], [225, 60, 0, 2.0], [270, 60, 0, 2.0],
                    [315, 60, 0, 2.0]]

    for model in models:
        get_images_for_model(model.replace('\\', '/'), view_params, os.path.join(BASE_DIR, 'images'))

if __name__ == '__main__':
    main()

    