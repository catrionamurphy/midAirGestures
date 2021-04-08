import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap, math
import pygame


class Slider(pygame.sprite.Sprite):
    brightnessCounter = 0
    def __init__(self,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = 60,350
    def update(self,l):
        swipeDir = l.swipeDirection
        if swipeDir == "Up":
            self.brightnessCounter += 1
            if self.brightnessCounter > 3:
                self.brightnessCounter = 3
        elif swipeDir == "Down":
            self.brightnessCounter -= 1
            if self.brightnessCounter < 0:
                self.brightnessCounter = 0
        if self.brightnessCounter == 0:
            self.rect.center = 60,350
        elif self.brightnessCounter == 1:
            self.rect.center = 440, 350
        elif self.brightnessCounter == 2:
            self.rect.center = 820, 350
        elif self.brightnessCounter == 3:
            self.rect.center = 1200, 350

class swipeListener(Leap.Listener):

    maxFrameCount = 200
    frameList = []

    ultraviolet = (127, 0, 255)
    electricBlue = (0, 128, 255)
    sparkBlue = (60, 200, 255)
    moonlight = (0, 255, 255)
    daylight = (255, 255, 204)
    iceWhite = (255, 255, 255)
    amberGlow = (255, 255, 51)
    limelight = (0, 204, 0)
    sunset = (255, 128, 0)
    racingRed = (255, 0, 0)
    swipeDirection = ""
    colours = [ultraviolet,electricBlue,sparkBlue,moonlight,daylight,iceWhite,amberGlow,limelight,sunset,racingRed]
    colourCounter = 0
    screen = pygame.display.set_mode((1300, 700))

    def on_init(self, controller):
        print "Initialised"

    def on_connect(self, controller):
        print "Motion Sensor Connected"

    def on_disconnect(self, controller):
        print "Motion Sensor Disconnected"

    def on_exit(self, controller):
        print "Exit"

    def getMajorAxis(self,x,y,z):
        if x > y and x > z:
            return 'x'
        elif y > x and y > z:
            return 'y'
        elif z > x and z > y:
            return 'z' 

    def on_frame(self, controller):
        pygame.draw.circle(self.screen, (255,0,0), (10,10), 10)
        frame = controller.frame()

        for hand in frame.hands:
            pygame.draw.circle(self.screen, (0,255,0), (10,10), 10)
            self.frameList.append(hand)

            start_x = self.frameList[0].palm_position.x
            end_x = self.frameList[-1].palm_position.x
            start_z = self.frameList[0].palm_position.z
            end_z = self.frameList[-1].palm_position.z
            difference = (end_x - start_x, end_z - start_z)

            absX = abs(difference[0])
            absZ = abs(difference[1])
            
            majorAxis = self.getMajorAxis(0, 0, absZ)

            if majorAxis == 'z' and absZ > 50:
                if difference[1] > 0:
                    self.swipeDirection = "Down"
                else:
                    self.swipeDirection = "Up"

        hands = frame.hands
        noHands = len(hands)

        if noHands == 0 or len(self.frameList) > self.maxFrameCount:   
            self.frameList = []
            if self.swipeDirection <> "":
                print self.swipeDirection
                if self.swipeDirection == "Up":
                    all_sprites.update(listener)
                elif self.swipeDirection == "Down":
                    all_sprites.update(listener)    
            self.swipeDirection = ""         

def main():
    pygame.init()
    pygame.mixer.init()
    background_colour = (255,255,255)
    (width, height) = (1300,700)
    end_colour = (0,0,0)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Brightness")
    
    screen.fill(background_colour)

    global all_sprites
    all_sprites = pygame.sprite.Group()

    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')
    
    sliderCircle = pygame.image.load(os.path.join(img_folder, 'circle.png')).convert()
    sliderCircle = pygame.transform.scale(sliderCircle, (80,60))
    slider = Slider(sliderCircle) 
    all_sprites.add(slider)    

    heading = pygame.image.load(os.path.join(img_folder, 'brightness.png')).convert()
    heading.set_colorkey((255,255,255))

    
    global listener
    listener = swipeListener()
    controller = Leap.Controller()
    
    running = True

    while running:
        controller.add_listener(listener)
        
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(0,300,1300,90))
        pygame.draw.line(screen, (0,0,0), (60,350), (1200,350), 10)
        pygame.draw.circle(screen, (0,0,0), (60, 350), 15)
        pygame.draw.circle(screen, (0,0,0), (440, 350), 15)
        pygame.draw.circle(screen, (0,0,0), (820, 350), 15)
        pygame.draw.circle(screen, (0,0,0), (1200, 350), 15)

        all_sprites.draw(screen)
        screen.blit(heading, (450,10))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                controller.remove_listener(listener)

if __name__ == "__main__":
    main()