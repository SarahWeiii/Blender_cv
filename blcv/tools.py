#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import bpy
import sys
import math
import random
import numpy as np

class BcObject:
    def __init__(self, id):
        self.obj = bpy.data.objects[id]

    def destroy(self):
        self.obj.select = True
        bpy.ops.object.delete() 

    def set_loc(self, x, y, z):
        self.obj.location[0] = x
        self.obj.location[1] = y 
        self.obj.location[2] = z

    def get_loc(self):
        return self.obj.location[0], self.obj.location[1], self.obj.location[2]

    def set_rot(self, x, y, z, w=None, mode='XYZ'):
        self.obj.rotation_mode = mode
        if mode == 'AXIS_ANGLE':
            if w is None:
                print('input error: w')
            else:
                self.obj.rotation_axis_angle[0] = w / 180 * math.pi
                self.obj.rotation_axis_angle[1] = x
                self.obj.rotation_axis_angle[2] = y
                self.obj.rotation_axis_angle[3] = z
        elif mode == 'QUATERNION':
            if w is None:
                print('input error: w')
            else:
                self.obj.rotation_quaternion[0] = w
                self.obj.rotation_quaternion[1] = x
                self.obj.rotation_quaternion[2] = y
                self.obj.rotation_quaternion[3] = z
        else:
            self.obj.rotation_euler[0] = x / 180 * math.pi
            self.obj.rotation_euler[1] = y / 180 * math.pi
            self.obj.rotation_euler[2] = z / 180 * math.pi

    def get_rot(self, mode='XYZ', w=None):
        self.obj.rotation_mode = mode
        if mode == 'AXIS_ANGLE':
            return self.obj.rotation_axis_angle[0] / math.pi * 180, \
                self.obj.rotation_axis_angle[1], \
                self.obj.rotation_axis_angle[2], \
                self.obj.rotation_axis_angle[3]
        elif mode == 'QUATERNION':
            return self.obj.rotation_quaternion[0], \
                self.obj.rotation_quaternion[1], \
                self.obj.rotation_quaternion[2], \
                self.obj.rotation_quaternion[3]
        else:
            return self.obj.rotation_euler[0] / math.pi * 180, \
                self.obj.rotation_euler[1] / math.pi * 180, \
                self.obj.rotation_euler[2] / math.pi * 180

    def set_scale(self, x, y, z):
        self.obj.scale[0] = x
        self.obj.scale[1] = y 
        self.obj.scale[2] = z
    
    def get_scale(self):
        return self.obj.scale[0], self.obj.scale[1], self.obj.scale[2]


class BcCamera(BcObject):
    def __init__(self, id):
        super().__init__(id)

    def _obj_centened_camera_pos(self, dist, azimuth_deg, elevation_deg):
        phi = float(elevation_deg) / 180 * math.pi
        theta = float(azimuth_deg) / 180 * math.pi
        x = (dist * math.cos(theta) * math.cos(phi))
        y = (dist * math.sin(theta) * math.cos(phi))
        z = (dist * math.sin(phi))
        return x, y, z

    def _quaternionFromYawPitchRoll(self, yaw, pitch, roll):
        c1 = math.cos(yaw / 2.0)
        c2 = math.cos(pitch / 2.0)
        c3 = math.cos(roll / 2.0)    
        s1 = math.sin(yaw / 2.0)
        s2 = math.sin(pitch / 2.0)
        s3 = math.sin(roll / 2.0)    
        q1 = c1 * c2 * c3 + s1 * s2 * s3
        q2 = c1 * c2 * s3 - s1 * s2 * c3
        q3 = c1 * s2 * c3 + s1 * c2 * s3
        q4 = s1 * c2 * c3 - c1 * s2 * s3
        return (q1, q2, q3, q4)


    def _camPosToQuaternion(self, cx, cy, cz):
        q1a = 0
        q1b = 0
        q1c = math.sqrt(2) / 2
        q1d = math.sqrt(2) / 2
        camDist = math.sqrt(cx * cx + cy * cy + cz * cz)
        cx = cx / camDist
        cy = cy / camDist
        cz = cz / camDist    
        t = math.sqrt(cx * cx + cy * cy) 
        tx = cx / t
        ty = cy / t
        yaw = math.acos(ty)
        if tx > 0:
            yaw = 2 * math.pi - yaw
        pitch = 0
        tmp = min(max(tx*cx + ty*cy, -1),1)
        #roll = math.acos(tx * cx + ty * cy)
        roll = math.acos(tmp)
        if cz < 0:
            roll = -roll    
        q2a, q2b, q2c, q2d = self._quaternionFromYawPitchRoll(yaw, pitch, roll)    
        q1 = q1a * q2a - q1b * q2b - q1c * q2c - q1d * q2d
        q2 = q1b * q2a + q1a * q2b + q1d * q2c - q1c * q2d
        q3 = q1c * q2a - q1d * q2b + q1a * q2c + q1b * q2d
        q4 = q1d * q2a + q1c * q2b - q1b * q2c + q1a * q2d
        return (q1, q2, q3, q4)

    def _camRotQuaternion(self, cx, cy, cz, theta): 
        theta = theta / 180.0 * math.pi
        camDist = math.sqrt(cx * cx + cy * cy + cz * cz)
        cx = -cx / camDist
        cy = -cy / camDist
        cz = -cz / camDist
        q1 = math.cos(theta * 0.5)
        q2 = -cx * math.sin(theta * 0.5)
        q3 = -cy * math.sin(theta * 0.5)
        q4 = -cz * math.sin(theta * 0.5)
        return (q1, q2, q3, q4)

    def _quaternionProduct(self, qx, qy): 
        a = qx[0]
        b = qx[1]
        c = qx[2]
        d = qx[3]
        e = qy[0]
        f = qy[1]
        g = qy[2]
        h = qy[3]
        q1 = a * e - b * f - c * g - d * h
        q2 = a * f + b * e + c * h - d * g
        q3 = a * g - b * h + c * e + d * f
        q4 = a * h + b * g - c * f + d * e    
        return (q1, q2, q3, q4)

    def set_camera_to_center(self, dist, azimuth_deg, elevation_deg, theta_deg):
        cx, cy, cz = self._obj_centened_camera_pos(dist, azimuth_deg, elevation_deg)
        q1 = self._camPosToQuaternion(cx, cy, cz)
        q2 = self._camRotQuaternion(cx, cy, cz, theta_deg)
        q = self._quaternionProduct(q2, q1)
        self.set_loc(cx, cy, cz)
        self.set_rot(q[1], q[2], q[3], q[0], 'QUATERNION')

class BcScene:
    def __init__(self):
        self.obj = bpy.data.scenes['Scene']

    def set_render_mode(self, mode):
        bpy.context.scene.render.alpha_mode = mode

    def get_img(self, filepath):
        self.obj.render.filepath = filepath
        bpy.ops.render.render( write_still=True )


def import_obj(shape_file):
    bpy.ops.import_scene.obj(filepath=shape_file, split_mode='OFF') 
    return bpy.context.selected_objects[0].name
        




        
