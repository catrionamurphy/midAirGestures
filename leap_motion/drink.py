import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap, math
import pygame
import random as r

class drinkListener(Leap.Listener):
    frameList = []
    screen = pygame.display.set_mode((750, 500))

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

            pinky = hand.fingers.finger_type(4)[0]
            thumb = hand.fingers.finger_type(0)[0]
            index = hand.fingers.finger_type(1)[0]
            middle = hand.fingers.finger_type(2)[0]
            ring = hand.fingers.finger_type(3)[0]

            extendedFingers = hand.fingers.extended()


            

            if index not in extendedFingers and middle not in extendedFingers and ring not in extendedFingers:
                #print "DRANKS"
                if startAngle > 40 and endAngle < 10:
                    print "opeeeen"
                    champagne_cooler = "OPEN"
                    
            
            if len(self.frameList) > 200:
                self.frameList = []

def main():
    pygame.init()
    background_colour = (255,255,255)
    (width, height) = (750,500)
    end_colour = (0,0,0)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Open Champagne Cooler")
    screen.fill(background_colour)

    champagne = pygame.image.load('bottle.png')
    star = pygame.image.load('star.png')

    champagne = pygame.transform.scale(champagne, (350,350))
    champagne = pygame.transform.rotate(champagne,310)
    screen.blit(champagne, (110,10))
    
    star = pygame.transform.scale(star, (100, 100))
    screen.blit(star, (100,100))
    screen.blit(star, (600,100))
    screen.blit(star, (100,300))
    screen.blit(star, (450,400))
    screen.blit(star, (600,240))
    

    listener = drinkListener()
    controller = Leap.Controller()
    controller.add_listener(listener)

    # Set up all the features
    frame = controller.frame()
    previous = controller.frame(1)
    hands = frame.hands
    pointables = frame.pointables
    fingers = frame.fingers
    tools = frame.tools

    running = True

    while running:
        pygame.display.flip()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                controller.remove_listener(listener)


if __name__ == "__main__":
    main()