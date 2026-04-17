import json

import math

import maya.cmds as cmds
# https://stackoverflow.com/questions/73683410/sort-vertices-of-a-convex-polygon-in-clockwise-or-counter-clockwise
def orderVerticesCCW(polygon):
    
    lowest = min(polygon, key= lambda x:(x[2], x[0]))
    vertices = sorted(polygon, key=lambda x:math.atan2(x[2]-lowest[2], x[0]-lowest[0]) + 2 * math.pi)
    vertices.reverse()

    return vertices

selection = cmds.ls(sl=1)[0]

data = []

faces = cmds.filterExpand(f'{selection}.f[*]', selectionMask=34)
for f in faces:

    polygon = []

    vertices = cmds.polyListComponentConversion(f, fromFace=True, toVertex=True)
    for v in cmds.ls(vertices, flatten=True):
        polygon.append(cmds.xform(v, q=1, t=1))

    data.append(orderVerticesCCW(polygon))

with open("C:/Users/charl/Documents/Scripts/portfolio/public/data.json", "w") as file:
    json.dump({'polygons': data}, file)