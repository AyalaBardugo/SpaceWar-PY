from pygame import *
import random

# Initialize Pygame
init()

# Constants for the game
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
SPACESHIP_WIDTH = 180
SPACESHIP_HEIGHT = 180
ENEMY_WIDTH = 100
ENEMY_HEIGHT = 80
ENEMY_X_CHANGE = 24
ENEMY_Y_CHANGE = 10
NUM_OF_ENEMIES = 6
FIREBALL_WIDTH = 40
FIREBALL_HEIGHT = 40
SPACESHIP_MOVE_STEP = 25
MAX_SPACESHIP_X = WINDOW_WIDTH - SPACESHIP_WIDTH
MAX_FIREBALL_Y = 0
GAME_OVER_Y_THRESHOLD = 360
FIREBALL_Y_STEP = 40

# Colors (RGB values)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

CLOCK_TICK_RATE = 40

# Set up window and game elements
window = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display.set_caption("Space War")
background = image.load('/Users/ayala/Desktop/SpaceWar-Game/images/background.png')

# Background sound
music_background = mixer.Sound('/Users/ayala/Desktop/SpaceWar-Game/sounds/background sound.mp3')
music_background.play()

# Fireball sound
fireball_sound = mixer.Sound("/Users/ayala/Desktop/SpaceWar-Game/sounds/fireball sound.mp3")

# Spaceship setup
spaceship_surf = image.load('/Users/ayala/Desktop/SpaceWar-Game/images/spaceship.png')
spaceship_surf = transform.scale(spaceship_surf, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
spaceship_rect = Rect(300, 400, spaceship_surf.get_width(), spaceship_surf.get_height())

# Enemy setup
enemy = image.load("/Users/ayala/Desktop/SpaceWar-Game/images/enemy.png")
enemy.set_colorkey(COLOR_BLACK)
enemy = transform.scale(enemy, (ENEMY_WIDTH, ENEMY_HEIGHT))

# Create enemies
enemy_imgs = []  
enemy_rects = []  
enemyX_change = []  

for i in range(NUM_OF_ENEMIES): 
    enemy_imgs.append(enemy)
    one_rect = Rect(random.randint(0, WINDOW_WIDTH - ENEMY_WIDTH), random.randint(50, 150),
                    enemy_imgs[-1].get_width(), enemy_imgs[-1].get_height())
    enemy_rects.append(one_rect) 
    enemyX_change.append(ENEMY_X_CHANGE)

# Fireball setup
fireball_surf = image.load('/Users/ayala/Desktop/SpaceWar-Game/images/fireball.png')
fireball_surf = transform.scale(fireball_surf, (FIREBALL_WIDTH, FIREBALL_HEIGHT))
fireball_rect = Rect(0, spaceship_rect.y, fireball_surf.get_width(), fireball_surf.get_height())
fireball_state = "ready" 

# Fonts
over_font = font.SysFont("Calibri", 80) 
score_font = font.SysFont("Calibri", 30) 

score_value = 0 

clock = time.Clock()

run = True
while run:
    # background
    window.blit(background, (0, 0))
    
    # Check events
    for e in event.get():
        if e.type == QUIT:
            run = False
        # Check for key presses
        if e.type == KEYDOWN:
            # If SPACE is pressed, fire the fireball
            if e.key == K_SPACE and fireball_state == "ready":
                fireball_rect.x = spaceship_rect.x
                fireball_state = "fire"
                fireball_sound.play()

    # Spaceship movement
    keys_pressed = key.get_pressed()
    if keys_pressed[K_LEFT]:
        spaceship_rect.x -= SPACESHIP_MOVE_STEP
    if keys_pressed[K_RIGHT]:
        spaceship_rect.x += SPACESHIP_MOVE_STEP

    # Bound spaceship within window
    if spaceship_rect.x <= 0:
        spaceship_rect.x = 0 
    elif spaceship_rect.x >= MAX_SPACESHIP_X:
        spaceship_rect.x = MAX_SPACESHIP_X

    # Handle enemies
    for i in range(NUM_OF_ENEMIES):
        window.blit(enemy_imgs[i], enemy_rects[i]) 

        # Move the enemies
        enemy_rects[i].x += enemyX_change[i] 
        if enemy_rects[i].x > WINDOW_WIDTH - ENEMY_WIDTH:  
            enemyX_change[i] = -ENEMY_X_CHANGE    
            enemy_rects[i].y += ENEMY_Y_CHANGE
        elif enemy_rects[i].x < 0: 
            enemyX_change[i] = ENEMY_X_CHANGE  
            enemy_rects[i].y += ENEMY_Y_CHANGE 

        # Game Over condition
        if enemy_rects[i].y > GAME_OVER_Y_THRESHOLD:
            for j in range(NUM_OF_ENEMIES):
                enemy_rects[j].y = 2000  # Move enemies off the screen
            over_text = over_font.render("GAME OVER", True, COLOR_WHITE)
            window.blit(over_text, (180, 250))
            break 
        
        # Collision detection
        if enemy_rects[i].colliderect(fireball_rect) and fireball_state == "fire":
            fireball_rect.y = spaceship_rect.y 
            fireball_state = "ready"
            enemy_rects[i].x = random.randint(0, WINDOW_WIDTH - ENEMY_WIDTH) 
            enemy_rects[i].y = random.randint(50, 150) 
            score_value += 1

    # Display score
    score = score_font.render(f"Score: {score_value}", True, COLOR_WHITE) 
    window.blit(score, (10, 10))

    # Handle fireball movement
    if fireball_rect.y < MAX_FIREBALL_Y:
        fireball_rect.y = spaceship_rect.y 
        fireball_state = "ready"

    if fireball_state == "fire": 
        window.blit(fireball_surf, (fireball_rect.x + 16, fireball_rect.y + 10))
        fireball_rect.y -= FIREBALL_Y_STEP 

    # Draw spaceship
    window.blit(spaceship_surf, spaceship_rect)

    # Update the display and control the frame rate
    clock.tick(CLOCK_TICK_RATE)
    display.update()
