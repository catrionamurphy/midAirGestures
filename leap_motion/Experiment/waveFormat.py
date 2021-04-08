import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap, math, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import pygame

class WaveListener(Leap.Listener):
    screen = pygame.display.set_mode((1300, 700))
    frequency = 4
    amplitude = 50
    speed = 1

    surface = pygame.Surface((1300, 700))
    surface.fill((0,0,0))

    def on_init(self, controller):
        print "Initialised"

    def on_connect(self, controller):
        print "Motion Sensor Connected"
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)

    def on_disconnect(self, controller):
        print "Motion Sensor Disconnected"

    def on_exit(self, controller):
        print "Exit"

    def wave(self, startPos, colour):
        for x in range(0,1300):
            y = int((startPos + self.amplitude*math.sin(self.frequency*((float(x)/750)* (2*math.pi)+ (self.speed*time.time())))))
            self.screen.set_at((x, y), (colour))
        #self.screen.blit(self.surface,(0,0))
        
        pygame.display.flip()

    def on_frame(self, controller):
        frame = controller.frame()
        #print "on frame"
        #pygame.draw.circle(self.screen, (255,0,0), (10,10), 10)

        extendedFingers = frame.fingers.extended()
        for gesture in frame.gestures():
            # Circle Data
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)
                
                if len(extendedFingers) == 5 or len(extendedFingers) == 4:
                    if circle.progress < 1:
                        print "Wave"
                        self.wave(250,(0,0,255))
                        self.wave(200,(0,80,150))
                        self.wave(300,(0,100,200))
                        self.wave(400,(30,80,200))
                        self.wave(450,(100,0,200))
                        self.wave(500,(250,250,250))

def main():
    pygame.init()
    pygame.mixer.init()
    background_colour = (0,0,0)
    (width, height) = (1300,700)

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Wave")
    
    screen.fill(background_colour)

    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')

    heading = pygame.image.load(os.path.join(img_folder, 'waveFormat.png')).convert()
    heading.set_colorkey((255,255,255))

    listener = WaveListener()
    controller = Leap.Controller()

    running = True
    while running:
        controller.add_listener(listener)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                controller.remove_listener(listener)
        screen.blit(heading, (400,-10))
        pygame.display.flip()
        

if __name__ == "__main__":
    main()