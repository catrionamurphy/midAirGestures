import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap, math
import pygame

class Volume(Leap.Listener):
    frameList = []
    screen = pygame.display.set_mode((750, 500))
    maxFrameCount = 100
    vol = 50
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
            self.frameList.append(hand)

            startAngle = self.frameList[0].direction.yaw
            startAngle = startAngle * Leap.RAD_TO_DEG
            endAngle = self.frameList[-1].direction.yaw
            endAngle = endAngle * Leap.RAD_TO_DEG
            
            angles = (startAngle,endAngle)

            difference_angles = endAngle-startAngle

            if len(self.frameList) > self.maxFrameCount:
                # reset number of frames
                self.frameList = []

                print difference_angles
                if difference_angles > 5:
                    volume = "up"
                elif difference_angles < -5:
                    volume = "down"
                else:
                    volume = "same"

                if volume == "up":
                    #print volume
                    if self.vol > 90:
                        self.vol = 95
                    else:
                        self.vol += 5
                    #print self.vol
                    all_sprites.update(self.vol)
                elif volume == "down":
                    #print volume
                    if self.vol<5:
                        self.vol = 0
                    else:
                        self.vol -= 5
                    #print self.vol
                    all_sprites.update(self.vol)
                else:
                    all_sprites.update(self.vol)
                    

class Dial(pygame.sprite.Sprite):
    screen = pygame.display.set_mode((1300, 700))
    def __init__(self,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (-250,250) 
    def update(self, volume):
        self.rect.center = (-250,250) 
        #self.screen.fill((0,volume,0))
        self.numberChange(volume)
    def numberChange(self, volume):
        if volume == 0:
            if self.image == zero:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(625,175,100,150))
                self.rect.center = 650,250
        if volume == 5:
            if self.image == five:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(625,175,100,150))
                self.rect.center = 650,250
        if volume == 10:
            if self.image == ten:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(625,175,100,150))
                self.rect.center = 650,250
        if volume == 15:
            if self.image == fifteen:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(625,175,100,150))
                self.rect.center = 650,250
        if volume == 20:
            if self.image == twenty:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(625,175,100,150))
                self.rect.center = 650,250
        if volume == 25:
            if self.image == twentyfive:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(625,175,100,150))
                self.rect.center = 650,250
        if volume == 30:
            if self.image == thirty:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(625,175,100,150))
                self.rect.center = 650,250
        if volume == 35:
            if self.image == thirtyfive:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(625,175,100,150))
                self.rect.center = 650,250
        if volume == 40:
            if self.image == forty:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(625,175,100,150))
                self.rect.center = 650,250
        if volume == 45:
            if self.image == fortyfive:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(625,175,100,150))
                self.rect.center = 650,250
        if volume == 50:
            if self.image == fifty:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(625,175,100,150))
                self.rect.center = 650,250
        if volume == 55:
            if self.image == fiftyfive:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(625,175,100,150))
                self.rect.center = 650,250
        if volume == 60:
            if self.image == sixty:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(625,175,100,150))
                self.rect.center = 650,250
        if volume == 65:
            if self.image == sixtyfive:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(625,175,100,150))
                self.rect.center = 650,250
        if volume == 70:
            if self.image == seventy:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(625,175,100,150))
                self.rect.center = 650,250
        if volume == 75:
            if self.image == seventyfive:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(625,175,100,150))
                self.rect.center = 650,250
        if volume == 80:
            if self.image == eighty:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(625,175,100,150))
                self.rect.center = 650,250
        if volume == 85:
            if self.image == eightyfive:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(625,175,100,150))
                self.rect.center = 650,250
        if volume == 90:
            if self.image == ninety:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(625,175,100,150))
                self.rect.center = 650,250
        if volume == 95:
            if self.image == ninetyfive:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(625,175,100,150))
                self.rect.center = 650,250


