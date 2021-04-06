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
    maxFrameCount = 100
    actualTemp = 16

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
            extendedFingers = hand.fingers.extended()

            pygame.draw.circle(self.screen, (0,255,0), (10,10), 10)
            self.frameList.append(hand)


            if len(extendedFingers) > 2:
                # print len(extendedFingers)
                # check dial 'angle'
                startAngle = self.frameList[0].direction.yaw
                startAngle = startAngle * Leap.RAD_TO_DEG
                endAngle = self.frameList[-1].direction.yaw
                endAngle = endAngle * Leap.RAD_TO_DEG

                angles = (startAngle,endAngle)

                difference_angles = endAngle-startAngle

                # check difference
                if len(self.frameList) > self.maxFrameCount:
                    # reset number of frames
                    self.frameList = []

                    # AIR CONDITIONING
                    if difference_angles > 10:
                        temperature = "up"
                    elif difference_angles < -10:
                        temperature = "down"
                    else:
                        temperature = "same"
                    print len(extendedFingers)
                    print (angles)
                    print difference_angles
                    print temperature


                    if temperature == "up" and self.actualTemp <= 24:
                        if difference_angles < 20:
                            if self.actualTemp >23:
                                self.actualTemp = 24
                            else:
                                self.actualTemp += 1
                            all_sprites.update(self.actualTemp)
                        elif difference_angles >= 20 and difference_angles < 40:
                            if self.actualTemp >22:
                                self.actualTemp = 24
                            else:
                                self.actualTemp += 2
                            all_sprites.update(self.actualTemp)
                        elif difference_angles >= 40 and difference_angles < 80:
                            if self.actualTemp >21:
                                self.actualTemp = 24
                            else:
                                self.actualTemp += 3
                            all_sprites.update(self.actualTemp)
                        elif difference_angles >= 80:
                            
                            if self.actualTemp > 19:
                                self.actualTemp = 24
                            else:
                                self.actualTemp += 5
                            all_sprites.update(self.actualTemp)
                        #print self.actualTemp
                    elif temperature == "down" and self.actualTemp >= 16:
                        
                        if difference_angles > -20:
                            if self.actualTemp < 17:
                                self.actualTemp = 16
                            else:
                                self.actualTemp -= 1
                            all_sprites.update(self.actualTemp)
                        elif difference_angles <= -20 and difference_angles > -40:
                            if self.actualTemp < 18:
                                self.actualTemp = 16
                            else:
                                self.actualTemp -= 2
                            all_sprites.update(self.actualTemp)
                        elif difference_angles <= -40 and difference_angles > -80:
                            if self.actualTemp < 19:
                                self.actualTemp = 16
                            else:
                                self.actualTemp -= 3
                            all_sprites.update(self.actualTemp)
                        elif difference_angles <= -80:
                            if self.actualTemp < 21:
                                self.actualTemp = 16
                            else:
                                self.actualTemp -= 5
                            all_sprites.update(self.actualTemp)
                        #print self.actualTemp
                    else:
                        all_sprites.update(self.actualTemp)
            else:
                #print "reset"
                self.frameList = []


            """

            #print difference_angles
            if len(self.frameList) > self.maxFrameCount:
                # reset number of frames
                self.frameList = []

                # AIR CONDITIONING
                if difference_angles > 0:
                    temperature = "up"
                elif difference_angles < 0:
                    temperature = "down"
                else:
                    temperature = "same"

                if temperature == "up" and self.actualTemp <= 24:
                    if difference_angles < 20:
                        if self.actualTemp >23:
                            self.actualTemp = 24
                        else:
                            self.actualTemp += 1
                        all_sprites.update(self.actualTemp)
                    elif difference_angles >= 20 and difference_angles < 40:
                        if self.actualTemp >22:
                            self.actualTemp = 24
                        else:
                            self.actualTemp += 2
                        all_sprites.update(self.actualTemp)
                    elif difference_angles >= 40 and difference_angles < 80:
                        if self.actualTemp >21:
                            self.actualTemp = 24
                        else:
                            self.actualTemp += 3
                        all_sprites.update(self.actualTemp)
                    elif difference_angles >= 80:
                        
                        if self.actualTemp > 19:
                            self.actualTemp = 24
                        else:
                            self.actualTemp += 5
                        all_sprites.update(self.actualTemp)
                    #print self.actualTemp
                elif temperature == "down" and self.actualTemp >= 16:
                    
                    if difference_angles > -20:
                        if self.actualTemp < 17:
                            self.actualTemp = 16
                        else:
                            self.actualTemp -= 1
                        all_sprites.update(self.actualTemp)
                    elif difference_angles <= -20 and difference_angles > -40:
                        if self.actualTemp < 18:
                            self.actualTemp = 16
                        else:
                            self.actualTemp -= 2
                        all_sprites.update(self.actualTemp)
                    elif difference_angles <= -40 and difference_angles > -80:
                        if self.actualTemp < 19:
                            self.actualTemp = 16
                        else:
                            self.actualTemp -= 3
                        all_sprites.update(self.actualTemp)
                    elif difference_angles <= -80:
                        if self.actualTemp < 21:
                            self.actualTemp = 16
                        else:
                            self.actualTemp -= 5
                        all_sprites.update(self.actualTemp)
                    print self.actualTemp
                else:
                    all_sprites.update(self.actualTemp)
            """
                

