import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap, math
import pygame



class pulseListener(Leap.Listener):

    strengthList = []

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
            self.strengthList.append(hand.grab_strength)
            
            if len(self.strengthList) > 200:
                for i in range(len(self.strengthList)-1):
                    if self.strengthList[i] == 1 and self.strengthList[i+1] < 1:
                        self.counter += 1
                    else:
                        continue
                if self.counter == 1:
                    #print self.counter
                    print "pulse"
                elif self.counter == 2:
                    #print self.counter
                    print "pulse duo"
                else:
                    #print self.counter
                    print "too many"  
                self.strengthList = []   
                self.counter = 0

class Orb(pygame.sprite.Sprite):
    def __init__(self,img):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = img
        self.image_original.set_colorkey((0,0,0))
    #def update(self):




def main():
    pygame.init()
    pygame.mixer.init()
    background_colour = (255,255,255)
    (width, height) = (750,500)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pulse")
    
    screen.fill(background_colour)
    
    global all_sprites
    all_sprites = pygame.sprite.Group()

    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')

    pulseCircle = pygame.image.load(os.path.join(img_folder, 'glowCircle.png')).convert()
    pulseCircle1 = pygame.transform.scale(pulseCircle, (80,60))
    pulseCircle2 = pygame.transform.scale(pulseCircle, (80,60))

    pulses = [pulseCircle1, pulseCircle2]

    for circle in pulses:
        circle = Orb(circle)
        all_sprites.add(circle)


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