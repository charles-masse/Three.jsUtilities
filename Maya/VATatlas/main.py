
import random, webbrowser

from PIL import Image

import maya.cmds as cmds

SAVE_PATH = 'D:/Desktop/Scripts/portfolio/public/VAT/animations.png'

def lerpFactor(a, b, value):
    return (value - a) / (b - a)

def generateTexture(data, width, height):

    img = Image.new('RGB', (width, height))
    img.putdata(data)

    return img

def run():

    vertex_animation = []

    selected_mesh = cmds.ls('anim', typ='transform')[0]
    selected_mesh_vertices = cmds.ls(selected_mesh + ".vtx[*]", fl=1)

    start_frame = int(cmds.playbackOptions(q=1, ast=1))
    end_frame = int(cmds.playbackOptions(q=1, aet=1))

    for frame in range(start_frame, end_frame + 1):
        cmds.currentTime(frame, e=1)

        frame_vertex_positions = []
        for vertex in selected_mesh_vertices:
            bind_position = cmds.xform('bind.' + vertex.split('.')[-1], q=1, t=1, ws=1)
            vertex_position = cmds.xform(vertex, q=1, t=1, ws=1)
            frame_vertex_positions.extend([a - b for a, b in zip(vertex_position, bind_position)])

        vertex_animation.extend(frame_vertex_positions)

    min_transform = min(vertex_animation)
    max_transform = max(vertex_animation)

    print(max_transform - min_transform, lerpFactor(min_transform, max_transform, 0))

    vertex_animation_normalized = [int(lerpFactor(min_transform, max_transform, transform) * 255) for transform in vertex_animation]
    
    vertex_animation_vec3 = []
    for i in range(0, len(vertex_animation_normalized), 3):
        vertex_animation_vec3.append(tuple(vertex_animation_normalized[i:i+3]))

    return generateTexture(vertex_animation_vec3, len(selected_mesh_vertices), end_frame - start_frame + 1)

run().save(SAVE_PATH)
webbrowser.open(SAVE_PATH)
