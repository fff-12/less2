from pygame import *

game = True
win_width = 700
win_height = 500
clock = time.Clock()
fps = 60

wind = display.set_mode((700, 500))
background = transform.scale(image.load('starsbg.jpg'), (700, 500))
display.set_caption('Maze')

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, sprite_x, sprite_y, sprite_wigth, sprite_height, sprite_speed): 
        super().__init__()
        self.image = transform.scale(image.load(sprite_image),(sprite_wigth, sprite_height))
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y
        self.speed = sprite_speed

    def reset(self):
        wind.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

pic1 = Player('ufo_1.png', 5, win_height - 80, 65, 65, 4)
final = GameSprite('Asset 28@4x.png', win_width - 120, win_height - 80, 65, 65, 0)
'''monster = Enemy('monster_4.png', win_width - 80, 280, 65, 65, 2)'''

while game:
    time.delay(60)
    for i in event.get():
        if i.type == QUIT:
            game = False

    wind.blit(background, (0, 0))
    pic1.update()
    pic1.reset()
    final.reset()
    
    display.update()
    clock.tick(fps)