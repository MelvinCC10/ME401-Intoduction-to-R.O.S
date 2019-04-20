#!/usr/bin/env python
import math
import random
import matplotlib.pyplot as plt
test = True

def checkDis(point1,point2):
    dis = abs(math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2))
    return dis

def RRT(bounds,start,goal,obs):

    print "hello"
    #unit of travel
    unit = 1
    #tolerence
    tol = 2

    #create node list to hold nodes and information about them
    #{Node#,[NodeID,ParentNodeID,X,Y]}
    nodeKeeper = {}

    nodeKeeper[0] = [0,0,start[0],start[1]]

    CurrentNode = 0

    while abs(checkDis([nodeKeeper[CurrentNode][2],nodeKeeper[CurrentNode][3]],goal)) > tol:

        #pick a random point with in the bounds of
        rndx = random.uniform(0,bounds[0])
        rndy = random.uniform(0,bounds[0])
        rndP = [rndx,rndy]


        #find closet point
        dummyDis = 999999999999999999
        for i in range(len(nodeKeeper)):
            buffer = checkDis(rndP,[nodeKeeper[i][2],nodeKeeper[i][3]])
            if buffer < dummyDis:
                closetNode = i
                dummyDis = buffer

        #create a new node 1 unit twords the direction of the random point from the closet nodes
        angle = math.atan2((nodeKeeper[closetNode][3]-rndy),(nodeKeeper[closetNode][2]-rndx))*(180/3.14)
        xa = unit*math.cos(angle)
        ya = unit*math.sin(angle)
        print angle
        print xa
        print ya

        nodeKeeper[CurrentNode+1] = [CurrentNode+1,closetNode,nodeKeeper[closetNode][2]+xa,nodeKeeper[closetNode][3]+ya]

        CurrentNode = CurrentNode+1

        #print to graph
        plt.axis([-1,bounds[0],-1,bounds[0]])
        plt.plot(nodeKeeper[CurrentNode][2],nodeKeeper[CurrentNode][3],'o', color = "b",linewidth=5.0)
        plt.pause(.05)


    nodeKeeper[CurrentNode+1] = [CurrentNode+1,CurrentNode,goal[0],goal[1]]
    CurrentNode = CurrentNode+1
    print nodeKeeper

    id = 1

    pathx = []
    pathy = []

    while id > 0:
        id = nodeKeeper[CurrentNode][0]
        pathx.append(nodeKeeper[CurrentNode][2])
        pathy.append(nodeKeeper[CurrentNode][3])
        CurrentNode = nodeKeeper[CurrentNode][1]


    plt.plot(pathx,pathy,color = "red")
    plt.show()






    return


if test == True:
    print "Running Test"
    RRT([10,10],[0,0],[9,9],[[8,9]])
