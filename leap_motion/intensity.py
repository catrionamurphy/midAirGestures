import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap, math
import pygame

class IntensityListener(Leap.Listener):
    intensityLevel = 0
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
        pygame.draw.circle(self.screen, (255,0,0), (10,10), 10)
        
        for hand in frame.hands:
            pygame.draw.circle(self.screen, (0,255,0), (10,10), 10)

            extendedFingers = frame.fingers.extended()
            noFingers = len(extendedFingers)
            if noFingers == 1:
                self.intensityLevel = 1
            elif noFingers == 2:
                self.intensityLevel =2
            elif noFingers == 3:
                self.intensityLevel = 3
            elif noFingers == 4:
                self.intensityLevel = 4
            elif noFingers == 5:
                self.intensityLevel = 5
        print self.intensityLevel
        all_sprites.update(self.intensityLevel)

class Numbers(pygame.sprite.Sprite):
    screen = pygame.display.set_mode((750, 500))
    def __init__(self,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (-250,250) 
    def update(self, level):
        self.rect.center = (-250,250)
        self.change(level)
    def change(self,level):
        if level == 1 and self.image == one:
            pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(325,150,100,200))
            self.rect.center = 375,250
        if level == 2 and self.image == two:
            pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(325,150,100,200))
            self.rect.center = 375,250
        if level == 3 and self.image == three:
            pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(325,150,100,200))
            self.rect.center = 375,250
        if level == 4 and self.image == four:
            pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(325,150,100,200))
            self.rect.center = 375,250
        if level == 5 and self.image == five:
            pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(325,150,100,200))
            self.rect.center = 375,250
        if level == 0 and (self.image == one or self.image == two or self.image==three or self.image==four or self.image==five):
            self.rect.center = (-250,250)


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

    heading = pygame.image.load(os.path.join(img_folder, 'intensity.png')).convert()
    heading.set_colorkey((255,255,255))

    global one, two, three, four, five

    one = pygame.image.load(os.path.join(img_folder, 'one.png')).convert()
    one = pygame.transform.scale(one, (100,180))
    two = pygame.image.load(os.path.join(img_folder, 'two.png')).convert()
    two = pygame.transform.scale(two, (100,180))
    three = pygame.image.load(os.path.join(img_folder, 'three.png')).convert()
    three = pygame.transform.scale(three, (100,180))
    four = pygame.image.load(os.path.join(img_folder, 'four.png')).convert()
    four = pygame.transform.scale(four, (100,180))
    five = pygame.image.load(os.path.join(img_folder, 'five.png')).convert()
    five = pygame.transform.scale(five, (100,180))

    numbers = [one, two, three, four, five]

    for number in numbers:
        number = Numbers(number)
        all_sprites.add(number)

    #global listener
    listener = IntensityListener()
    controller = Leap.Controller()

    running = True

    while running:
        controller.add_listener(listener)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                controller.remove_listener(listener)
        all_sprites.draw(screen)
        screen.blit(heading, (90,10))
        pygame.display.flip()


if __name__ == "__main__":
    main()