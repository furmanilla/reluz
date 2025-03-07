import random
from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (30, 30))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed

    def reset(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color, wall_x, wall_width, hole_height):
        super().__init__()
        self.color = color
        self.width = wall_width
        self.hole_height = hole_height  

        # Випадкова висота верхньої стіни
        self.height_top = random.randint(10, win_height - hole_height - 10)  
        self.height_bottom = win_height - (self.height_top + self.hole_height) 

        # Створення верхньої стіни
        self.top_wall = Surface((self.width, self.height_top))
        self.top_wall.fill(self.color)
        self.top_rect = self.top_wall.get_rect()
        self.top_rect.x = wall_x
        self.top_rect.y = 0  # Верхня стіна знаходиться вгорі екрану

        # Створення нижньої стіни
        self.bottom_wall = Surface((self.width, self.height_bottom))
        self.bottom_wall.fill(self.color)
        self.bottom_rect = self.bottom_wall.get_rect()
        self.bottom_rect.x = wall_x
        self.bottom_rect.y = self.height_top + self.hole_height  # Нижня стіна під проміжком

    def update(self):
        # Рух стін вліво
        self.top_rect.x -= 1
        self.bottom_rect.x -= 1

        # Якщо стіна виходить за межі екрану, її позиція відновлюється
        if self.top_rect.x < -self.width:
            self.top_rect.x = win_width
            self.bottom_rect.x = win_width
            self.height_top = random.randint(10, win_height - self.hole_height - 10)  # Нова висота верхньої стіни
            self.height_bottom = win_height - (self.height_top + self.hole_height)  # Нова висота нижньої стіни
            self.bottom_rect.y = self.height_top + self.hole_height

    def draw_wall(self, window):
        # Малюємо верхню та нижню стіну
        window.blit(self.top_wall, self.top_rect)
        window.blit(self.bottom_wall, self.bottom_rect)

def check_collisions(player, walls):
    for wall in walls:
        if player.rect.colliderect(wall.top_rect) or player.rect.colliderect(wall.bottom_rect):
            return True  
    return False  

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Flappy Bir')


background = transform.scale(image.load("bg.png"), (win_width, win_height))


player = Player('birdup.png', 1, win_height - 80, 4)


walls = []


hole_height = 150 


for i in range(5):
    wall = Wall((120, 150, 50), win_width + i * 300, 50, hole_height)
    walls.append(wall)


game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.blit(background, (0, 0))  
    player.update()  

    if check_collisions(player, walls): 
        game = False  

    player.reset(window)  

    for wall in walls:
        wall.update()
        wall.draw_wall(window)

    display.update()

quit() 