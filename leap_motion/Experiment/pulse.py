import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap, math
import pygame

class pulseListener(Leap.Listener):
    
    screen = pygame.display.set_mode((750, 500))
    strengthList = []
    counter = 0
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
        pygame.draw.circle(self.screen, (255,0,0), (10,10), 10)
        
        for hand in frame.hands:
            pygame.draw.circle(self.screen, (0,255,0), (10,10), 10)
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
                    all_sprites.update("Pulse")
                elif self.counter == 2:
                    #print self.counter
                    print "pulse duo"
                    all_sprites.update("Pulse Duo")
                else:
                    #print self.counter
                    print "too many"  
                self.strengthList = []   
                self.counter = 0

class Orb(pygame.sprite.Sprite):
    screen = pygame.display.set_mode((750, 500))
    def __init__(self,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = -250,250 
    def update(self,type):
        self.rect.center = -250,250
        if type == "Pulse":
            self.pulse()
        elif type == "Pulse Duo":
            self.pulseDuo()
    def pulse(self):
        if self.image == pulseCircle1:
            self.rect.center = 375, 250
        else:
            self.rect.center == -250,250
    def pulseDuo(self):
        if self.image == pulseCircle1:
            self.rect.center = 200,250
        else:
            self.rect.center = 550,250

def main():
    pygame.init()
    pygame.mixer.init()
    background_colour = (0,0,0)
    (width, height) = (750,500)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pulse")
    
    screen.fill(background_colour)
    
    global all_sprites
    all_sprites = pygame.sprite.Group()

    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')

    global pulseCircle1, pulseCircle2
    pulseCircle1 = pygame.image.load(os.path.join(img_folder, 'orb4.png')).convert()
    pulseCircle1 = pygame.transform.scale(pulseCircle1, (300,300))
    pulseCircle1.set_colorkey((255,255,255))
    pulseCircle2 = pygame.image.load(os.path.join(img_folder, 'orb4.png')).convert()
    pulseCircle2 = pygame.transform.scale(pulseCircle2, (300,300))
    pulseCircle2.set_colorkey((255,255,255))

    pulses = [pulseCircle1, pulseCircle2]

    for circle in pulses:
        circle = Orb(circle)
        all_sprites.add(circle)

    global listener
    listener = pulseListener()
    controller = Leap.Controller()

    pygame.display.flip()
    running = True

    while running:
        controller.add_listener(listener)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                controller.remove_listener(listener)
        screen.fill((0,0,0))
        all_sprites.draw(screen)
        pygame.display.flip()



if __name__ == "__main__":
    main()