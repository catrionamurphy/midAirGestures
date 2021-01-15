import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap, math
import pygame
import random as r

class Star(pygame.sprite.Sprite):
    def __init__(self,img):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = img
        self.image_original.set_colorkey((0,0,0))
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.rot = 0
        self.rot_speed = 10
        self.last_update = pygame.time.get_ticks()
        if img == star0:
            self.rect.x = 100
            self.rect.y = 80
        if img == star1:
            self.rect.x = 550
            self.rect.y = 80
        elif img == star2:
            self.rect.x = 100
            self.rect.y = 350
        elif img == star3:
            self.rect.x = 600
            self.rect.y = 200
        elif img == star4:
            self.rect.x = 550
            self.rect.y = 350
        elif img == star5:
            self.rect.x = 50
            self.rect.y = 200
    def update(self):
        self.rotate()
    def rotate(self):
        now = pygame.time.get_ticks()
        if (now - self.last_update) > 50:
            self.last_update = now
            self.rot = ((self.rot + self.rot_speed)%360)
            new_image = pygame.transform.rotate(self.image_original, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

class drinkListener(Leap.Listener):
    frameList = []
    screen = pygame.display.set_mode((750, 500))
    champagne_cooler = "CLOSED"

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
                    self.champagne_cooler = "OPEN"
              
            if self.champagne_cooler == "OPEN":
                all_sprites.update()
            
            if len(self.frameList) > 200:
                self.frameList = []
                
def main():
    pygame.init()
    pygame.mixer.init()
    background_colour = (255,255,255)
    (width, height) = (750,500)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Open Champagne Cooler")
    clock = pygame.time.Clock()
    screen.fill(background_colour)

    global all_sprites
    all_sprites = pygame.sprite.Group()

    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')

    heading = pygame.image.load(os.path.join(img_folder, 'cooler2.png')).convert()
    heading.set_colorkey((255,255,255))

    champagne = pygame.image.load(os.path.join(img_folder, 'champers.png')).convert()

    champagne = pygame.transform.scale(champagne, (100,300))
    champagne = pygame.transform.rotate(champagne,330)
    champagne.set_colorkey((0,0,0))

    global star0, star1, star2, star3, star4, star5
    star0 = pygame.image.load(os.path.join(img_folder, 'star1.png')).convert()
    star1 = pygame.image.load(os.path.join(img_folder, 'star1.png')).convert()
    star2 = pygame.image.load(os.path.join(img_folder, 'star2.png')).convert()
    star3 = pygame.image.load(os.path.join(img_folder, 'star3.png')).convert()
    star4 = pygame.image.load(os.path.join(img_folder, 'star4.png')).convert()
    star5 = pygame.image.load(os.path.join(img_folder, 'star4.png')).convert()
    
    starList = [star0, star1, star2, star3, star4, star5]
    for star in starList:
        star = Star(star)
        all_sprites.add(star)

    listener = drinkListener()
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
        screen.blit(champagne, (220,120))
        screen.blit(heading, (90,-5))
        pygame.display.flip()

if __name__ == "__main__":
    main()