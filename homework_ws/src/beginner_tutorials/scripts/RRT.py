#!/usr/bin/env python
import math
import random
import matplotlib.pyplot as plt
test = True

def checkDis(point1,point2):
    dis = abs(math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2))
    return dis

def RRT(bounds,start,goal,obs):

    #unit of travel
    unit = 1
    #tolerence
    tol = 2

    #create node list to hold nodes and information about them
    #{Node#,[NodeID,ParentNodeID,X,Y]}
    nodeKeeper = {}

    nodeKeeper[0] = [0,0,start[0],start[1]]

    CurrentNode = 0

    while checkDis([nodeKeeper[CurrentNode][2],nodeKeeper[CurrentNode][3]],goal] > tol:

        #pick a random point with in the bounds of
        rndx = random.randint(0,bounds[0])
        rndy = random.randint(0,bounds[0])
        rndP = [rndx,rndy]

        #find closet point
        dummyDis = 999999999999999999
        for i in range(len(nodeKeeper)):
            buffer = checkDis(rndP,[nodeKeeper[i][2],nodeKeeper[i][3]])
            if buffer < dummyDis:
                closetNode = i
                dummyDis = buffer

        #create a new node 1 unit twords the direction of the random point from the closet nodes
        angle = atan2((nodeKeeper[closetNode][3]-rndy),(nodeKeeper[closetNode][2]-rndx)*(3.14/180)
        xadd = unit*cos(angle)
        yadd = unit*sin(angle)
        nodeKeeper[CurrentNode+1] = [CurrentNode+1,nodeKeeper[closetNode][0],nodeKeeper[closetNode][2]+xadd,nodeKeeper[closetNode][3]+yadd]]

        CurrentNode = CurrentNode+1

    nodeKeeper[CurrentNode+1] = [CurrentNode+1,CurrentNode,]






    return





if test == True:
