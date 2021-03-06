import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap, math
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import pygame

class Massage(Leap.Listener):
    state_names = ["STATE_INVALID", "STATE_START", "STATE_UPDATE", "STATE_END"]
    frameList = []
    screen = pygame.display.set_mode((1300, 700))

    def on_init(self, controller):
        print "Initialised"

    def on_connect(self, controller):
        print "Motion Sensor Connected"
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)

    def on_disconnect(self, controller):
        print "Motion Sensor Disconnected"

    def on_exit(self, controller):
        print "Exit"

    def on_frame(self, controller):
        frame = controller.frame()
        pygame.draw.circle(self.screen, (255,0,0), (10,10), 10)
        
        for hand in frame.hands:
            pygame.draw.circle(self.screen, (0,255,0), (10,10), 10)
        

        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                print "circle detected"
                circle = CircleGesture(gesture)

                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                    clockwiseness = "clockwise"
                    massageOn = True
                else:
                    clockwiseness = "counter-clockwise"
                    massageOn = False
                print clockwiseness
            
            if circle.progress >= 0.8:
                if massageOn:
                    pygame.draw.circle(self.screen, (0,200,0), (650, 350), 220, 20)
                else:
                    pygame.draw.circle(self.screen, (255,0,0), (650, 350), 220, 20)
                    

def degreesToRadians(deg):
    return deg/180.0 * math.pi

# Draw an arc that is a portion of a circle.
# We pass in screen and color,
# followed by a tuple (x,y) that is the center of the circle, and the radius.
# Next comes the start and ending angle on the "unit circle" (0 to 360)
#  of the circle we want to draw, and finally the thickness in pixels

def drawCircleArc(screen,color,center,radius,startDeg,endDeg,thickness):
    (x,y) = center
    rect = (x-radius,y-radius,radius*2,radius*2)
    startRad = degreesToRadians(startDeg)
    endRad = degreesToRadians(endDeg)
   
    pygame.draw.arc(screen,color,rect,startRad,endRad,thickness)
    
def main():
    pygame.init()
    pygame.mixer.init()
    background_colour = (255,255,255)
    (width, height) = (1300,700)
    end_colour = (0,0,0)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Massage Chair")
    
    screen.fill(background_colour)
    
    pygame.draw.circle(screen, (0,0,0), (650, 350), 200, 10)
    drawCircleArc(screen, (0,0,0), (650, 350), 150, 120, 420,10)
    pygame.draw.line(screen, (0,0,0),(650,180),(650,280),20)

    global all_sprites
    all_sprites = pygame.sprite.Group()

    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')
    
    heading = pygame.image.load(os.path.join(img_folder, 'massage.png')).convert()
    heading.set_colorkey((255,255,255))

    listener = Massage()
    controller = Leap.Controller()

    running = True

    while running:
        controller.add_listener(listener)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                controller.remove_listener(listener)
        all_sprites.draw(screen)
        screen.blit(heading, (400,0))
        pygame.display.flip()

if __name__ == "__main__":
    main()