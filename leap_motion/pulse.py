


class pulseListener(Leap.Listener):
    def on_init(self, controller):
        print "Initialised"

    def on_connect(self, controller):
        print "Motion Sensor Connected"

    def on_disconnect(self, controller):
        print "Motion Sensor Disconnected"

    def on_exit(self, controller):
        print "Exit"




def main():
    pygame.init()
    pygame.mixer.init()
    background_colour = (255,255,255)
    (width, height) = (750,500)
    end_colour = (0,0,0)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Ambient Lighting")
    
    screen.fill(background_colour)

    pygame.draw.rect(screen, (127, 0, 255), pygame.Rect(30, 400, 60, 60))
    pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(100, 400, 60, 60))
    pygame.draw.rect(screen, (60, 200, 255), pygame.Rect(170, 400, 60, 60))
    pygame.draw.rect(screen, (0, 255, 255), pygame.Rect(240, 400, 60, 60))
    pygame.draw.rect(screen, (255, 255, 204), pygame.Rect(310, 400, 60, 60))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(380, 400, 60, 60))
    pygame.draw.rect(screen, (255, 255, 51), pygame.Rect(450, 400, 60, 60))
    pygame.draw.rect(screen, (0, 204, 0), pygame.Rect(520, 400, 60, 60))
    pygame.draw.rect(screen, (255, 128, 0), pygame.Rect(590, 400, 60, 60))
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(660, 400, 60, 60))
    
    global all_sprites
    all_sprites = pygame.sprite.Group()

    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')
    
    sliderCircle = pygame.image.load(os.path.join(img_folder, 'circle.png')).convert()
    sliderCircle = pygame.transform.scale(sliderCircle, (80,60))
    slider = Slider(sliderCircle) 
    all_sprites.add(slider)    

    global listener
    listener = swipeListener()
    controller = Leap.Controller()

    running = True

    while running:
        controller.add_listener(listener)
        
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(0,0,750,90))
        pygame.draw.line(screen, (0,0,0), (60,50), (670,50), 10)
        pygame.draw.circle(screen, (0,0,0), (60, 50), 15)
        pygame.draw.circle(screen, (0,0,0), (280, 50), 15)
        pygame.draw.circle(screen, (0,0,0), (480, 50), 15)
        pygame.draw.circle(screen, (0,0,0), (670, 50), 15)

        all_sprites.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                controller.remove_listener(listener)

if __name__ == "__main__":
    main()