import pygame
import pygame_menu
from random import randint
import sys
import os

def resource_path(relative_path):
    """Get the correct path for files when running as .py or as .exe"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Game window settings
WIDTH = 1200
HEIGHT = 800

# Initialize the game and window
pygame.init()
pygame.display.set_caption('Bubble Hunter')
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load game icon
icon = pygame.image.load(resource_path('image/player/right/player_right_1.png'))
pygame.display.set_icon(icon)

font = pygame.font.SysFont('Comic Sans MS', 30)

# Background image for menus
bg_image = pygame.transform.scale(
    pygame.image.load(resource_path('image/background/bg.jpg')).convert(), 
    (WIDTH, HEIGHT)
)

# Game Over menu
def game_over_menu():
    game_over_text = "You lost, don't worry!\nYou can try again."
    game_over_menu = pygame_menu.Menu('Game Over!', 600, 400, theme=main_theme)
    game_over_menu.add.label(game_over_text, max_char=-1, font_size=30, font_color=(0, 0, 139))
    game_over_menu.add.button('Play Again', start_the_game, font_color=(0, 0, 139))
    game_over_menu.add.button('Exit', pygame_menu.events.EXIT, font_color=(0, 0, 139))
    
    while True:
        window.blit(bg_image, (0, 0))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if game_over_menu.is_enabled():
            game_over_menu.update(events)
            game_over_menu.draw(window)
        pygame.display.update()

# Victory menu
def game_win_menu():
    game_win_text = "Congratulations! You won!!!"
    game_win_menu = pygame_menu.Menu('Victory!', 600, 400, theme=main_theme)
    game_win_menu.add.label(game_win_text, max_char=-1, font_size=30, font_color=(0, 0, 139))
    game_win_menu.add.button('Play Again', start_the_game, font_color=(0, 0, 139))
    game_win_menu.add.button('Exit', pygame_menu.events.EXIT, font_color=(0, 0, 139))
    
    while True:
        window.blit(bg_image, (0, 0))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if game_win_menu.is_enabled():
            game_win_menu.update(events)
            game_win_menu.draw(window)
        pygame.display.update()

# Function to start the game
def start_the_game():
    game_timer = 30
    seconds = 0
    next_goal = 1000
    
    # Game background
    background = pygame.transform.scale(
        pygame.image.load(resource_path('image/background/bg.jpg')).convert(), 
        (WIDTH, HEIGHT)
    )

    # Player (submarine) class
    class Player:
        def __init__(self, window):
            self.index = 0
            # Right movement animation
            self.move_right = [
                pygame.transform.scale(pygame.image.load(resource_path('image/player/right/player_right_1.png')).convert_alpha(), (64, 64)),
                pygame.transform.scale(pygame.image.load(resource_path('image/player/right/player_right_2.png')).convert_alpha(), (64, 64)),
                pygame.transform.scale(pygame.image.load(resource_path('image/player/right/player_right_3.png')).convert_alpha(), (64, 64)),
                pygame.transform.scale(pygame.image.load(resource_path('image/player/right/player_right_4.png')).convert_alpha(), (64, 64)),
                pygame.transform.scale(pygame.image.load(resource_path('image/player/right/player_right_5.png')).convert_alpha(), (64, 64)),
                pygame.transform.scale(pygame.image.load(resource_path('image/player/right/player_right_6.png')).convert_alpha(), (64, 64))
            ]
            # Left movement animation
            self.move_left = [
                pygame.transform.scale(pygame.image.load(resource_path('image/player/left/player_left_1.png')).convert_alpha(), (64, 64)),
                pygame.transform.scale(pygame.image.load(resource_path('image/player/left/player_left_2.png')).convert_alpha(), (64, 64)),
                pygame.transform.scale(pygame.image.load(resource_path('image/player/left/player_left_3.png')).convert_alpha(), (64, 64)),
                pygame.transform.scale(pygame.image.load(resource_path('image/player/left/player_left_4.png')).convert_alpha(), (64, 64)),
                pygame.transform.scale(pygame.image.load(resource_path('image/player/left/player_left_5.png')).convert_alpha(), (64, 64)),
                pygame.transform.scale(pygame.image.load(resource_path('image/player/left/player_left_6.png')).convert_alpha(), (64, 64))
            ]
            
            self.window = window
            self.image = self.move_right[self.index]
            self.rect = self.image.get_rect(center=(600, 400))
            self.speed = 4
            self.score = 0

        def update(self):
            self.image = self.move_right[self.index]
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] and self.rect.x < 1135:
                self.image = self.move_right[self.index]
                self.rect.x += self.speed
            if keys[pygame.K_LEFT] and self.rect.x > 0:
                self.image = self.move_left[self.index]
                self.rect.x -= self.speed
            if keys[pygame.K_UP] and self.rect.y > 0:
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN] and self.rect.y < 735:
                self.rect.y += self.speed
            
            # Animation cycle
            if self.index < 5:
                self.index += 1
            else:
                self.index = 0
            
            self.window.blit(self.image, self.rect)

    player = Player(window)

    # Bubble (enemy) class
    class Enemy(pygame.sprite.Sprite):
        def __init__(self, speed):
            super().__init__()
            self.image = pygame.transform.scale(
                pygame.image.load(resource_path('image/enemy/enemy.png')).convert_alpha(), 
                (35, 35)
            )
            self.rect = self.image.get_rect()
            self.speed = speed
            self.rect.x = randint(0, 1135)
            self.rect.y = randint(0, 735)

        def respawn(self):
            rect_x = randint(min(player.rect.x + 300, 1135), 1135)
            rect_x_second = randint(0, max(player.rect.x - 150, 0))
            if randint(0, 1) == 1:
                self.rect.x = rect_x
            else:
                self.rect.x = rect_x_second
            self.rect.y = randint(0, 735)
            self.speed = randint(1, 3)

        def update(self):
            self.rect.x -= self.speed
            if self.rect.x < 0:
                self.respawn()
            # Collision with player
            if abs(self.rect.x - player.rect.x) < 50 and abs(self.rect.y - player.rect.y) < 50:
                self.respawn()
                player.score += 100

        def draw(self, window):
            window.blit(self.image, self.rect)

    enemy = Enemy(2)
    enemies = pygame.sprite.Group()

    start_ticks_amount = pygame.time.get_ticks()

    # Main game loop
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        seconds = (pygame.time.get_ticks() - start_ticks_amount) / 1000
        
        # Score and timer display
        score_label = font.render(f'Score: {player.score} | Time: {int(game_timer - seconds)}', False, (255, 0, 0))
        
        window.blit(background, (0, 0))
        player.update()
        
        enemy.update()
        enemy.draw(window)
        enemies.update()
        enemies.draw(window)
        
        # Spawn new bubbles if there are fewer than 8
        if len(enemies) < 8:
            new_enemy = Enemy(randint(1, 4))
            enemies.add(new_enemy)
        
        window.blit(score_label, (10, 0))
        pygame.display.update()
        clock.tick(75)
        
        # Add 30 seconds every 1000 points
        if player.score >= next_goal:
            next_goal += 1000
            game_timer += 30
        
        # Game Over
        if seconds >= game_timer:
            game_over_menu()
        
        # Victory
        if player.score >= 5000:
            game_win_menu()

# Main menu theme
main_theme = pygame_menu.themes.THEME_BLUE.copy()
main_theme.set_background_color_opacity(0.7)

# Main menu
menu = pygame_menu.Menu('Bubble Hunter', 500, 250, theme=main_theme)

# Rules text
rules_text = (
    "Welcome to Bubble Hunter!\n\n"
    "You control a submarine.\n"
    "Use arrow keys to move.\n"
    "Pop bubbles to score points.\n"
    "You start with 30 seconds.\n"
    "Every 1000 points adds 30 extra seconds.\n"
    "The game ends when time runs out.\n\n"
    "Good luck!"
)

rules_menu = pygame_menu.Menu('How to Play', 1000, 700, theme=main_theme)
rules_menu.add.label(rules_text, max_char=-1, font_size=28, font_color=(0, 0, 139))
rules_menu.add.button('Back', pygame_menu.events.BACK)

# Main menu buttons
menu.add.button('How to Play', rules_menu, font_color=(0, 0, 139))
menu.add.button('Play', start_the_game, font_color=(0, 0, 139))
menu.add.button('Exit', pygame_menu.events.EXIT, font_color=(0, 0, 139))

# Main menu loop
while True:
    window.blit(bg_image, (0, 0))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    if menu.is_enabled():
        menu.update(events)
        menu.draw(window)
    
    pygame.display.update()
