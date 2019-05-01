#!/usr/bin/env python
import math
import matplotlib.pyplot as plt
import numpy as np
import csv


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

def checkLoc(obs, bounds, currentLoc):
    st = True

    for i in range(len(obs)):
        if obs[i] == [currentLoc[0],currentLoc[1]]:

            st = False

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
    plt.plot(start[0],start[1],'o',marker = "D" ,color = 'g',linewidth=5.0)
    plt.plot(goal[0],goal[1],'o',marker = "D", color = 'r',linewidth=5.0)

    for i in obs:
        plt.plot(i[0],i[1],color = "k",marker = 's',linewidth=10.0,markersize = 20)
    #black list obstacles
    for i in range(len(obs)):
        indx = nodeIndex((obs[i][0]+1,obs[i][1]+1),bounds)
        nodeKeeper[indx][3] = 1

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
        for i in nib:
            if checkLoc(obs, bounds, nodeKeeper[i]) == False:
                nib.remove(i)
                print "removed"
                print i


        print nib
        print current

        if current[3] == 1:
            for j in range(len(nodeKeeper)):
                print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXxx"
                print nodeKeeper[j+1][3]
                print nodeKeeper[j+1][2]
                tempnode = nodeKeeper[j+1]
                print j+1
                if tempnode[3] == 0 and tempnode[2] != 0:
                    current = tempnode
                    currentIndex = nodeIndex((tempnode[0]+1,tempnode[1]+1),bounds)
                    smallIndex = currentIndex
                    print "Xoooo"
                    break


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
                break

        plt.axis([-1,bounds,-1,bounds])
        #plt.plot(current[0],current[1],'o', color = "w",linewidth=5.0)
        #plt.pause(.01)


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

    vx = []
    vy = []
    for i in path:
        vx.append(nodeKeeper[i][0])
        vy.append(nodeKeeper[i][1])
    plt.plot(vx,vy,color = "blue")
    plt.show()

    xo = start[0]
    yo = start[1]
    theta = 0
    waypoints = [[xo,yo,theta]]
    for i in path:
        x = nodeKeeper[i][0]
        y = nodeKeeper[i][1]
        theta = math.atan2((y-yo),(x-xo))
        waypoints.append([x,y,theta])

    print waypoints
    return waypoints




#the starting location, goal location, grid information, and obstacle list.
#test = True
#if test == True:

    #findShortPath(10,[0,0],[1,9],[[8,9]])
