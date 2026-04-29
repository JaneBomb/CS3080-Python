import pygame
from sys import exit

'''
Name: Jane Bombria
Class: CS3080
Professor: Professor Z.
Due Date: May 3, 2026

Assignment:
Recreating 'Flappy Bird' with Python's pygame

Note: Followed this tutorial: https://www.youtube.com/watch?v=7IqrZb0Sotw&t=1431s 
'''
# Creates a new pygame with a clock
pygame.init()
clock = pygame.time.Clock()

#----------------------------- SETTINGS ------------------------------#
# Window Settings
win_height = 720
win_width = 551
window = pygame.display.set_mode((win_width, win_height))

# Image settings
bird_img = pygame.image.load("_Semester_Project/bird.png")
sky_bg = pygame.image.load("_Semester_Project/sky.png")
grass_fg = pygame.image.load("_Semester_Project/sky.png")
btm_pipe_img = pygame.image.load("_Semester_Project/pipe_btm.png")
top_pipe_img = pygame.image.load("_Semester_Project/pipe_top.png")

# Game settings
scroll_spd = 1
bird_start_pos = (180, 250)

#----------------------------- CLASSES ------------------------------#
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)     # for visible game obj
        '''
        Parameters: Self
        Initializes the bird obj
        '''
        self.image = bird_img
        self.rect = self.image.get_rect()
        self.rect.center = bird_start_pos
        self.velocity = 0
        self.flap = False
        
    def update(self, user_input):
        '''
        Parameters: self, and user input
        Update called every loop
        Controls the bird's flapping
        '''
        # Gravity and flap
        self.velocity += 0.5
        
        # Ensures bird's velocity doesn't exceed 7 (prevents downwards movement)
        if self.velocity > 7:
            self.velocity = 7
        
        # Sets a limit for where the bird can start moving upwards
        if self.rect.y < 500:
            self.rect.y += int(self.velocity)
            
        # Sets a limit for how high the bird and flap on the screen
        if self.velocity == 0:
            self.flap = False
            
        # If there's user input, the bird is not currently flapping, and the bird's position is greater than 0
        # Ensures used cannot spam flapping
        # Ensures bird is not in a gameover state
        if user_input[pygame.K_SPACE] and not self.flap and self.rect.y > 0:
            self.flap = True
            self.velocity = -7
# END OF BIRD CLASS
        

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        '''
        Parameters: Self, x coord, y coord
        Initializes the ground object
        '''
        pygame.sprite.Sprite.__init__(self)     # for visible game obj
        self.image = grass_fg                   # Uses grass_fg as ground img
        self.rect = self.image.get_rect()          # Rectangle object
        self.rect.x, self.rect.y = x, y         # Initializes location
        
    def update(self):
        '''
        Parameters: self
        Update called every loop
        Moves the ground across the bottom of screen to simulate movement
        Destroys object when off-screen
        '''
        # Move ground
        # If ground is off screen, destryo/kill object
        self.rect.x -= scroll_spd
        if self.rect.x <= -win_width:
            self.kill()
# END OF GROUND CLASS

#----------------------------- FUNCTIONS ------------------------------#
# Quit Function
def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
#----------------------------- MAIN/GAME LOOP ------------------------------#
# AWAKE()
# Instantiate initial ground
x_pos_ground, y_pos_ground = 0, 520
ground = pygame.sprite.Group()      # creates a container/group to control multiple sprites
ground.add(Ground(x_pos_ground, y_pos_ground))
    
# Instantiate bird obj
bird = pygame.sprite.GroupSingle()      # container/group for a single sprite
bird.add(Bird())

# START()
run = True
# Game loop
while run:
    # Creates quit (red 'x') button
    quit_game()     
    # Reset frame
    window.fill((0, 0, 0))
        
    # User input
    user_input = pygame.key.get_pressed()
        
    # Draw BG
    window.blit(sky_bg, (0, 0))
        
    # Spawn Ground
    if len(ground) <= 2:
        ground.add(Ground(win_width, y_pos_ground))

    # Draw - Pipes, ground, bird, etc.
    ground.draw(window)
    bird.draw(window)

    # UPDATE()
    # Update
    ground.update()
    bird.update(user_input)
        
    clock.tick(60)      # FPS
    pygame.display.update()     # Updates display
# END OF WHILE