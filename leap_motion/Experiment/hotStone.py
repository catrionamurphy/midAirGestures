import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap, math
import pygame

class HotStoneListener(Leap.Listener):
    maxFrameCount = 100
    frameList = []

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
        frame = controller.frame()

        for hand in frame.hands:
            self.frameList.append(hand)
            start_x = self.frameList[0].palm_position.x
            end_x = self.frameList[-1].palm_position.x
            start_z = self.frameList[0].palm_position.z
            end_z = self.frameList[-1].palm_position.z
            start_y = self.frameList[0].palm_position.y
            end_y = self.frameList[-1].palm_position.y
            difference = (end_x - start_x, end_y - start_y, end_z - start_z)

            absX = abs(difference[0])
            absZ = abs(difference[1])
            
            majorAxis = self.getMajorAxis(absX, 0, absZ)
            if len(self.frameList) > self.maxFrameCount:
                self.frameList = []
                if difference[0] < 5 and difference[1] < 5 and difference[2] < 5:
                    all_sprites.update()
                    print "still"

class Stone(pygame.sprite.Sprite):
    def __init__(self,img):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = img
        self.image_original.set_colorkey((0,0,0))
        self.image_original = pygame.transform.scale(self.image_original, (200,200))
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.rot = 0
        self.rot_speed = 30
        self.last_update = pygame.time.get_ticks()
        if img == rock1:
            self.rect.x = 15
            self.rect.y = 100
        if img == rock2:
            self.rect.x = 630
            self.rect.y = 300
        if img == rock3:
            self.rect.x = 1100
            self.rect.y = 500
        if img == rock4:
            self.rect.x = 1000
            self.rect.y = 120
        if img == rock5:
            self.rect.x = 300
            self.rect.y = 380
        if img == rock6:
            self.rect.x = 600
            self.rect.y = 90
        if img == rock7:
            self.rect.x = 800
            self.rect.y = 450
        if img == rock8:
            self.rect.x = 350
            self.rect.y = 100
        if img == rock9:
            self.rect.x = 50
            self.rect.y = 500
    def update(self):
        self.rotate()
    def rotate(self):
        now = pygame.time.get_ticks()
        if (now - self.last_update) > 10:
            self.last_update = now
            self.rot = ((self.rot + self.rot_speed)%360)
            new_image = pygame.transform.rotate(self.image_original, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
        
        

def main():
    pygame.init()
    pygame.mixer.init()
    background_colour = (255,255,255)
    (width, height) = (1300,700)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Hot Stone Massage")
    clock = pygame.time.Clock()
    screen.fill(background_colour)
    
    global all_sprites
    all_sprites = pygame.sprite.Group()

    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')

    heading = pygame.image.load(os.path.join(img_folder, 'hotStone.png')).convert()
    heading.set_colorkey((255,255,255))

    global rock1, rock2, rock3, rock4, rock5,rock6, rock7, rock8, rock9
    rock1 = pygame.image.load(os.path.join(img_folder, 'hotRock1.png')).convert()
    rock2 = pygame.image.load(os.path.join(img_folder, 'hotRock1.png')).convert()
    rock3 = pygame.image.load(os.path.join(img_folder, 'hotRock1.png')).convert()
    rock4 = pygame.image.load(os.path.join(img_folder, 'hotRock2.png')).convert()
    rock5 = pygame.image.load(os.path.join(img_folder, 'hotRock2.png')).convert()
    rock6 = pygame.image.load(os.path.join(img_folder, 'hotRock2.png')).convert()
    rock7 = pygame.image.load(os.path.join(img_folder, 'hotRock3.png')).convert()
    rock8 = pygame.image.load(os.path.join(img_folder, 'hotRock3.png')).convert()
    rock9 = pygame.image.load(os.path.join(img_folder, 'hotRock3.png')).convert()

    stoneList = [rock1, rock2, rock3, rock4, rock5,rock6, rock7, rock8, rock9]
    for stone in stoneList:
        stone = Stone(stone)
        all_sprites.add(stone)

    global listener
    listener = HotStoneListener()
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
        screen.blit(heading, (350,10))
        pygame.display.flip()



if __name__ == "__main__":
    main()