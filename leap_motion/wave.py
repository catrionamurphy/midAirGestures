import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap, math
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import pygame

class WaveListener(Leap.Listener):
    screen = pygame.display.set_mode((750, 500))
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
        #print "on frame"
        #pygame.draw.circle(self.screen, (255,0,0), (10,10), 10)

        extendedFingers = frame.fingers.extended()

        """
        for hand in frame.hands:
            #print "Hand detected"
            print len(extendedFingers)
        """

        for gesture in frame.gestures():
            # Circle Data
            #print "gesture"
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                #print "circle"
                circle = CircleGesture(gesture)
                
                if len(extendedFingers) == 5 or len(extendedFingers) == 4:
                    if circle.progress < 1:
                        print "Wave"
                        all_sprites.update()

class Waves(pygame.sprite.Sprite):
    screen = pygame.display.set_mode((750, 500))
    def __init__(self,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        #self.rect.center = -375,250

        if self.image == wave1:
            self.rect.center = -500, -150
        if self.image == wave2:
            self.rect.center = 375, 120
        if self.image == wave3:
            self.rect.center = 375, 400

    
    def update(self):
        for i in range (400):
            self.moveUp()
    def moveUp(self):
        self.rect.y += 10
        if self.rect.y <= 0:
            self.moveDown()
    def moveDown(self):
        self.rect.y -= 10
        if self.rect.y >= 500:
            self.moveUp
        
    
    
    """
    def Wave1(self):
        #print "Wave 1 Called"
        self.rect.center = -375,250
        if self.image == wave1:
            self.rect.center = 375, 250
    def Wave2(self):
        #print "Wave 2 Called"
        self.rect.center = -375,250
        if self.image == wave2:
            self.rect.center = 375, 250
    def Wave3(self):
        #print "Wave 3 Called"
        self.rect.center = -375,250
        if self.image == wave3:
            self.rect.center = 375, 250
    """
    """
    def update(self):
        self.rect.center = -375,250 
        for i in range(12):
            self.order()

    def order(self):
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(0, 0, 750, 500))
        self.Wave2()
        pygame.time.wait(50)
        self.Wave3()
        pygame.time.wait(50)
    """
       
def main():
    pygame.init()
    pygame.mixer.init()
    background_colour = (255,255,255)
    (width, height) = (750,500)

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Wave")
    
    screen.fill(background_colour)
    
    global all_sprites
    all_sprites = pygame.sprite.Group()

    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')

    global wave1, wave2, wave3
    wave1 = pygame.image.load(os.path.join(img_folder, 'wave.png')).convert()
    wave1 = pygame.transform.scale(wave1, (750,500))
    wave2 = pygame.image.load(os.path.join(img_folder, 'wave4.png')).convert()
    wave2 = pygame.transform.scale(wave2, (750,250))
    wave3 = pygame.image.load(os.path.join(img_folder, 'wave5.png')).convert()
    wave3 = pygame.transform.scale(wave3, (750,250))
    
    waves = [wave1, wave2, wave3]
    for wave in waves:
        wave = Waves(wave)
        all_sprites.add(wave)

    listener = WaveListener()
    controller = Leap.Controller()

    running = True
    while running:
        controller.add_listener(listener)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                controller.remove_listener(listener)
        all_sprites.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()