#!/usr/bin/env python
from std_msgs.msg import String
from rosgraph_msgs.msg import Log
import os
import re
import rospy
import time

def setup():
    global turtlobj
    turtlobj = open('turtle_col.txt', 'w')

setup()

class Turtle_Collions:
    def __init__(envior):
        # Nos suscribimos
        envior.sub = rospy.Subscriber("/rosout_agg", Log, envior.callback)
        # Inicializamos en 0's
        envior.prev_x = 0; envior.prev_y = 0; envior.count = 0

    def callback(envior, data):
        turtle_msg = data.msg
        # Cuando manda mensaje de choque
        if re.match(r'Oh no! I hit the wall!', turtle_msg):
            match = re.search(r'x=(.*), y=(.*)]', turtle_msg)
            # Obtenemos las codenadas en x & y
            x = float(match.group(1)); y = float(match.group(2))
            same_spot = (int(x) == envior.prev_x)and(int(y) == envior.prev_y)
            if not same_spot:
                # Mandamos el mensaje en la consola
                turtle_msg = 'Your turtle crashed in x = {0} and y = {1}'.format(x, y)
                turtlobj.write(turtle_msg+os.linesep)
                print(turtle_msg)
                envior.count += 1
            envior.prev_x = int(x); envior.prev_y = int(y)

if __name__ == '__main__':
    col = Turtle_Collions()
    try:
        rospy.init_node('turtle_collisions')
        rospy.spin()
        final_msg = "\n Total of colisions: {0}".format(col.count)
        turtlobj.write(final_msg)
        print(final_msg)
        time.sleep(5)
        turtlobj.close()
    except rospy.ROSInterruptException:
        turtlobj.close()
