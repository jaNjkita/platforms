import pygame # Выполняет импорт основного модуля
import classes # Импортируем модули
from random import randint
pygame.init() # Импортирует отедльные функции всех модулей

sc = pygame.display.set_mode((0,0),pygame.FULLSCREEN) 
size_sc = pygame.display.get_window_size() #Функция возвращет размеры клиентской области (возвращает кортеж)
W = size_sc[0] # Ширина экрана
H = size_sc[1] # Высота экрана

# Объявление важных переменных
clock = pygame.time.Clock()
flRunnung = True
FPS = 30
animCount = 0 # Количество проигранных движения анимаций (указывает какая анимация из 6 проигрывается)
animCount_2 = 0 # Счётчик для другой анимации  
fps_count = 0 # счётчик кадров для падения
ground = H - 125 # Уровень лавы
ceiling = 125 # Уровень сталактитов
move_past = 'игрок стоит на месте'
end = False # переменная отвечает закончена ли игра

# Фоновое иизображение
bg = pygame.image.load(r'фон2.jpg')

                                       # Платформы
# Создание платформ
size_platforms = (W//10 + 50, H//25) # Размеры платформ (одиннаковые)
# Объявление платформ
top_left_plat = classes.Platforms(r'верх_платформа.png', size_platforms, (2*W//5 + 60, H//3 + 50))
top_right_plat = classes.Platforms(r'верх_платформа.png', size_platforms, (4*W//5 - 60, H//3 + 50))
bottom_left_plat = classes.Platforms(r'нижн_платформа.png', size_platforms, (2*W//5 + 60, 2*H//3 - 25))
bottom_right_plat = classes.Platforms(r'нижн_платформа.png', size_platforms, (4*W//5 - 60, 2*H//3 - 25))
center_plat = classes.Platforms(r'сред_платформа.png', size_platforms, (3*W//5, H//2 + 25))

tuple_plat = (center_plat, top_left_plat, top_right_plat, bottom_left_plat, bottom_right_plat) #Кортеж хранящий платформы


                                        # Башня
surf_tower = pygame.transform.scale(pygame.image.load(r'башня.png').convert_alpha(), (W//6, H - 350))
rect_tower = surf_tower.get_rect(bottomleft = (0, ground))

                                        # Лава
surf_lava = pygame.transform.scale(pygame.image.load(r'лава.png').convert_alpha(), (W, 200)) # по высоте 250
rect_lava = surf_lava.get_rect(topleft =  (0, H - 200))

                                        # Сталактиты
surf_stalactits = pygame.transform.scale(pygame.image.load(r'сталактиты.png').convert_alpha(), (W, 125))
rect_stalactits = surf_stalactits.get_rect(topleft = (0,0))

                                        # Ядра
size_ball = (25,25)
up_ball = classes.Ball(r'ядро.png', size_ball, (275,275), 23, False)
middle_ball = classes.Ball(r'ядро.png', size_ball, (275,438), 23, False)

tuple_balls = (up_ball, middle_ball)

                                       # Пламя
size_blaze = (W//10, 2*H//6)
left_blaze = classes.Blaze(r'пламя.png', size_blaze, (2*W//5 - W//10//2 + 60, 920), False, 0)
right_blaze = classes.Blaze(r'пламя.png', size_blaze, (4*W//5 - W//10//2 - 60, 920), False, 0)

tuple_blazes = (left_blaze, right_blaze)

                                       # Списко всех возможных событий
event_list = [up_ball, middle_ball, left_blaze, right_blaze]

                                       # Персонаж
# Размер персонажа
size_hero = (W//30, H//9)

# Анимация (в кортежах поверхности)
run_right = (pygame.transform.scale(pygame.image.load(r'правый_бег_1.png').convert_alpha(),size_hero),
             pygame.transform.scale(pygame.image.load(r'правый_бег_2.png').convert_alpha(),size_hero),
             pygame.transform.scale(pygame.image.load(r'правый_бег_3.png').convert_alpha(),size_hero),
             pygame.transform.scale(pygame.image.load(r'правый_бег_4.png').convert_alpha(),size_hero),
             pygame.transform.scale(pygame.image.load(r'правый_бег_5.png').convert_alpha(),size_hero),
             pygame.transform.scale(pygame.image.load(r'правый_бег_6.png').convert_alpha(),size_hero))

run_left = (pygame.transform.scale(pygame.image.load(r'левый_бег_1.png').convert_alpha(),size_hero),
            pygame.transform.scale(pygame.image.load(r'левый_бег_2.png').convert_alpha(),size_hero),
            pygame.transform.scale(pygame.image.load(r'левый_бег_3.png').convert_alpha(),size_hero),
            pygame.transform.scale(pygame.image.load(r'левый_бег_4.png').convert_alpha(),size_hero),
            pygame.transform.scale(pygame.image.load(r'левый_бег_5.png').convert_alpha(),size_hero),
            pygame.transform.scale(pygame.image.load(r'левый_бег_6.png').convert_alpha(),size_hero))

stand_right = (pygame.transform.scale(pygame.image.load(r'правый_стоит.png').convert_alpha(), size_hero),
               pygame.transform.scale(pygame.image.load(r'правый_моргает.png').convert_alpha(), size_hero))

stand_left = (pygame.transform.scale(pygame.image.load(r'левый_стоит.png').convert_alpha(), size_hero),
              pygame.transform.scale(pygame.image.load(r'левый_моргает.png').convert_alpha(), size_hero))

fly_left = (pygame.transform.scale(pygame.image.load(r'левый_прыжок_1.png').convert_alpha(), size_hero),
            pygame.transform.scale(pygame.image.load(r'левый_прыжок_2.png').convert_alpha(), size_hero),
            pygame.transform.scale(pygame.image.load(r'левый_прыжок_3.png').convert_alpha(), size_hero))

fly_right = (pygame.transform.scale(pygame.image.load(r'правый_прыжок_1.png').convert_alpha(), size_hero),
             pygame.transform.scale(pygame.image.load(r'правый_прыжок_2.png').convert_alpha(), size_hero),
             pygame.transform.scale(pygame.image.load(r'правый_прыжок_3.png').convert_alpha(), size_hero))

hero_died = pygame.transform.scale(pygame.image.load(r'смерть.png').convert_alpha(), (W//20, H//20))


# Объявление персонажа
hero = classes.Hero(r'C:\Users\GigaByte\Desktop\Nikita\project\content\персонаж_стоит.png',
                    size_hero, (center_plat.rect.center[0], center_plat.rect.top), 9, H//5,
                    15, 1, False, False, False, False, False)

# концовка игры
pictures_lose = pygame.transform.scale(pygame.image.load(r'lose.png').convert_alpha(), (W, H))


                                        # Музыка
music = pygame.mixer.music.load(r'музыка.mp3')
pygame.mixer.music.play(-1)

def end_of_game(): # она будет выводить поверхность , что игра закончена (вызывается в последнюю очередь)
    global end
    end = True #переменная говорит игра закончена
    pygame.mixer.music.stop()
    sc.blit(pictures_lose, (0,0))
    if event.type == pygame.MOUSEBUTTONDOWN:
        end = False
        hero.died = False
        pygame.mixer.music.play(-1)
        hero.rect.bottomleft = (center_plat.rect.center[0], center_plat.rect.top)


    
   
        

def call_event():
    global fps_count
    if fps_count > 60:
        fps_count = 0
    if fps_count == 60: # Если проиграно 45 кадров, то пушка стреляет (каждые 1,5 секунды)
        while True:
            first_event = randint(0,3) # выбор первого события
            second_event = randint(0,3) # выбор второго события
            events = (first_event, second_event) # создание кортежа
            if first_event != second_event:
                break
        for event in events:
            if event < 2: # Если событий имеет номер меньший чем два, то это выстрел из пушки (под номером 0 или 1)
               event_list[event].bum = True
               event_list[event].shot(W)
            else: # иначе это событие вспышки лавы
                event_list[event].be = True # идёт вспышка лавы
                event_list[event].flash()
    fps_count += 1 # увеличиваем счётчик кадров
    for ball in tuple_balls:
        if ball.bum == True:
            ball.shot(W)
            sc.blit(ball.image, ball.rect)
    for blaze in tuple_blazes:
        if blaze.be == True:
            blaze.flash()
            sc.blit(blaze.image, blaze.rect)
    
                
    

def draw_image(): # Функция размещает текстуры
    sc.blit(bg, (0,0))
    sc.blit(surf_tower, rect_tower)
    for plat in tuple_plat:
        sc.blit(plat.image, plat.rect)
        
        
def animation(): # Функция анимации персонажа
    global animCount
    global animCount_2
    global move_past
    if animCount +1 >= 30:
        animCount = 0

    if hero.died == True:
        hero.image = hero_died
    else:
        if hero.jump_p == True:
            if hero.left == True and hero.right == False:
                hero.image = fly_left[0]
            elif hero.right == True and hero.left == False:
                hero.image = fly_right[0]
            elif hero.left == False and hero.right == False:
                hero.image = fly_right[0]
        elif hero.fall_p == True: # Если он летит, но не в прыжке, то тогда
            if hero.left == True and hero.right == False:
                hero.image = fly_left[1]
            elif hero.right == True and hero.left == False:
                hero.image = fly_right[1]
            elif hero.left == False and hero.right == False:
                hero.image = fly_right[1]
        else:
            if hero.left == False and hero.right == False: 
                animCount = 0
                if animCount_2 > 60:
                    animCount_2 = 0
                if move_past == 'игрок двигался на лево':
                    if animCount_2 < 50:
                        hero.image = stand_left[0]
                    else:
                        hero.image = stand_left[1]
                elif move_past == 'игрок двигался на право':
                    if animCount_2 < 50:
                        hero.image = stand_right[0]
                    else:
                        hero.image = stand_right[1]
                animCount_2 += 1
            elif hero.left == True and hero.right == False:
                hero.image = run_left[animCount//5]
                animCount += 1
                move_past = 'игрок двигался на лево'
            elif hero.right == True and hero.left == False:
                hero.image = run_right[animCount//5]
                animCount += 1
                move_past = 'игрок двигался на право'
    sc.blit(hero.image, hero.rect)
            
            
            


# Создаём игровой цикл
while flRunnung:
    hero.run(tuple_plat)
    hero.die(ground, ceiling, tuple_balls, tuple_blazes)
    hero.check(tuple_plat)
    draw_image()
    call_event()
    animation()
    sc.blit(surf_lava, rect_lava) #Лава рисуется после анимации
    sc.blit(surf_stalactits, rect_stalactits)

    if hero.jump_p == True:
        hero.jump()
        
    if hero.fall_p == True:
        hero.fall(tuple_plat)

    if hero.died == True or end == True : # Если игрок умер, то вызывается функция конца игры
        end_of_game()
        
        
    pygame.display.update()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                flRunnung = False
            elif event.key == pygame.K_UP:
                if hero.jump_p == False and hero.fall_p == False:
                    hero.jump()


