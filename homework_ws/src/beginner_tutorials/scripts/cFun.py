#!/usr/bin/env python
import math

# This function will generate a dubins curve that passes through a given set of
# waypoints and return a list of points for the dubin curve.
# a waypoint =  [x, y, heading in degrees]
def dubinsGen(wayPoints, turning_radius, step_size):
    wpm = []
    for i in range(len(WayPoints)):
        q0 = wayPoints[i]
        try:
            q1 = wayPoints[i+1]
        except:
            break
        path = dubins.shortest_path(q0, q1, turning_radius)
        configurations, _ = path.sample_many(step_size)
        for i in range(len(configurations)):
            wpm.append(configurations[i])
    return wpm

def checkDis(point1,point2):
    dis = abs(math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2))
    return dis

def checkLoc(obstacles, gridBond, currentLoc):
    st = "Valid"
    if currentLoc[0] < 0 or currentLoc[0] > gridBond[0] or currentLoc[1] < 0 or currentLoc[1] > gridBond[1]:
        st =  "Invalid"

    for i in range(len(obstacles)):
        if obstacles[i] == currentLoc:
            st = "Invalid"
            break
    print st

def nodeIndex(node, bounds):
    #                   y                  x
    index = bounds*node[1] - (bounds-node[0])
    return index

def nodes(bounds):
    for j in range(bounds):
        for k in range(bounds):
            dic[nodeIndex((k+1,j+1),bounds)] = [k+1,j+1,0,0,0,0,0]
    return dic

def createNodes(bounds):
    NodeKeeper = []
    for i in range(bounds):
        for j in range(bounds):
            x = j+1
            y = i+1
            index = nodeIndex([x,y],bounds)
            N = node
            NodeKeeper.append()
        return NodeKeeper

#the starting location, goal location, grid information, and obstacle list.
def Dijkstra(Start,goal,bounds,obst):
    keeper = {}
    keeper = nodes(bounds)
    print keeper
    startIndex = nodeIndex(Start,bounds)
    keeper[startIndex].append(0)
    print keeper[startIndex]
    keeper[startIndex][3] = 1
    uv = True
    currentnode = startIndex

    while uv == True:
        for i in range(bounds*bounds):
            if keeper[i+1][2] == 0:
                break
            else:
                uv = False

        #determin cost brute force method
        for i in range(bounds*bounds):
            keeper[i+1][2] = checkDis(keeper[currentnode],keeper[i+1])
        #find node with lowest cost
        for i in range(bounds*bounds):
            if keeper[i+1][2] == 1 and keeper[i+1][3] == 0:
                oldnode = currentnode
                currentnode = keeper[i+1]
                currentnode[4] = nodeIndex(oldnode,bounds)
                break












test = True
if test == True:

    X = checkDis([2,1],[3,2])
    print (X)

    obs = [(1,1), (4,4), (3,4), (5,0), (5,1), (0,7), (1,7), (2,7), (3,7)]
    currLoc = (5,1)
    grid = [2,2]
    print len(obs)

    checkLoc(obs, grid, currLoc)

    nodeIndex([3,3],10)

    dic = {}
    nodes(3)

    Dijkstra((3,3),(4,4),10,11)