def main():
    pygame.init()
    pygame.mixer.init()
    background_colour = (255,255,255)
    (width, height) = (1300,700)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Adjust Volume")
    screen.fill(background_colour)

    global all_sprites
    all_sprites = pygame.sprite.Group()

    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')

    heading = pygame.image.load(os.path.join(img_folder, 'volume.png')).convert()
    heading.set_colorkey((255,255,255))

    global zero, five, ten, fifteen, twenty, twentyfive, thirty, thirtyfive, forty, fortyfive, fifty, fiftyfive, sixty, sixtyfive, seventy, seventyfive, eighty, eightyfive, ninety, ninetyfive, hundred
    
    zero = pygame.image.load(os.path.join(img_folder, 'zero.png')).convert()
    zero = pygame.transform.scale(zero, (80,150))
    five = pygame.image.load(os.path.join(img_folder, 'five.png')).convert()
    five = pygame.transform.scale(five, (80,150))
    ten = pygame.image.load(os.path.join(img_folder, 'ten.png')).convert()
    ten = pygame.transform.scale(ten, (80,150))
    fifteen = pygame.image.load(os.path.join(img_folder, 'fifteen.png')).convert()
    fifteen = pygame.transform.scale(fifteen, (80,150))
    twenty = pygame.image.load(os.path.join(img_folder, 'twenty.png')).convert()
    twenty = pygame.transform.scale(twenty, (80,150))
    twentyfive = pygame.image.load(os.path.join(img_folder, 'twentyfive.png')).convert()
    twentyfive = pygame.transform.scale(twentyfive, (80,150))
    thirty = pygame.image.load(os.path.join(img_folder, 'thirty.png')).convert()
    thirty = pygame.transform.scale(thirty, (80,150))
    thirtyfive = pygame.image.load(os.path.join(img_folder, 'thirtyfive.png')).convert()
    thirtyfive = pygame.transform.scale(thirtyfive, (80,150))
    forty = pygame.image.load(os.path.join(img_folder, 'forty.png')).convert()
    forty = pygame.transform.scale(forty, (80,150))
    fortyfive = pygame.image.load(os.path.join(img_folder, 'fortyfive.png')).convert()
    fortyfive = pygame.transform.scale(fortyfive, (80,150))
    fifty = pygame.image.load(os.path.join(img_folder, 'fifty.png')).convert()
    fifty = pygame.transform.scale(fifty, (80,150))
    fiftyfive = pygame.image.load(os.path.join(img_folder, 'fiftyfive.png')).convert()
    fiftyfive = pygame.transform.scale(fiftyfive, (80,150))
    sixty = pygame.image.load(os.path.join(img_folder, 'sixty.png')).convert()
    sixty = pygame.transform.scale(sixty, (80,150))
    sixtyfive = pygame.image.load(os.path.join(img_folder, 'sixtyfive.png')).convert()
    sixtyfive = pygame.transform.scale(sixtyfive, (80,150))
    seventy = pygame.image.load(os.path.join(img_folder, 'seventy.png')).convert()
    seventy = pygame.transform.scale(seventy, (80,150))
    seventyfive = pygame.image.load(os.path.join(img_folder, 'seventyfive.png')).convert()
    seventyfive = pygame.transform.scale(seventyfive, (80,150))
    eighty = pygame.image.load(os.path.join(img_folder, 'eighty.png')).convert()
    eighty = pygame.transform.scale(eighty, (80,150))
    eightyfive = pygame.image.load(os.path.join(img_folder, 'eightyfive.png')).convert()
    eightyfive = pygame.transform.scale(eightyfive, (80,150))
    ninety = pygame.image.load(os.path.join(img_folder, 'ninety.png')).convert()
    ninety = pygame.transform.scale(ninety, (80,150))
    ninetyfive = pygame.image.load(os.path.join(img_folder, 'ninetyfive.png')).convert()
    ninetyfive = pygame.transform.scale(ninetyfive, (80,150))
    
    
    digits = [zero, five, ten, fifteen, twenty, twentyfive, thirty, thirtyfive, forty, fortyfive, fifty, fiftyfive, sixty, sixtyfive, seventy, seventyfive, eighty, eightyfive, ninety, ninetyfive]
    for number in digits:
        dial = Dial(number)
        all_sprites.add(dial)
    
    pygame.draw.circle(screen, (0,0,0), (650, 250), 100, 10)

    listener = Volume()
    controller = Leap.Controller()
    
    running = True

    while running:
        controller.add_listener(listener)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                controller.remove_listener(listener)
        all_sprites.draw(screen)
        screen.blit(heading, (500,10))
        pygame.display.flip()
        

if __name__ == "__main__":
    main()