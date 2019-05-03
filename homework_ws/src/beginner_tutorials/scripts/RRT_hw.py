#!/usr/bin/env python
import math
import random
import matplotlib.pyplot as plt
import csv
test = True

def checkDis(point1,point2):
    dis = abs(math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2))
    return dis

def RRT(bounds,start,goal,obs):

    for i in obs:
        plt.plot(i[0],i[1],color = "k",marker = 's',linewidth=10.0,markersize = 15)
    print "hello"
    #unit of travel


    unit = 1.2#*(ideal/10)
    #tolerence
    tol = 1
    tolw = .7

    #create node list to hold nodes and information about them
    #{Node#,[NodeID,ParentNodeID,X,Y]}
    nodeKeeper = {}

    nodeKeeper[0] = [0,0,start[0],start[1]]

    CurrentNode = 0

    while abs(checkDis([nodeKeeper[CurrentNode][2],nodeKeeper[CurrentNode][3]],goal)) > tol:

        check = False
        while check == False:
            agl = math.atan2(goal[1]-start[1],goal[0]-start[0])

            m2 = math.tan(.05+agl)

            m3 = math.tan(agl-.05)

            incone = False

            #while incone ==False:
                #pick a random point with in the bounds of
            c1 = False
            c2 = False
            rndx = int(random.uniform(-bounds[0],bounds[0]+bounds[0]))
            rndy = int(random.uniform(-bounds[0],bounds[0]+bounds[0]))
            rndP = [rndx,rndy]
            #print rndP

                #if rndy< (m2*rndx+b) and rndy> (m3*rndx+b):
                    #incone = True


            incone = False





            #find closet point
            dummyDis = 999999999999999999
            for i in range(len(nodeKeeper)):
                buffer = checkDis(rndP,[nodeKeeper[i][2],nodeKeeper[i][3]])
                if buffer < dummyDis:
                    closetNode = i
                    dummyDis = buffer

            #create a new node 1 unit twords the direction of the random point from the closet nodes
            angle = math.atan2((rndy - nodeKeeper[closetNode][3]),(rndx - nodeKeeper[closetNode][2]))*(180/3.14)
            xa = (unit*math.cos(angle))
            ya = (unit*math.sin(angle))
            print xa
            print ya



            for i in range(len(obs)):
                if (nodeKeeper[closetNode][2]+xa) > (obs[i][0]-tolw) and nodeKeeper[closetNode][2]+xa < (obs[i][0]+tolw) and nodeKeeper[closetNode][3]+ya > (obs[i][1]-tolw) and nodeKeeper[closetNode][3]+ya < (obs[i][1]+tolw):
                    check = False
                    #print obs[i]
                    break
                elif nodeKeeper[closetNode][2]+xa < 0 or nodeKeeper[closetNode][2]+xa > bounds[0] or nodeKeeper[closetNode][3]+ya < 0 or nodeKeeper[closetNode][3]+ya > bounds[1]:
                    check = False
                    #print obs[i]
                    break

                check = True

        nodeKeeper[CurrentNode+1] = [CurrentNode+1,closetNode,int(nodeKeeper[closetNode][2]+xa),int(nodeKeeper[closetNode][3]+ya)]
        print (nodeKeeper[closetNode][2]+xa)
        print (nodeKeeper[closetNode][3]+ya)

        CurrentNode = CurrentNode+1

        #print to graph
        plt.axis([-1,bounds[0],-1,bounds[0]])
        plt.plot(nodeKeeper[CurrentNode][2],nodeKeeper[CurrentNode][3],'o', color = "b",linewidth=5.0)
        #plt.pause(.000000001)


    nodeKeeper[CurrentNode+1] = [CurrentNode+1,CurrentNode,goal[0],goal[1]]
    CurrentNode = CurrentNode+1
    print nodeKeeper

    id = 1

    pathx = []
    pathy = []
    full = []

    while id > 0:
        id = nodeKeeper[CurrentNode][0]
        pathx.append(nodeKeeper[CurrentNode][2])
        pathy.append(nodeKeeper[CurrentNode][3])
        full.append([nodeKeeper[CurrentNode][2],nodeKeeper[CurrentNode][3]])
        CurrentNode = nodeKeeper[CurrentNode][1]
    print full[::-1]
    full = full[::-1]
    plt.title("RRT")
    plt.plot(pathx,pathy,color = "red")
    plt.savefig("RRT.png",bbox_inches="tight")
    plt.show()

    new_list = zip(pathx, pathy)
    with open('RRThwp2.csv', 'wb+') as csvfile:
         filewriter = csv.writer(csvfile)
         filewriter.writerows(new_list)
    print "wrote"






    return full


#if test == True:
    #print "Running Test"
    #RRT([10,10],[0,0],[1,9],[[1,1], [4,4], [3,4], [5,0], [5,1], [0,7], [1,7], [2,7], [3,7]])
