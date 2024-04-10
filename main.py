from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, sprite_x, sprite_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(sprite_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(
        self,
        sprite_image,
        sprite_x,
        sprite_y,
        size_x,
        size_y,
        player_x_speed,
        player_y_speed,
    ):

        GameSprite.__init__(self, sprite_image, sprite_x, sprite_y, size_x, size_y)

        self.x_speed = player_x_speed
        self.y_speed = player_y_speed

    def update(self):
        if (
            player.rect.x <= win_width - 40
            and player.x_speed > 0
            or player.rect.x >= 0
            and player.x_speed < 0
        ):
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if (
            self.x_speed > 0
        ): 
            for p in platforms_touched:
                self.rect.right = min(
                    self.rect.right, p.rect.left
                )  # якщо торкнулися відразу кількох, то правий край - мінімальний із можливих
        elif (
            self.x_speed < 0
        ):  # йдемо ліворуч, ставимо лівий край персонажа впритул до правого краю стіни
            for p in platforms_touched:
                self.rect.left = max(
                    self.rect.left, p.rect.right
                )  # якщо торкнулися кількох стін, то лівий край - максимальний
        if (
            player.rect.y <= win_height - 40
            and player.y_speed > 0
            or player.rect.y >= 0
            and player.y_speed < 0
        ):
            self.rect.y += self.y_speed
        # якщо зайшли за стінку, то встанемо впритул до стіни
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:  # йдемо вниз
            for p in platforms_touched:
                self.y_speed = 0
                # Перевіряємо, яка з платформ знизу найвища, вирівнюємося по ній, запам'ятовуємо її як свою опору:
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0:  # йдемо вгору
            for p in platforms_touched:
                self.y_speed = (
                    0  # при зіткненні зі стіною вертикальна швидкість гаситься
                )
                self.rect.top = max(
                    self.rect.top, p.rect.bottom
                )  # вирівнюємо верхній край по нижніх краях стінок, на які наїхали

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.right, self.rect.centery, 15, 20, 9)
        bullets.add(bullet)


class Enemy(GameSprite):
    direction = "left"

    def __init__(self, sprite_image, sprite_x, sprite_y, size_x, size_y, enemy_speed):
        super().__init__(sprite_image, sprite_x, sprite_y, size_x, size_y)
        self.speed = enemy_speed

    def update(self):
        if self.rect.x <= 420:
            self.direction = "right"
        if self.rect.x >= win_width - 40:
            self.direction = "left"
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


class Bullet(GameSprite):
    def __init__(self, sprite_image, sprite_x, sprite_y, size_x, size_y, bullet_speed):
        super().__init__(sprite_image, sprite_x, sprite_y, size_x, size_y)
        self.speed = bullet_speed
        self.image = transform.rotate(self.image, 90)

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width + 1:
            self.kill()


# Створюємо віконц
win_width = 700
win_height = 500
display.set_caption("Лабіринт")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load("starsbg.jpg"), (win_width, win_height))


# Створюємо групу для стін
barriers = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()
# Створюємо стіни картинки


w1 = GameSprite("platform.png", 0, 0, 10, 500)
w2 = GameSprite("platform.png", 690, 0, 10, 500)
w3 = GameSprite("platform.png", 0, 0, 700, 10)
w4 = GameSprite("platform.png", 0, 490, 700, 10)
w5 = GameSprite("platform.png", 0, 420, 50, 10)
w6 = GameSprite("platform.png", 100, 420, 10, 90)
w7 = GameSprite("platform.png", 140, 0, 10, 370)
w99 = GameSprite("platform.png", 0, 100, 70, 10)
w9 = GameSprite("platform.png", 210, 100, 500, 10)
w10 = GameSprite("platform.png", 160, 420, 700, 10)
w11 = GameSprite("platform.png", 70, 100, 10, 270)
w12 = GameSprite("platform.png", 140, 360, 500, 10)
w13 = GameSprite("platform.png", 630, 240, 10, 120)
w14 = GameSprite("platform.png", 200, 240, 430, 10)
w15 = GameSprite("platform.png", 400, 150, 10, 90)
w16 = GameSprite("platform.png", 200, 240, 10, 70)
w17 = GameSprite("platform.png", 200, 310, 380, 10)

barriers.add(w1)
barriers.add(w2)
barriers.add(w3)
barriers.add(w4)
barriers.add(w5)
barriers.add(w6)
barriers.add(w7)
barriers.add(w99)
barriers.add(w9)
barriers.add(w10)
barriers.add(w11)
barriers.add(w12)
barriers.add(w13)
barriers.add(w14)
barriers.add(w15)
barriers.add(w16)
barriers.add(w17)

# створюємо спрайти
player = Player("ufo_1.png", 10, win_height - 80, 40, 40, 0, 10)

monster = Enemy("monster_4.png", win_width - 80, 180, 40, 40, 3)
monster1 = Enemy("monster_4.png", win_width - 80, 100, 40, 40, 2)

monsters.add(monster)
monsters.add(monster1)

final_sprite = GameSprite("Asset 28@4x.png", 610, 10, 80, 80)


# змінна, що відповідає за те, як закінчилася гра
finish = False
# ігровий цикл
run = True
while run:

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_a:
                player.x_speed = -5
            elif e.key == K_d:
                player.x_speed = 5
            elif e.key == K_w:
                player.y_speed = -5
            elif e.key == K_s:
                player.y_speed = 5
            elif e.key == K_SPACE:
                player.fire()
        elif e.type == KEYUP:
            if e.key == K_a:
                player.x_speed = 0
            elif e.key == K_d:
                player.x_speed = 0
            elif e.key == K_w:
                player.y_speed = 0
            elif e.key == K_s:
                player.y_speed = 0

    if not finish:
        window.blit(background, (0, 0))  # зафарбовуємо вікно кольором
        # малюємо об'єкти
        # w1.reset()
        # w2.reset()
        barriers.draw(window)
        bullets.draw(window)
        monsters.draw(window)

        final_sprite.reset()
        player.reset()

        # включаємо рух
        player.update()
        bullets.update()
        monsters.update()

        sprite.groupcollide(bullets, barriers, True, False)
        sprite.groupcollide(monsters, bullets, True, True)

    # Перевірка зіткнення героя з ворогом та стінами
    if sprite.spritecollide(player, monsters, False):
        finish = True
        # обчислюємо ставлення
        img = image.load("gameover.jpg")
        d = img.get_width() // img.get_height()
        window.fill((255, 255, 255))
        window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))

    if sprite.collide_rect(player, final_sprite):
        finish = True
        img = image.load("thumb.jpg")
        window.fill((255, 255, 255))
        window.blit(transform.scale(img, (win_width, win_height)), (0, 0))

    # цикл спрацьовує кожну 0.05 секунд
    time.delay(10)
    display.update()
