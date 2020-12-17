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
    vol = 10
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


            if difference_angles > 0:
                    volume = "up"
                elif difference_angles < 0:
                    volume = "down"
                else:
                    volume = "same"

            if len(self.frameList) > self.maxFrameCount:
                # reset number of frames
                self.frameList = []

                if volume == "up"



def main():
    pygame.init()
    pygame.mixer.init()
    background_colour = (255,255,255)
    (width, height) = (750,500)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Adjust Temperature")
    screen.fill(background_colour)

    global all_sprites
    all_sprites = pygame.sprite.Group()

    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')

    global five, ten, fifteen, twenty, twentyfive, thirty, thirtyfive, forty, fortyfive, fifty, fiftyfive, sixty, sixtyfive, seventy, seventyfive, eighty, eightyfive, ninety, ninetyfive,
    global red,orange,blue
    global triangle

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
    
    digits = [sixteen, seventeen, eighteen, nineteen, twenty, twentyone, twentytwo, twentythree, twentyfour]
    for number in digits:
        dial = Dial(number)
        all_sprites.add(dial)
    
    global colouredRings
    colouredRings = [red,orange,blue]
    for colours in colouredRings:
        dial = Dial(colours)
        all_sprites.add(dial)

    pygame.draw.circle(screen, (0,0,0), (375, 250), 100, 10)

    #pygame.draw.polygon(screen, (0,0,0), [(250,270),(330,250),(250, 230)])

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
        pygame.display.flip()

if __name__ == "__main__":
    main()