import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap, math
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from Listeners import *

def main():
    controller = Leap.Controller()

    dial = Dial()
    drink = Drink()
    circle = Circle_Listener()
    swipe = Swipe_Listener()

    controller.add_listener(dial)
    controller.add_listener(drink)
    controller.add_listener(circle)
    controller.add_listener(swipe)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(dial)
        controller.remove_listener(drink)
        controller.remove_listener(circle)
        controller.remove_listener(swipe)


if __name__ == "__main__":
    main()