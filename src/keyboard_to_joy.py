#!/usr/bin/env python

import sys, select, termios, tty
import rospy
from sensor_msgs.msg import Joy

msg = '''
Simulate a joypad:
        w     
   a    s    d
   1    2    3
CTRL-C to quit
'''

axesBindings = {'w': (1, 1), 'a': (0, 1), 's': (1, -1), 'd': (0,-1)}
buttonsBindings = {'1': 0, '2': 1, '3': 2}


def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


if __name__ == '__main__':
    settings = termios.tcgetattr(sys.stdin)
    rospy.init_node('keyboard_to_joy')
    pub = rospy.Publisher('kbjoy', Joy, queue_size=1)

    joy_msg = Joy()
    joy_msg.axes = [0.0, 0.0]
    joy_msg.buttons = [0.0, 0.0, 0.0]

    try:
        print msg
        while True:
            key = getKey()
            if key == '\x03':
                break
            if key in axesBindings:
                joy_msg.axes[axesBindings[key][0]] = axesBindings[key][1]
            elif key in buttonsBindings:
                joy_msg.buttons[buttonsBindings[key]] = 1
            else:
                joy_msg.axes = [0.0, 0.0]
                joy_msg.buttons = [0.0, 0.0, 0.0]
            pub.publish(joy_msg)
    except Exception as e:
        print e
    finally:
        pub.publish(joy_msg)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
