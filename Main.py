import pygame #Подключаем библиотеку pygame.
import pygame_menu #Подключаем библиотеку pygame-menu.
from random import randint #Подключаем функцию randint из библиотеки random
import sys
import os

def resource_path(relative_path):
    """Правильно находит файлы и в .py, и в .exe"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

#параметры окна
WIDTH = 1200 #Ширина окна
HEIGHT = 800 #Высота окна
#Создаем игру и окно.
pygame.init() #Инициализируем модули pygame.
pygame.display.set_caption('Охотник за пузырями') #Заголовок окна.
window = pygame.display.set_mode((WIDTH, HEIGHT)) #Задаём размеры игровому окну.
clock = pygame.time.Clock() #Кол-во кадров в секунду.
icon = pygame.image.load(resource_path('image/player/right/player_right_1.png')) #Задём картинку для иконки.
pygame.display.set_icon(icon) #Иконка игры
font = pygame.font.SysFont('Comic Sans MS', 30)
#Задний фон для меню
bg_image = pygame.transform.scale(pygame.image.load(resource_path('image/background/bg.jpg')).convert(), (WIDTH, HEIGHT))
#Меню поражения игрока
def game_over_menu():
    #Текст, который будет написан в меню.
    game_over_text = "Вы проиграли, не расстраивайтесь!"\
                      "Вы можете попробовать ещё раз."
    game_over_menu = pygame_menu.Menu('Игра окончена!',600,400, theme=main_theme) #Заголовок и размеры меню
    game_over_menu.add.label(game_over_text, max_char=-1,font_size=30, font_color = (0, 0, 139))
    game_over_menu.add.button('Cыграть ещё раз', start_the_game, font_color=(0, 0, 139))
    game_over_menu.add.button('Выход', pygame_menu.events.EXIT, font_color=(0, 0, 139))
    #Отображение меню на экране.
    while True:
    #Задний фон для меню
     window.blit(bg_image, (0,0))
     events = pygame.event.get()
     for event in events:
      if event.type == pygame.QUIT:
         pygame.quit()
         sys.exit()                    # ← ИСПРАВЛЕНО
     if game_over_menu.is_enabled():
        game_over_menu.update(events)
        game_over_menu.draw(window)
     pygame.display.update()
#Меню победы игрока
def game_win_menu():
    game_win_text = "Поздравляю! Вы победили!!!" #Текст, который будет написан в меню
    game_win_menu = pygame_menu.Menu('Победа!', 600,400,theme=main_theme) #Заголовок и размеры меню
    game_win_menu.add.label(game_win_text, max_char=-1,font_size=30, font_color = (0, 0, 139))
    game_win_menu.add.button('Сыграть ещё раз',start_the_game, font_color=(0, 0, 139))
    game_win_menu.add.button('Выход', pygame_menu.events.EXIT, font_color=(0, 0, 139))
    
    #Отображение меню на экране.
    while True:
     #Задний фон для меню
      window.blit(bg_image, (0,0))
      events = pygame.event.get()
      for event in events:
       if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()                    # ← ИСПРАВЛЕНО
      if game_win_menu.is_enabled():
         game_win_menu.update(events)
         game_win_menu.draw(window)
      pygame.display.update()
#Функция, которая запускает игру, когда мы в меню нажимаем на кнопку "Играть"
def start_the_game():
 game_timer = 30 #Игровой таймер. Изначальное значение 30 секунд.
 seconds = 0 #Кол-во секунд, которое прошло с начала игры.
 next_goal = 1000 #Кол-во очков, чтобы продлить таймер.
 font = pygame.font.SysFont('Comic Sans MS', 30) #Шрифт для надписей
 #Загружаем задний фон игры и масштабируем его под размер окна, чтобы была видна картинка полностью.Так же конвертируем картинку в более удобный формат для pygame.
 background = pygame.transform.scale(pygame.image.load(resource_path('image/background/bg.jpg')).convert(), (WIDTH, HEIGHT))
 #Класс игрока (лодки)
 class Player:
    def __init__(self, window):
        self.index = 0 #Переменная для списков с текстурами лодки.
        #Список картинок для перемещения в право.
        self.move_right = [pygame.transform.scale(pygame.image.load(resource_path('image/player/right/player_right_1.png')).convert_alpha(), (64, 64)),
                           pygame.transform.scale(pygame.image.load(resource_path('image/player/right/player_right_2.png')).convert_alpha(), (64, 64)),
                           pygame.transform.scale(pygame.image.load(resource_path('image/player/right/player_right_3.png')).convert_alpha(), (64, 64)),
                           pygame.transform.scale(pygame.image.load(resource_path('image/player/right/player_right_4.png')).convert_alpha(), (64, 64)),
                           pygame.transform.scale(pygame.image.load(resource_path('image/player/right/player_right_5.png')).convert_alpha(), (64, 64)),
                           pygame.transform.scale(pygame.image.load(resource_path('image/player/right/player_right_6.png')).convert_alpha(), (64, 64))]
        #Список картинок для перемещения в лево.
        self.move_left = [pygame.transform.scale(pygame.image.load(resource_path('image/player/left/player_left_1.png')).convert_alpha(), (64, 64)),
                          pygame.transform.scale(pygame.image.load(resource_path('image/player/left/player_left_2.png')).convert_alpha(), (64, 64)),
                          pygame.transform.scale(pygame.image.load(resource_path('image/player/left/player_left_3.png')).convert_alpha(), (64, 64)),
                          pygame.transform.scale(pygame.image.load(resource_path('image/player/left/player_left_4.png')).convert_alpha(), (64, 64)),
                          pygame.transform.scale(pygame.image.load(resource_path('image/player/left/player_left_5.png')).convert_alpha(), (64, 64)),
                          pygame.transform.scale(pygame.image.load(resource_path('image/player/left/player_left_6.png')).convert_alpha(), (64, 64))]
          
        self.window = window #инициализируем игрока(лодку) на экране.
        self.image = self.move_right[self.index]
        #Создаём прямоугольную область для игрока(лодки) и распологаем игрока в центре экрана.
        self.rect = self.image.get_rect(center=(600, 400))
        self.speed = 4 #Скорость лодки
    def update(self):
        self.image = self.move_right[self.index] #делаем анимацию лодки, когда игрок не нажимает на клавиши.
        #Управление лодкой
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]and self.rect.x < 1135:
            self.image = self.move_right[self.index]
            self.rect.x += self.speed
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.image = self.move_left[self.index]
            self.rect.x -= self.speed
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]and self.rect.y < 735:
            self.rect.y += self.speed
        #Смена картинок лодки для анимации.
        if self.index < 5:
           self.index += 1
        else:
            self.index = 0
        #Накладываем текстуру игрока на наш экран и передаём его координаты.
        self.window.blit(self.image, self.rect)
    score = 0 #Очки игрока.Изначально это значение равно 0.
    
 player = Player(window)
 #Класс пузырей.
 class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
       super().__init__()
       #Загружаем картинку для пузырей.
       self.image = pygame.transform.scale(pygame.image.load(resource_path('image/enemy/enemy.png')).convert_alpha(), (35, 35))
       #Создаём прямоугольную область для пузырей.
       self.rect = self.image.get_rect()
       #Скорость пузырей
       self.speed = speed
       #Спавн пузырей.
       self.rect.x = randint(0, 1135)
       self.rect.y = randint(0, 735)
    #Респавн пузырей
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
        self.rect.x -= self.speed #Передвижение пузырей
        #Если пузырь заходит за границу окна, то мы его спавним заново.
        if self.rect.x < 0:
            self.respawn()
        #Протыкание пузырей игроком.
        if abs(self.rect.x - player.rect.x) < 50 and abs(self.rect.y - player.rect.y) < 50:
            self.respawn()
            player.score += 100
    #Отображение пузырей на экране.
    def draw(self, window):
        window.blit(self.image, self.rect)
 enemy = Enemy(2)
 enemies = pygame.sprite.Group()
 #Получаем время, тики, когда игра только запускается.
 start_ticks_amount = pygame.time.get_ticks()
 # Цикл игры
 run = True #Флаг
 while run:
     # Ввод процесса (события).
     for event in pygame.event.get():
         if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()                    # ← ИСПРАВЛЕНО
     #Получаем эти же тики и отбавляем от них тики, которые были во время запуска.
     #А потом делим на 1000 т.к в pygame 1 тик = 1мс
     seconds = (pygame.time.get_ticks() - start_ticks_amount)/1000
     #Отображаем надписи с кол-вом очков и игровым временем.
     score_label = font.render('Очки: ' + str(player.score) + '. Время: ' + str(int(game_timer - seconds)), False, (255,0,0))
     window.blit(background, (0, 0)) #Применяем задний фон на наш экран и располагаем его на координатах x=0 и y=0, чтобы фон применился на весь экран.
     player.update() #Обновляем игрока(лодку) на экране.
     #Обновляем и отображаем пузыри на экране.
     enemy.update()
     enemy.draw(window)
     enemies.update()
     enemies.draw(window)
     #Если пузырей меньше 8, то мы спавним новые пузыри.
     if len(enemies) < 8:
         #Скорость берем рандомную от 1 до 4
         enemy = Enemy(randint (1, 4))
         enemies.add(enemy)
     window.blit(score_label, (10,0)) #Отображаем и даем координаты для надписи с таймером и очками.
     pygame.display.update() #Обновление картинки на экране
     clock.tick(75)
     #Если игрок набирает 1000 очков, то время увеличивается на 30 секунд.
     if player.score >= next_goal:
          next_goal += 1000
          game_timer += 30
     #Если время закончилось, то откроется меню поражения.
     if seconds >= game_timer:
        event.type = game_over_menu()
     #Если игрок набрал 5000 очков, то откроется меню победы.
     if player.score >= 5000:
        event.type = game_win_menu()
       
#Главное Меню
main_theme = pygame_menu.themes.THEME_BLUE.copy()
main_theme.set_background_color_opacity(0.7) #Прозрачность
menu = pygame_menu.Menu('Охотник за пузырями', 500, 250, theme=main_theme)
#Правила игры, которые будут написаны в меню.
rules = 'Добро пожаловать в игру "Охотник за пузырями." '\
        'Вы должны управлять подводной лодкой.'\
        'Стрелками лодка перемещается.'\
        'За протыкание пузырей начисляются очки.'\
        'Первоначальное время 30 секунд.'\
        'Каждая 1000 очков добавляет время.'\
        'Игра заканчивается, когда истекает время. '\
        'Желаем удачи!'
rules_menu = pygame_menu.Menu('Правила игры',1000, 700, theme=main_theme)
rules_menu.add.label(rules, max_char=-1,font_size=30, font_color = (0, 0, 139))
rules_menu.add.button('Вернуться в главное меню', pygame_menu.events.BACK)
#Кнопки главного меню
menu.add.button('Правила игры', rules_menu, font_color=(0, 0, 139))
menu.add.button('Играть', start_the_game, font_color=(0, 0, 139))
menu.add.button('Выход', pygame_menu.events.EXIT, font_color=(0, 0, 139))
#Отображение меню на экране.
while True:
#Задний фон для меню
    window.blit(bg_image, (0,0))
    events = pygame.event.get()
    for event in events:
     if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()                        
    if menu.is_enabled():
        menu.update(events)
        menu.draw(window)
    pygame.display.update()