class Dial(pygame.sprite.Sprite):
    screen = pygame.display.set_mode((1300, 700))
    def __init__(self,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (-250,250)
    def update(self, actualTemp):
        self.colourChange(actualTemp)
        self.numberChange(actualTemp)
    def numberChange(self,actualTemp):
        if actualTemp == 16:
            if self.image == sixteen:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(610,275,100,150))
                self.rect.center = 650,350
        if actualTemp == 17:
            if self.image == seventeen:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(610,275,100,150))
                self.rect.center = 630,350
        if actualTemp == 18:
            if self.image == eighteen:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(610,275,100,150))
                self.rect.center = 640,350
        if actualTemp == 19:
            if self.image == nineteen:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(610,275,100,150))
                self.rect.center = 640,350
        if actualTemp == 20:
            if self.image == twenty:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(610,275,100,150))
                self.rect.center = 650,350
        if actualTemp == 21:
            if self.image == twentyone:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(610,275,100,150))
                self.rect.center = 650,350
        if actualTemp == 22:
            if self.image == twentytwo:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(605,275,100,150))
                self.rect.center = 650,350
        if actualTemp == 23:
            if self.image == twentythree:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(610,275,100,150))
                self.rect.center = 650,350
        if actualTemp == 24:
            if self.image == twentyfour:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(610,275,100,150))
                self.rect.center = 640,350
    def colourChange(self,actualTemp):
        if actualTemp > 21:
            if self.image == red:
                self.rect.center = (650,350)
            else:
                self.rect.center = (-250,350)
        elif actualTemp >18 and actualTemp <= 21:
            if self.image == orange:
                self.rect.center = (650,350)
            else:
                self.rect.center = (-250,350)
        elif actualTemp <= 18:
            if self.image == blue:
                self.rect.center = (650,350)
            else:
                self.rect.center = (-250,350)


def main():
    pygame.init()
    pygame.mixer.init()
    background_colour = (255,255,255)
    (width, height) = (1300,700)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Adjust Temperature")
    screen.fill(background_colour)

    global all_sprites
    all_sprites = pygame.sprite.Group()

    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')
    
    heading = pygame.image.load(os.path.join(img_folder, 'Temperature.png')).convert()
    heading.set_colorkey((255,255,255))

    global sixteen, seventeen, eighteen, nineteen, twenty, twentyone, twentytwo, twentythree, twentyfour
    global red,orange,blue

    sixteen = pygame.image.load(os.path.join(img_folder, 'sixteen.jpg')).convert()
    sixteen = pygame.transform.scale(sixteen, (100,150))
    seventeen = pygame.image.load(os.path.join(img_folder, 'seventeen.png')).convert()
    seventeen = pygame.transform.scale(seventeen, (100,150))
    eighteen = pygame.image.load(os.path.join(img_folder, 'eighteen.png')).convert()
    eighteen = pygame.transform.scale(eighteen, (100,150))
    nineteen = pygame.image.load(os.path.join(img_folder, 'nineteen.png')).convert()
    nineteen = pygame.transform.scale(nineteen, (100,150))
    twenty = pygame.image.load(os.path.join(img_folder, 'twenty.png')).convert()
    twenty = pygame.transform.scale(twenty, (80,150))
    twentyone = pygame.image.load(os.path.join(img_folder, 'twentyone.png')).convert()
    twentyone = pygame.transform.scale(twentyone, (80,150))
    twentytwo = pygame.image.load(os.path.join(img_folder, 'twentytwo.png')).convert()
    twentytwo = pygame.transform.scale(twentytwo, (80,150))
    twentythree = pygame.image.load(os.path.join(img_folder, 'twentythree.png')).convert()
    twentythree = pygame.transform.scale(twentythree, (80,150))
    twentyfour = pygame.image.load(os.path.join(img_folder, 'twentyfour.png')).convert()
    twentyfour = pygame.transform.scale(twentyfour, (80,150))

    
    red = pygame.image.load(os.path.join(img_folder, 'redCircle.png')).convert()
    red = pygame.transform.scale(red, (225,225))
    orange = pygame.image.load(os.path.join(img_folder, 'orangeCircle.png')).convert()
    orange = pygame.transform.scale(orange, (225,225))
    blue = pygame.image.load(os.path.join(img_folder, 'blueCircle.png')).convert()
    blue = pygame.transform.scale(blue, (225,225))
    
    digits = [sixteen, seventeen, eighteen, nineteen, twenty, twentyone, twentytwo, twentythree, twentyfour]
    for number in digits:
        dial = Dial(number)
        all_sprites.add(dial)
    
    global colouredRings
    colouredRings = [red,orange,blue]
    for colours in colouredRings:
        dial = Dial(colours)
        all_sprites.add(dial)

    pygame.draw.circle(screen, (0,0,0), (650, 350), 100, 10)

    listener = adjustTemp()
    controller = Leap.Controller()
    
    running = True

    while running:
        controller.add_listener(listener)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                controller.remove_listener(listener)
        all_sprites.draw(screen)
        screen.blit(heading, (350,10))
        pygame.display.flip()

if __name__ == "__main__":
    main()