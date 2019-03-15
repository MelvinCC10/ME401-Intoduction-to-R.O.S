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

def checkLoc(obstacles, bounds, currentLoc):
    st = True
    if currentLoc[0] < 0 or currentLoc[0] > bounds or currentLoc[1] < 0 or currentLoc[1] > bounds:
        st =  False

    for i in range(len(obstacles)):
        if obstacles[i] == currentLoc:
            st = False
            break
    return st

def nodeIndex(node, bounds):
    #                   y                  x
    index = bounds*node[1] - (bounds-node[0])
    return index

def nodes(bounds):
    dic = {}
    for j in range(bounds):
        for k in range(bounds):
                                        #  [x,y,cost,visted,parentID,current]
            dic[nodeIndex((k+1,j+1),bounds)] = [k,j,0,0,0,0,0,0]
    return dic

def createNodes(bounds):
    nodeKeeper = nodes(bounds)
    return nodeKeeper

def findShortPath(bounds,start,goal,obs):
    nodeKeeper = createNodes(bounds)
    startIndex = nodeIndex((start[0]+1,start[1]+1),bounds)
    current = nodeKeeper[startIndex]
    currentIndex = startIndex

    x= True
    while x == True:

        templist = []#keep distence values of nodes// resets ever time we move to a new node

        nib = [(currentIndex+bounds),(currentIndex-bounds), (currentIndex+1),(currentIndex-1),(currentIndex+bounds+1),(currentIndex+bounds-1),(currentIndex-bounds+1),(currentIndex-bounds-1)]

        #cornor conditions
        #if currentIndex == 1 or currentIndex == (bounds*bounds) or currentIndex == (bounds*bounds - (bounds-1)) or currentIndex == 1 + (bounds-1):

        #edge and cornor conditions
        if (currentIndex % bounds) == 1 and  currentIndex + bounds > (bounds*bounds):
            nib.remove((currentIndex+bounds-1))
            nib.remove((currentIndex-bounds-1))
            nib.remove((currentIndex-1))
            nib.remove((currentIndex+bounds))
            nib.remove((currentIndex+bounds+1))
        elif (currentIndex % bounds) == 1 and currentIndex - bounds <0:
            nib.remove((currentIndex+bounds-1))
            nib.remove((currentIndex-bounds-1))
            nib.remove((currentIndex-1))
            nib.remove((currentIndex-bounds))
            nib.remove((currentIndex-bounds+1))
        elif currentIndex % bounds == 0 and currentIndex + bounds > (bounds*bounds):
            nib.remove((currentIndex+bounds+1))
            nib.remove((currentIndex-bounds+1))
            nib.remove((currentIndex+1))
            nib.remove((currentIndex+bounds))
            nib.remove((currentIndex+bounds-1))
        elif currentIndex % bounds == 0 and currentIndex - bounds <=0:
            nib.remove((currentIndex+bounds+1))
            nib.remove((currentIndex-bounds+1))
            nib.remove((currentIndex+1))
            nib.remove((currentIndex-bounds))
            nib.remove((currentIndex-bounds-1))
        else:
            if (currentIndex % bounds) == 1:
                nib.remove((currentIndex+bounds-1))
                nib.remove((currentIndex-bounds-1))
                nib.remove((currentIndex-1))
            if currentIndex % bounds == 0:
                nib.remove((currentIndex+bounds+1))
                nib.remove((currentIndex-bounds+1))
                nib.remove((currentIndex+1))
            if currentIndex + bounds > (bounds*bounds):
                nib.remove((currentIndex+bounds))
                nib.remove((currentIndex+bounds+1))
                nib.remove((currentIndex+bounds-1))
            if currentIndex - bounds <0:
                nib.remove((currentIndex-bounds))
                nib.remove((currentIndex-bounds+1))
                nib.remove((currentIndex-bounds-1))

        nibpass = []
        print nib

        if current[3] == 1:
            for j in range(len(nodeKeeper)):
                if nodeKeeper[j+1][3] == 0:
                    current = nodeKeeper[j+1]
                    currentIndex = nodeIndex((current[0]+1,current[1]+1),bounds)
                    smallIndex = currentIndex

        current[3] = 1 #marking current as visted





        for i in nib:#range((bounds*bounds)):
            if nodeKeeper[i][3] == 0:#if unvisted
                if (checkDis(nodeKeeper[i],current)+current[2]) < (nodeKeeper[i][2]) or nodeKeeper[i][2] == 0:
                    nodeKeeper[i][2] = checkDis(nodeKeeper[i],current) + current[2]
                    nodeKeeper[i][4] =currentIndex
                templist.append([(i),nodeKeeper[i][2]])

        print "--------------------------------------------------------"
        print templist
        print nodeKeeper
        currentSmall = 999999999999999999*99 #some random large value
        for i in range(len(templist)): #find shortest_path
            if templist[i][1] < currentSmall:
                smallIndex = templist[i][0]
                currentSmall = templist[i][1]
        print smallIndex
        print "--------------------------------------------------------"
        current = nodeKeeper[smallIndex]
        currentIndex = smallIndex

        for j in range(len(nodeKeeper)):
            x = False
            if nodeKeeper[j+1][3] == 0:
                x = True


    #find short path
    pathIndex = nodeIndex((goal[0]+1,goal[1]+1),bounds)
    path = []
    while pathIndex != startIndex:
        print pathIndex
        path.append(pathIndex)
        pathIndex = nodeKeeper[pathIndex][4]
    path.append(pathIndex)
    path.reverse()
    print "pathIndex"
    print path





#the starting location, goal location, grid information, and obstacle list.
def dDijkstra(Start,goal,bounds,obst):
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

    findShortPath(5,[0,0],[3,4],'none')
