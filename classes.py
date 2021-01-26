import pygame
pygame.init()

class Platforms:
    def __init__(self, filename, size, location):
        self.image = pygame.transform.scale((pygame.image.load(filename).convert_alpha()), size) # изображение
        self.rect = self.image.get_rect(center = location) # Потом напишем координаты #Прямоугольная область


class Hero:
    def __init__(self, filename, size, location,
                 speed_run, height_jump, speed_jump, gravitation, jump_p, fall_p, left, right, died): 
        self.image = pygame.transform.scale((pygame.image.load(filename).convert_alpha()), size) # изображение
        self.rect = self.image.get_rect(bottomleft = location)
        self.speed_run = speed_run
        self.height_jump = height_jump
        self.speed_jump = speed_jump
        self.jump_p = jump_p # Закончился ли прыжок (взлёт или нет)
        self.gravitation = gravitation
        self.rise = 0 # Переменная отвечает за подъём с момента прыжка
        self.fall_p = fall_p # Переменная отвечает находится ли персонаж в падении
        self.left = left
        self.right = right
        self.died = died
        self.fps_count = 0
        
# У нас прыжок и падение - это два разных процесса. И соответсвенно у нас есть две переменные,
# которые говорят находится ли герой в прыжке или в падении!!! 



    def run(self, plats): # Функция бега
        if self.died == False:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] == 1:
                self.rect.left = self.rect.left - self.speed_run
                self.left = True
                self.right = False
            elif keys[pygame.K_RIGHT] == 1: 
                self.rect.right = self.rect.right + self.speed_run
                self.left = False
                self.right = True
            else:
                self.left = False
                self.right = False


    def jump(self): # Если герой нажал на клавишу вызывается Функция прыжка
        if self.died == False:
            self.jump_p = True # герой находится в прыжке
            self.rise += self.speed_jump
            if self.rise < self.height_jump: # Если высота подъёма меньше допусмой, то игрок поднимается вверх
                self.rect.top = self.rect.top - self.speed_jump 
            else:
                self.jump_p = False # то есть прыжок закончен
                self.fall_p = True # Начинается процесс падения
                self.rise = 0 # сбрасывается высота подъёма с момента прыжка
                
        else:
            self.fall_p = True
          
        

    def fall(self, plats): # принимает платформы
        if self.fps_count > 12:
           self.fps_count = 0 
        for plat in plats:
            if not(plat.rect.center[1] - 40 <= self.rect.bottom <= plat.rect.center[1] + 40):
                self.rect.bottom += self.gravitation
                if self.fps_count == 12:
                     self.gravitation += 1
            else:
                if plat.rect.topleft[0] <= self.rect.center[0] <= plat.rect.topright[0]:
                    self.rect.bottom = plat.rect.top
                    self.fall_p = False
                    self.gravitation = 1
                else:
                    self.rect.bottom += self.gravitation
                    if self.fps_count == 5:
                        self.gravitation += 1
        self.fps_count += 1
               
                    

    def check(self, plats):
        if self.died == False:
            info_list = [] # Список с информацией на каких платформах стоит игрок
            for plat in plats:
                if not(plat.rect.topleft[0] <= self.rect.center[0] <= plat.rect.topright[0]):
                    info_list.append(0) # если игрок не на платформе, то в список добавляется 0
                else:
                    info_list.append(1) # если игрок на платформе, то в список добавляется единица     
            if info_list.count(0) == 5 and self.jump_p == False: # Если в списке все 0, то игрок падает!
                self.fall_p = True

    def die(self, ground, ceiling, balls, blazes): # функция принимает уровень земли
        if self.rect.bottom >= ground or self.rect.top <= ceiling:
            self.died = True
        for ball in balls:
            balls_rects_info = (ball.rect.topleft, ball.rect.topright, ball.rect.bottomright, ball.rect.bottomleft) # Кортеж хранит свойства шаров
            for i in balls_rects_info:
                if self.rect.left <= i[0] <= self.rect.right and self.rect.top <= i[1] <= self.rect.bottom:
                    self.died = True
                    break
        hero_rects_info = (self.rect.topleft, self.rect.topright, self.rect.bottomright, self.rect.bottomleft)
        for blaze in blazes:
            for i in hero_rects_info:
                if blaze.rect.top <= i[1] <= blaze.rect.bottom and blaze.rect.left <= i[0]<= blaze.rect.right:
                    if blaze.be == True:
                        self.died = True
                        break

            
        
                    
            
            

class Ball:
    def __init__(self, filename, size, location, speed, bum): 
        self.image = pygame.transform.scale(pygame.image.load(filename).convert(), size)
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect(center = location)
        self.location = location
        self.speed = speed
        self.bum = bum # переменная говорит летит ли снаряд

    def shot(self, W): # Если происходит выстрел, то вызывается функция
        self.rect.left += self.speed # и расположение снаяда начинает меняться
        if self.rect.left > W:
            self.bum = False # ядро перестаёт лететь
            self.rect.center = self.location

class Blaze:
    def __init__(self, filename, size, location, be, time):
        self.image = pygame.transform.scale((pygame.image.load(filename).convert_alpha()), size)
        self.rect = self.image.get_rect(bottomleft = location) # Вспышка будет во всю длину платформы
        self.be = be # Переменная говорит идёт ли лава или нет
        self.time = time # счётчик кадров для пламени

    def flash(self):
        self.time += 1
        if self.time > 15: # Если пламя стоит больше 10 кадров, то оно исчезает (полсеукнды)
            self.be = False
            self.time = 0

        
    

 # именно потому что вспышка идёт во всю длину платформы нам будет нужно размещать вспышку по середине платформы
 # location хранит кортеж расположения пламени
 # и во всю длину
            
        


   


                       
    
