#!/usr/bin/env python

# This function will generate a dubins curve passing the through a given set of waypoints
# a waypoint =  [x, y, heading in degrees]
def dubinsGen(wayPoints, turning_radius, step_size)
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
