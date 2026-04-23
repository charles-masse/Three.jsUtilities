
import json, math
import maya.cmds as cmds

def orderPointsCCW(points):
    # https://stackoverflow.com/questions/73683410/sort-vertices-of-a-convex-polygon-in-clockwise-or-counter-clockwise
    lowest = min(points, key=lambda x:(x[2], x[0]))
    ordered_points = sorted(points, key=lambda x:math.atan2(x[2]-lowest[2], x[0]-lowest[0]) + 2 * math.pi)
    ordered_points.reverse()

    return ordered_points

def run():
    
    data = {}
    # NAVMESH
    navmesh = cmds.ls('navmesh')[0]
    if navmesh:
        data['navmesh'] = getNavMesh(navmesh)
    else:
        cmds.error("Coudn't find navmesh." )
    # SPAWN POINTS
    spawns = list(cmds.ls('spawn*', tr=1))
    if spawns:
        for s in spawns:
            data.setdefault('spawns', []).append(getSpawn(s))
    else:
        cmds.warning("Couldn't find spawn points, skipping." )
    # OBSTACLES
    obstacles = list(cmds.ls('obstacle*', tr=1))
    if obstacles:
        for o in obstacles:
            data.setdefault('obstacles', []).append(getObstacle(o))
    else:
        cmds.warning("Couldn't find obstacles, skipping." )
    # TRIGGERS
    triggers = list(cmds.ls('trigger*', tr=1))
    if triggers:
        for t in triggers:
            data.setdefault('triggers', []).append(getTrigger(t))
    else:
        cmds.warning("Couldn't find triggers, skipping." )
    # SAVE JSON
    saveFile(data)

def getPoints(vertices):

    points = []

    for v in cmds.ls(vertices, fl=1):
        points.append(cmds.xform(v, q=1, t=1, ws=1))

    return orderPointsCCW(points)

def getNavMesh(mesh):

    polys = []

    for f in cmds.filterExpand(f'{mesh}.f[*]', sm=34):

        vertices = cmds.polyListComponentConversion(f, ff=1, tv=1)
        polys.append(getPoints(vertices))
        
    return polys

def getObstacle(mesh):

    vertices = cmds.ls(f'{mesh}.vtx[*]', fl=1)

    return getPoints(vertices)

def getTrigger(mesh):

    vertices = cmds.ls(f'{mesh}.vtx[*]', fl=1)

    return {
        'points': getPoints(vertices),
        'type': 'stop',
    }

def getSpawn(loc):
    return cmds.xform(loc, q=1, t=1, ws=1)

def saveFile(data, path="C:/Users/charl/Documents/Scripts/portfolio/public/stage.json"):
    with open(path, "w") as file:
        json.dump(data, file, indent=4)

run()
