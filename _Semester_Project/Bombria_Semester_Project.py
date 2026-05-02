import pygame
import random
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
ground_fg = pygame.image.load("_Semester_Project/ground.png")
btm_pipe_img = pygame.image.load("_Semester_Project/pipe_btm.png")
top_pipe_img = pygame.image.load("_Semester_Project/pipe_top.png")
start_img = pygame.image.load("_Semester_Project/start.png")
game_over_img = pygame.image.load("_Semester_Project/game_over.png")
font = pygame.font.SysFont("Segoe", 26)

# Game settings
scroll_spd = 1
bird_start_pos = (180, 250)
score = 0
game_stopped = True

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
        self.alive = True
        
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
        if user_input[pygame.K_SPACE] and not self.flap and self.rect.y > 0 and self.alive:
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
        self.image = ground_fg                   # Uses ground_fg as ground img
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

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, image, pipe_type):
        '''
        Parameters: self, x and y coordinates, image
        Creates the initial pipe using the passed in image
        '''
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.enter = False
        self.exit = False
        self.passed = False
        self.pipe_type = pipe_type
        
    def update(self):
        '''
        Parameters: self
        Moves the pipes along the screen
        Deletes pipe when off screen.
        '''
        # Move pipe
        self.rect.x -= scroll_spd
        
        # Deletes obj when off screen
        if self.rect.x <= -win_width:
            self.kill()
            
        # Global score
        global score
        if self.pipe_type == 'bottom':
            # Bird is entering pipe
            if bird_start_pos[0] > self.rect.topleft[0] and not self.passed:
                self.enter = True
            # Bird has exited pipe
            if bird_start_pos[0] > self.rect.topright[0] and not self.passed:
                self.exit = True
            # Bird has successfully passed pipe
            if self.enter and self.exit and not self.passed:
                self.passed = True
                score += 1
# END OF PIPE CLASS

#----------------------------- FUNCTIONS ------------------------------#
# Quit Function
def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
# Main Menu
def menu():
    global game_stopped

    # Pauses the game and generates menu
    while game_stopped:
        quit_game()

        # Draw menu
        window.fill((0, 0, 0))
        window.blit(sky_bg, (0, 0))
        window.blit(ground_fg, Ground(0, 520))
        window.blit(bird_img, (100, 250))
        window.blit(start_img, (win_width // 2 - start_img.get_width() // 2,
                                win_height // 2 - start_img.get_height() // 2))

        # User input
        user_input = pygame.key.get_pressed()
        
        # Press space to start
        if user_input[pygame.K_SPACE]:
            main()

        pygame.display.update()

#----------------------------- MAIN/GAME LOOP ------------------------------#
def main():
    # AWAKE()
    global score

    # Instantiate bird obj
    bird = pygame.sprite.GroupSingle()      # container/group for a single sprite
    bird.add(Bird())

    # Instantiate initial ground
    x_pos_ground, y_pos_ground = 0, 520
    ground = pygame.sprite.Group()      # creates a container/group to control multiple sprites
    ground.add(Ground(x_pos_ground, y_pos_ground))

    # Setup and instantiate pipes
    pipe_timer = 0
    pipes = pygame.sprite.Group()       # creates a container/group to control multiple sprites


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
        window.blit(sky_bg, (0, 0))         # blit = canvas
            
        # Spawn Ground
        if len(ground) <= 2:
            ground.add(Ground(win_width, y_pos_ground))
            
        # Spawn pipes
        if pipe_timer <= 0 and bird.sprite.alive:
            x_top = 550
            x_bottom = 550
            y_top = random.randint(-600, -480)
            y_bottom = y_top + random.randint(90, 130) + btm_pipe_img.get_height()
            
            pipes.add(Pipe(x_top, y_top, top_pipe_img, 'top'))
            pipes.add(Pipe(x_bottom, y_bottom, btm_pipe_img, 'bottom'))
            pipe_timer = random.randint(180, 250)
        pipe_timer -= 1         # starts countdown for next pipe spawn
        
        # Pipe collision detection
        collision_pipes = pygame.sprite.spritecollide(bird.sprite, pipes, False)
        collision_ground = pygame.sprite.spritecollide(bird.sprite, ground, False)
        
        # If the bird collides with a pipe or the ground
        if collision_pipes or collision_ground:
            bird.sprite.alive = False
            
            if collision_ground:
                window.blit(game_over_img, (win_width // 2 - game_over_img.get_width() // 2,
                                            win_height // 2 - game_over_img.get_height() // 2))
                
                # Resets game
                if user_input[pygame.K_r]:
                    score = 0
                    menu()
                    break
        
        # Draw - Pipes, ground, bird, etc.
        ground.draw(window)
        bird.draw(window)
        pipes.draw(window)
        
        # Show score
        score_text = font.render("Score: " + str(score), True, pygame.Color(255, 255, 255))
        window.blit(score_text, (20, 20))       # blit = canvas

        # UPDATE()
        # Update
        if bird.sprite.alive:
            ground.update()
            pipes.update()
        bird.update(user_input)
            
        clock.tick(60)      # FPS
        pygame.display.update()     # Updates display
    # END OF WHILE
    
menu()