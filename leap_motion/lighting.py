import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap, math
import pygame

class swipeListener(Leap.Listener):

    maxFrameCount = 90
    frameList = []

    ultraviolet = (127, 0, 255)
    electricBlue = (0, 128, 255)
    sparkBlue = (60, 200, 255)
    moonlight = (0, 255, 255)
    daylight = (255, 255, 204)
    iceWhite = (255, 255, 255)
    amberGlow = (255, 255, 51)
    limelight = (0, 204, 0)
    sunset = (255, 128, 0)
    racingRed = (255, 0, 0)

    colours = [ultraviolet,electricBlue,sparkBlue,moonlight,daylight,iceWhite,amberGlow,limelight,sunset,racingRed]
    colourCounter = 0
    screen = pygame.display.set_mode((750, 500))

    def on_init(self, controller):
        print "Initialised"

    def on_connect(self, controller):
        print "Motion Sensor Connected"

    def on_disconnect(self, controller):
        print "Motion Sensor Disconnected"

    def on_exit(self, controller):
        print "Exit"

    def getMajorAxis(self,x,y,z):
        if x > y and x > z:
            
            return 'x'
        elif y > x and y > z:
            return 'y'
        elif z > x and z > y:
            
            return 'z' 

    def on_frame(self, controller):
        
        frame = controller.frame()
        swipeDirection = ""
        for hand in frame.hands:
            self.frameList.append(hand)

            start_x = self.frameList[0].palm_position.x
            end_x = self.frameList[-1].palm_position.x
            start_z = self.frameList[0].palm_position.z
            end_z = self.frameList[-1].palm_position.z
            difference = (end_x - start_x, end_z - start_z)

            absX = abs(difference[0])
            absZ = abs(difference[1])
            
            majorAxis = self.getMajorAxis(absX, 0, absZ)

            if majorAxis == 'x' and absX > 50:
                if difference[0] > 0:
                    swipeDirection = "Right"
                else:
                    swipeDirection = "Left"
            elif majorAxis == 'z' and absZ > 50:
                if difference[1] > 0:
                    swipeDirection = "Down"
                else:
                    swipeDirection = "Up"
            
            if len(self.frameList) > self.maxFrameCount:
                self.frameList = []

                if swipeDirection <> "":
                    print swipeDirection
                    if swipeDirection == "Right":
                        self.colourCounter +=1
                        if self.colourCounter>9:
                            self.colourCounter = 0
                        pygame.draw.rect(self.screen,self.colours[self.colourCounter], pygame.Rect(0, 80, 750, 300))
                    elif swipeDirection == "Left":
                        self.colourCounter -=1
                        if self.colourCounter <0:
                            self.colourCounter = 9
                        pygame.draw.rect(self.screen,self.colours[self.colourCounter], pygame.Rect(0, 80, 750, 300))

def main():
    pygame.init()
    background_colour = (255,255,255)
    (width, height) = (750,500)
    end_colour = (0,0,0)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Ambient Lighting")
    screen.fill(background_colour)

    size = (50,50)
    radius = 25
    pygame.draw.circle(screen, (0,0,0), (60, 50), 20)
    pygame.draw.circle(screen, (0,0,0), (280, 50), 20)
    pygame.draw.circle(screen, (0,0,0), (480, 50), 20)
    pygame.draw.circle(screen, (0,0,0), (670, 50), 20)
    pygame.draw.line(screen, (0,0,0), (60,50), (670,50), 10)


    pygame.draw.rect(screen, (127, 0, 255), pygame.Rect(30, 400, 60, 60))
    pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(100, 400, 60, 60))
    pygame.draw.rect(screen, (60, 200, 255), pygame.Rect(170, 400, 60, 60))
    pygame.draw.rect(screen, (0, 255, 255), pygame.Rect(240, 400, 60, 60))
    pygame.draw.rect(screen, (255, 255, 204), pygame.Rect(310, 400, 60, 60))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(380, 400, 60, 60))
    pygame.draw.rect(screen, (255, 255, 51), pygame.Rect(450, 400, 60, 60))
    pygame.draw.rect(screen, (0, 204, 0), pygame.Rect(520, 400, 60, 60))
    pygame.draw.rect(screen, (255, 128, 0), pygame.Rect(590, 400, 60, 60))
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(660, 400, 60, 60))

    
    
    listener = swipeListener()
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