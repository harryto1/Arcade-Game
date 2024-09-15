from distutils.command.build import build

import pygame, sys, random

def ball_movement():
    """
    Handles the movement of the ball and collision detection with the player and screen boundaries.
    """
    global ball_speed_x, ball_speed_y, score, start, super_score, high_score

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Start the ball movement when the game begins
    if start:
        ball_speed_x = -7
        ball_speed_y = -7
        start = False

    # Ball collision with the player paddle
    if ball.colliderect(player):
        if abs(ball.bottom - player.top) < 10:  # Check if ball hits the top of the paddle
            score += 1  # Increase player score
            ball_speed_y *= -1  # Reverse ball's vertical direction
            ball_speed_y *= round(random.uniform(1,1.000005), 3) # random number to be less predictable
            ball_speed_x *= round(random.uniform(1,1.000005), 3) # random number to be less predictable
    for obstacle in obstacles:
        if ball.colliderect(obstacle):
            if abs(ball.bottom - obstacle.bottom) < 10:
                score += 1
                ball_speed_y *= -1
                obstacles.remove(obstacle)
                pygame.display.update()
    # Ball collision with top boundary
    if ball.top <= 0:
        ball_speed_y *= -1  # Reverse ball's vertical direction

    # Ball collision with left and right boundaries
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1

    # Ball goes below the bottom boundary (missed by player)
    if ball.bottom > screen_height:
        if score > high_score:
            high_score = score
        restart()  # Reset the game

def invert_colors():
    global player_text, super_score_text, high_score_text
    pygame.draw.rect(screen, light_grey, player)  # Draw player paddle
    player_text = basic_font.render(f'{score}', False, light_grey)  # Render player score
    super_score_text = super_score_font.render(f'{super_score}', False, light_pink)
    high_score_text = basic_font.render(f'{high_score}', False, dark_grey)
    
def player_movement():
    """
    Handles the movement of the player paddle, keeping it within the screen boundaries.
    """
    player.x += player_speed  # Move the player paddle horizontally

    # Prevent the paddle from moving out of the screen boundaries
    if player.left <= 0:
        player.left = 0
    if player.right >= screen_width:
        player.right = screen_width

def build_obstacles():
    global obstacles, temp_var
    n = 120
    temp_var = 0
    obstacles.clear()  # Clear existing obstacles
    i = 0
    for y in range(1, 7):
        for x in range(1, 850):
            if y % 2 == 0:
                if x == 75 or x == temp_var + 95:
                    temp_obstacle = pygame.Rect(x, n, 75, 15)
                    obstacles.append(temp_obstacle)
                    pygame.draw.rect(screen, green, temp_obstacle)
                    temp_var = x
                    i += 1
            else:
                if x == 30 or x == temp_var + 95:
                    temp_obstacle = pygame.Rect(x, n, 75, 15)
                    obstacles.append(temp_obstacle)
                    pygame.draw.rect(screen, green, temp_obstacle)
                    temp_var = x
                    i += 1
        n += 20


def restart():
    """
    Resets the ball and player scores to the initial state.
    """
    global ball_speed_x, ball_speed_y, score, started, super_score
    pygame.font.Font.set_bold(basic_font, True)
    restart_text = basic_font.render('You Died', False, red)  # You Died Text
    restart_text_rect = restart_text.get_rect(center=(screen_width / 2, screen_height / 2))
    screen.blit(restart_text, restart_text_rect)
    pygame.display.update()
    pygame.font.Font.set_bold(basic_font, False)
    pygame.time.wait(750)
    ball.center = (screen_width / 2, screen_height / 2)  # Reset ball position to center
    ball_speed_y, ball_speed_x = 0, 0  # Stop ball movement
    score = 0  # Reset player score
    super_score = 0 # Reset super score
    started = 0 # Reset started
    build_obstacles()

# General setup
pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()
clock = pygame.time.Clock()

# Main Window setup
screen_width = 900 # Screen width (can be adjusted)
screen_height = 600  # Screen height (can be adjusted)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')  # Set window title

# Colors
light_grey = (200, 200, 200)
dark_grey = (100, 100, 100)
light_pink = (255, 179, 222)
blue = (0, 0, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
bg_color = pygame.Color('grey12')

# Game Rectangles (ball and player paddle)
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 24, 24)  # Ball (centered)
player = pygame.Rect(screen_width/2 - 45, screen_height - 20, 100, 15)  # Player paddle

# Game Variables
ball_speed_x = 0
ball_speed_y = 0
player_speed = 0
started = 0
high_score = 0
obstacles = []

# Music Files

# Score Text setup
score = 0
super_score = 0
basic_font = pygame.font.Font('freesansbold.ttf', 32)  # Font for displaying score
super_score_font = pygame.font.Font('freesansbold.ttf', 32)

start = False # Indicates if the game has started

# Main game loop
build_obstacles()
while True:
    # Event handling
    name = "Harry Ruiz"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit the game
            pygame.quit()
            sys.exit()
        # KEY DOWN
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_speed -= 12 # Move paddle left
            if event.key == pygame.K_RIGHT:
                player_speed += 12  # Move paddle right
            if event.key == pygame.K_SPACE:
                if started == 0:
                    start = True  # Start the ball movement
                    started = 1
            if event.key == pygame.K_ESCAPE: # Quit the game if ESC key is pressed
                pygame.quit()
                sys.exit()
        # KEY UP
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_speed += 12  # Stop moving left
            if event.key == pygame.K_RIGHT:
                player_speed -= 12  # Stop moving right
    # Game Logic
    ball_movement()
    player_movement()
    temp_var = 0
    # Visuals
    screen.fill(bg_color)  # Clear screen with background color
    invert_colors()
    i=0
    for obstacle in obstacles:
        pygame.draw.rect(screen, green, obstacle)
    pygame.draw.ellipse(screen, red, ball)  # Draw ball
    screen.blit(player_text, (screen_width/2 - 15, 10))  # Display score on screen
    screen.blit(super_score_text, (screen_width - 50, 10))
    screen.blit(high_score_text, (25, 10))

    # Update display
    pygame.display.flip()
    clock.tick(60)  # Maintain 60 frames per second
