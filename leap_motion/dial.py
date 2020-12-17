import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap, math
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import pygame


class Dial(Leap.Listener):

    frameList = []

    def on_init(self, controller):
        print "Initialised"

    def on_connect(self, controller):
        print "Motion Sensor Connected"

    def on_disconnect(self, controller):
        print "Motion Sensor Disconnected"

    def on_exit(self, controller):
        print "Exit"
    
    def on_frame(self, controller):
        frame = controller.frame()

        for hand in frame.hands:
            self.frameList.append(hand)

            startAngle = self.frameList[0].direction.yaw
            startAngle = startAngle * Leap.RAD_TO_DEG
            endAngle = self.frameList[-1].direction.yaw
            endAngle = endAngle * Leap.RAD_TO_DEG
            
            angles = (startAngle,endAngle)

            difference_angles = endAngle-startAngle

            if len(self.frameList) > self.maxFrameCount:
                # reset number of frames
                self.frameList = []

                # AIR CONDITIONING
                if difference_angles > 0:
                    temperature = "up"
                elif difference_angles < 0:
                    temperature = "down"
                else:
                    temperature = "same"

                if temperature == "up" and self.actualTemp < 32:
                    if difference_angles < 20:
                        self.actualTemp += 1
                    elif difference_angles >= 20 and difference_angles < 40:
                        self.actualTemp += 2
                    elif difference_angles >= 40 and difference_angles < 80:
                        self.actualTemp += 3
                    elif difference_angles >= 80:
                        self.actualTemp += 5
                elif temperature == "down" and self.actualTemp > 2:
                    if difference_angles > -20:
                        self.actualTemp -= 1
                    elif difference_angles <= -20 and difference_angles > -40:
                        self.actualTemp -= 2
                    elif difference_angles <= -40 and difference_angles > -80:
                        self.actualTemp -= 3
                    elif difference_angles <= -80:
                        self.actualTemp -= 5
                else:
                    continue




def main():
    listener = Dial()
    controller = Leap.Controller()
    

    running = True
    while running:
        controller.add_listener(listener)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                controller.remove_listener(listener)
        screen.fill((0,0,0))
        pygame.display.flip()

    """
    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)
    """

if __name__ == "__main__":
    main()