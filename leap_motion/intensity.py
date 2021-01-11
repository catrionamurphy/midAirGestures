import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap, math
import pygame

class IntensityListener(Leap.Listener):
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
             extendedFingers = frame.fingers.extended()
            noFingers = len(extendedFingers)
            if noFingers == 1:
                intensityLevel = 1
            elif noFingers == 2:
                intensityLevel =2
            elif noFingers == 3:
                intensityLevel = 3
            elif noFingers == 4:
                intensityLevel = 4
            elif noFingers == 5:
                intensityLevel = 5



def main():
    pygame.init()
    pygame.mixer.init()
    background_colour = (255,255,255)
    (width, height) = (750,500)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Intensity Level")

    screen.fill(background_colour)
    
    global all_sprites
    all_sprites = pygame.sprite.Group()

    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')

    global listener
    listener = pulseListener()
    controller = Leap.Controller()

    running = True

    while running:
        controller.add_listener(listener)

        all_sprites.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                controller.remove_listener(listener)


if __name__ == "__main__":
    main()