import random
from pygame import init, display, Rect, font
from constants import *
from game_assets import load_game_files

def initialize_game():
    """
    Initialize the game, create game window and setup all game objects
    Returns: Tuple containing all initialized game objects and assets
    """
    # Initialize pygame
    init()
    
    # Set up game window
    window = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    display.set_caption("Space War")
    
    # Load all game assets
    background, spaceship_surf, enemy, fireball_surf, music_background, fireball_sound = load_game_files()
    
    # Start background music
    music_background.play()
    
    # Create spaceship
    spaceship_rect = Rect(300, 400, spaceship_surf.get_width(), spaceship_surf.get_height())
    
    # Create enemies
    enemy_imgs = []
    enemy_rects = []
    enemyX_change = []
    
    for i in range(NUM_OF_ENEMIES):
        enemy_imgs.append(enemy)
        enemy_rects.append(Rect(
            random.randint(0, WINDOW_WIDTH - ENEMY_WIDTH),
            random.randint(50, 150),
            enemy_imgs[-1].get_width(),
            enemy_imgs[-1].get_height()
        ))
        enemyX_change.append(ENEMY_X_CHANGE)
    
    # Create fireball
    fireball_rect = Rect(0, spaceship_rect.y, fireball_surf.get_width(), fireball_surf.get_height())
    
    # Setup fonts
    over_font = font.SysFont("Calibri", 80)
    score_font = font.SysFont("Calibri", 30)
    
    return (window, background, spaceship_surf, spaceship_rect, enemy_imgs, enemy_rects, 
            enemyX_change, fireball_surf, fireball_rect, fireball_sound, over_font, score_font)