def runHomeScreen(self):
        background_image = pygame.image.load('\assets\ui\load_screen.jpg')
        background_image = pygame.transform.scale(background_image, (800, 800))
        title_image = pygame.image.load('assets\ui\banners\citadel_logo.png')
        title_image = pygame.transform.scale(title_image, (self.settings.screen_width, title_image.get_height() * self.settings.screen_width // title_image.get_width()))
    
        arduino_image = pygame.image.load('assets\ui\banners\use_arduino.png')
        keyboard_image = pygame.image.load('assets\ui\banners\use_keyboard.png')
        
        # Scale images to new sizes
        arduino_image = pygame.transform.scale(arduino_image, (250, 60))
        keyboard_image = pygame.transform.scale(keyboard_image, (250, 60))
        
        while self.hs_running:
            self.screen.blit(background_image, (0, 0))
            self.screen.blit(title_image, (0, 50))
            
            button1_rect = pygame.Rect(self.settings.screen_width // 2 - 125, self.settings.screen_height // 2 - 20, 250, 60)
            button2_rect = pygame.Rect(self.settings.screen_width // 2 - 125, self.settings.screen_height // 2 + 80, 250, 60)

            # Get the mouse position
            mouse_pos = pygame.mouse.get_pos()

            # Check button hover and click
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button1_rect.collidepoint(event.pos):
                        self.use_arduino = True
                        self.hs_running = False
                    if button2_rect.collidepoint(event.pos):
                        self.use_arduino = False
                        self.hs_running = False

            # Animate button on click
            if button1_rect.collidepoint(mouse_pos):
                arduino_image = pygame.transform.scale(pygame.image.load('assets\ui\banners\use_arduino.png'), (320, 90))
            else:
                arduino_image = pygame.transform.scale(pygame.image.load('assets\ui\banners\use_arduino.png'), (300, 70))

            if button2_rect.collidepoint(mouse_pos):
                keyboard_image = pygame.transform.scale(pygame.image.load('assets\ui\banners\use_keyboard.png'), (320, 90))
            else:
                keyboard_image = pygame.transform.scale(pygame.image.load('assets\ui\banners\use_keyboard.png'), (300, 70))

            # Draw the buttons
            self.screen.blit(arduino_image, button1_rect.topleft)
            self.screen.blit(keyboard_image, button2_rect.topleft)

            pygame.display.flip()

        self.screen.fill(YELLOW)
        if self.use_arduino:
            ports = serial.tools.list_ports.comports()
            for port in ports:
                if 'Arduino' in port.description:
                    try:
                        self.ard = serial.Serial(port.device, 9600)
                    except Exception as e:
                        print(e)
                        print("couldn't connect to arduino")
                        sys.exit()
                    self.arduino_connected = True
                    break

            if not self.arduino_connected:
                print("No connected arduino found")
                sys.exit()
        else:
            print('done')
            self.settings.player_max_speed = 4
            self.settings.enemy_speed = 1
        self.spawn_player()
        self.spawn_enemies()
        self.place_cannon()
        self.game_running = True
        self.rungame()