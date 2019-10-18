import os, sys, tempfile, shutil
import os.path as osp
import glob

name = "blcv"

# import blender configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR,'../'))

def call_blender(render_code, blender_executable_path, blank_blend_file_path, io_redirect='', background=True):
    blank_file = osp.join(blank_blend_file_path)

    if background:
        render_cmd = '{:s} {:s} --background --python {:s}'.format(
            blender_executable_path, 
            blank_file, 
            render_code
        )
    else:
        render_cmd = '{:s} {:s} --python {:s}'.format(
            blender_executable_path, 
            blank_file, 
            render_code
        )
    render_cmd = render_cmd.replace('\\', '/')
    try:
        os.system('{:s} {:s}'.format(render_cmd, io_redirect))
    except Exception as e:
        print(e)
        print('render failed. render_cmd: {:s}'.format(render_cmd))