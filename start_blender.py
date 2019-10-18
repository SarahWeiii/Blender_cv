import os, sys, tempfile, shutil
import os.path as osp
import glob

# import blender configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR,'../'))
sys.path.append(os.path.join(BASE_DIR,'blcv'))

import blcv as bc

# Blender configs
render_code = 'blender_script.py'
blender_executable_path = 'D:/Install/Blender/blender.exe' #!! MODIFY if necessary
blank_blend_file_path = os.path.join(BASE_DIR, 'blank.blend') 


# set debug mode
debug_mode = 1
if debug_mode:
    io_redirect = ''
else:
    io_redirect = ' > ./logs'


if __name__ == '__main__':
    bc.call_blender(render_code, blender_executable_path, blank_blend_file_path, io_redirect)