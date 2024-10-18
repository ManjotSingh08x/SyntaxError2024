import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moving Rectangle")

# Rectangle properties
rect_width, rect_height = 50, 50
rect_x, rect_y = width // 2, height // 2

# Colors
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0,0,255)

import serial
try:
    ard = serial.Serial("/dev/ttyACM0", timeout=1)
except Exception as e:
    print(e)


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the state of all keys
    # keys = pygame.key.get_pressed()

    # Move the rectangle
    try:
        line = ard.readline()
        line_s = line.decode()
        splitted_line = line_s.split("||")
        
        x = int(splitted_line[0].strip(" ").strip("\n"))
        y = int(splitted_line[1].strip(" ").strip("\n"))
        button = bool(int(splitted_line[2].strip(" ").strip("\n")))
        
        # print(x,y,button)
        
        x_default = 503
        y_default = 512
        x_max = 1023
        y_max = 1023
        
        del_x = (x-x_default)/(x_max-x_default)
        del_y = (y-y_default)/(y_max-y_default)
        
        # print(del_y)
        if abs(del_x)<0.02:
            del_x = 0
            
        if abs(del_y)<0.02:
            del_y = 0
        
        max_speed_x = 5
        max_speed_y = 5
        
        speed_x = del_x*max_speed_x
        speed_y = del_y*max_speed_y
        
        
        # print(del_x, del_y)
        print(speed_x, speed_y, button)
        
        rect_x += speed_x
        rect_y += speed_y

        # Fill the screen with black
        screen.fill(black)

        # Draw the rectangle
        if button:
            pygame.draw.rect(screen, blue, (rect_x, rect_y, rect_width, rect_height))
        else:
            pygame.draw.rect(screen, red, (rect_x, rect_y, rect_width, rect_height))

        # Update the display
        pygame.display.flip()
    
    except Exception as e:
        print(e)


    # Limit the frame rate
    # pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
