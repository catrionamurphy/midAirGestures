import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap, math
import pygame

class adjustTemp(Leap.Listener):
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




           
def main():
    pygame.init()
    background_colour = (255,255,255)
    (width, height) = (750,500)
    end_colour = (0,0,0)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Open Champagne Cooler")
    screen.fill(background_colour)

    
    pygame.draw.circle(screen, (0,0,0), (375, 250), 100, 10)
    pygame.draw.circle(screen, (51, 153, 255), (375, 250), 110, 15)


    pygame.draw.polygon(screen, (0,0,0), [(250,270),(330,250),(250, 230)])




    listener = adjustTemp()
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