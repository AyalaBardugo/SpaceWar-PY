import os
from pygame import image, transform, mixer
from constants import *

def load_game_files():
    """
    Load all game assets including images and sounds
    Returns: Tuple containing all loaded game assets
    """
    current_dir = os.path.dirname(__file__)
    
    # Load images
    background = image.load(os.path.join(current_dir, "images", "background.png"))
    
    spaceship_surf = image.load(os.path.join(current_dir, "images", "spaceship.png"))
    spaceship_surf = transform.scale(spaceship_surf, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
    
    enemy = image.load(os.path.join(current_dir, "images", "enemy.png"))
    enemy.set_colorkey(COLOR_BLACK)
    enemy = transform.scale(enemy, (ENEMY_WIDTH, ENEMY_HEIGHT))
    
    fireball_surf = image.load(os.path.join(current_dir, "images", "fireball.png"))
    fireball_surf = transform.scale(fireball_surf, (FIREBALL_WIDTH, FIREBALL_HEIGHT))
    
    # Load sounds
    music_background = mixer.Sound(os.path.join(current_dir, "sounds", "background.mp3"))
    fireball_sound = mixer.Sound(os.path.join(current_dir, "sounds", "fireball.mp3"))
    
    return background, spaceship_surf, enemy, fireball_surf, music_background, fireball_sound