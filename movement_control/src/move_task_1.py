#!/usr/bin/env python
from __future__ import print_function

import roslib; roslib.load_manifest('teleop_twist_keyboard')
import rospy

from geometry_msgs.msg import Twist

import sys, select, termios, tty

settings = termios.tcgetattr(sys.stdin)

msg = """
Reading from the keyboard  and Publishing to Twist.
---------------------------
Key Bindings:
w to move forward by 2 m/s
a to increase anticlockwise angular velocity by 0.5 each time
d to decrease anticlockwise angular velocity by 0.5 each time
q to quit
"""

def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key



def final():

    rospy.init_node('trial1',anonymous=True)
    pub=rospy.Publisher('/cmd_vel',Twist,queue_size=1)
    twist=Twist()
    rate=rospy.Rate(10)

    twist.linear.y = 0
    twist.linear.z = 0
    twist.angular.x = 0
    twist.angular.y = 0

    ang_inc=0.0

    try:
        print(msg)
        while(1):
            key=getKey()
            if key == 'w':
                print('w pressed\n')
                twist.linear.x=0.15
                twist.angular.z=0
                    
            elif key=='s':
                print('s pressed\n')
                twist.linear.x=0
                twist.angular.z=0

            elif key == 'a':
                print('a pressed\n')
                ang_inc=0.2
                twist.linear.x=0
                twist.angular.z=ang_inc        
            
	    elif key == 'd':
                print('d pressed\n')
                ang_inc=-0.2
                twist.linear.x=0
                twist.angular.z=ang_inc
	    
            elif key=='x':
                print('x pressed\n')
                
                twist.linear.x=-0.15
                twist.angular.z=0		
                    
            else:
                twist.linear.x = 0
                twist.angular.z = 0
                if (key == 'q'):
                    print('q pressed\n')
                    sys.exit()
            
            pub.publish(twist)
            rate.sleep()

    except Exception as e:
        print(e)

    finally:
        twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
        pub.publish(twist)

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)


if __name__ == '__main__':
    try:
        while not rospy.is_shutdown():
            final()
    except rospy.ROSInterruptException: pass





