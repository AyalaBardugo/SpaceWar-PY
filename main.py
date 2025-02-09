from pygame import event, QUIT, KEYDOWN, K_SPACE, K_LEFT, K_RIGHT, key, time, display, mouse, MOUSEBUTTONDOWN, Rect, draw
import random
from constants import *
from game_init import initialize_game

def reset_game_state(enemy_rects, spaceship_rect):
    """
    Reset game objects to their initial positions
    """
    # Reset enemy positions
    for i in range(NUM_OF_ENEMIES):
        enemy_rects[i].x = random.randint(0, WINDOW_WIDTH - ENEMY_WIDTH)
        enemy_rects[i].y = random.randint(50, 150)
    
    # Reset spaceship position
    spaceship_rect.x = 300
    spaceship_rect.y = 400
    
    return 0  # Reset score

def draw_button(window, text, font, color, x, y, width, height):
    """
    Draw a button with text and return its rectangle
    """
    button_rect = Rect(x, y, width, height)
    draw.rect(window, color, button_rect, border_radius=10)
    draw.rect(window, COLOR_WHITE, button_rect, 2, border_radius=10)  # Button border
    
    text_surface = font.render(text, True, COLOR_WHITE)
    text_rect = text_surface.get_rect(center=button_rect.center)
    window.blit(text_surface, text_rect)
    
    return button_rect

def main():
    """
    Main game loop - handles all game events and updates
    """
    # Initialize the game
    (window, background, spaceship_surf, spaceship_rect, enemy_imgs, enemy_rects,
     enemyX_change, fireball_surf, fireball_rect, fireball_sound, over_font, score_font) = initialize_game()
    
    clock = time.Clock()
    score_value = 0
    fireball_state = "ready"
    game_active = True
    run = True
    
    # Create buttons (but don't draw them yet)
    restart_button = None
    quit_button = None
    button_color = (70, 70, 70)  # Dark gray
    
    while run:
        # Draw background
        window.blit(background, (0, 0))
        
        # Handle events
        for e in event.get():
            if e.type == QUIT:
                run = False
                
            if game_active:
                if e.type == KEYDOWN and e.key == K_SPACE and fireball_state == "ready":
                    fireball_rect.x = spaceship_rect.x
                    fireball_state = "fire"
                    fireball_sound.play()
            else:
                # Handle button clicks when game is over
                if e.type == MOUSEBUTTONDOWN:
                    mouse_pos = mouse.get_pos()
                    if restart_button and restart_button.collidepoint(mouse_pos):
                        score_value = reset_game_state(enemy_rects, spaceship_rect)
                        game_active = True
                    elif quit_button and quit_button.collidepoint(mouse_pos):
                        run = False
        
        if game_active:
            # Handle spaceship movement
            keys_pressed = key.get_pressed()
            if keys_pressed[K_LEFT] and spaceship_rect.x > 0:
                spaceship_rect.x -= SPACESHIP_MOVE_STEP
            if keys_pressed[K_RIGHT] and spaceship_rect.x < MAX_SPACESHIP_X:
                spaceship_rect.x += SPACESHIP_MOVE_STEP
            
            # Handle enemies
            for i in range(NUM_OF_ENEMIES):
                # Check for game over
                if enemy_rects[i].y > GAME_OVER_Y_THRESHOLD:
                    game_active = False
                    break
                
                # Enemy movement
                enemy_rects[i].x += enemyX_change[i]
                if enemy_rects[i].x >= WINDOW_WIDTH - ENEMY_WIDTH or enemy_rects[i].x <= 0:
                    enemyX_change[i] *= -1
                    enemy_rects[i].y += ENEMY_Y_CHANGE
                
                # Collision detection
                if enemy_rects[i].colliderect(fireball_rect) and fireball_state == "fire":
                    fireball_rect.y = spaceship_rect.y
                    fireball_state = "ready"
                    enemy_rects[i].x = random.randint(0, WINDOW_WIDTH - ENEMY_WIDTH)
                    enemy_rects[i].y = random.randint(50, 150)
                    score_value += 1
                
                # Draw enemy
                window.blit(enemy_imgs[i], enemy_rects[i])
            
            # Handle fireball
            if fireball_rect.y < MAX_FIREBALL_Y:
                fireball_rect.y = spaceship_rect.y
                fireball_state = "ready"
            
            if fireball_state == "fire":
                window.blit(fireball_surf, (fireball_rect.x + 16, fireball_rect.y + 10))
                fireball_rect.y -= FIREBALL_Y_STEP
            
            # Draw spaceship
            window.blit(spaceship_surf, spaceship_rect)
        
        else:  # Game Over state
            over_text = over_font.render("GAME OVER", True, COLOR_WHITE)
            window.blit(over_text, (180, 250))
            
            # Draw buttons
            restart_button = draw_button(window, "Restart", score_font, button_color, 300, 350, 200, 50)
            quit_button = draw_button(window, "Quit", score_font, button_color, 300, 420, 200, 50)
        
        # Always draw score
        score = score_font.render(f"Score: {score_value}", True, COLOR_WHITE)
        window.blit(score, (10, 10))
        
        # Update display
        clock.tick(CLOCK_TICK_RATE)
        display.update()

if __name__ == "__main__":
    main()