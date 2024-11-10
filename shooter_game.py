#Создай собственный Шутер!

from pygame import *
from random import randint

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire = mixer.Sound('fire.ogg')

font.init()
funt2 = font.SysFont('Arial', 36)
font3 = font.SysFont('Arial', 70)

lose = font3.render('лох', True, (1, 2, 3))
win = font3.render('не лох', True, (4, 5, 6))

score = 0
lost = 0
max_score = 10
max_lost = 30

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()




class Enemy(GameSprite):
     def update(self):
         self.rect.y += self.speed
         global lost
         if self.rect.y > win_height:
             self.rect.x = randint(80, win_width - 80)
             self.rect.y = 0
             lost += 1

win_width = 700
win_height = 500
display.set_caption('БОБР КУРВА')
window = display.set_mode((win_width,win_height))
back = transform.scale(image.load('galaxy.jpg'),(win_width, win_height))

ship = Player('images.png', 5, win_height - 100, 70, 90, 10)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('bobr.png', randint(80, win_height - 80), -20, 80, 52, randint(2,20))
    monsters.add(monster)

bullets = sprite.Group()
finish = False
game = True

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire.play()
                ship.fire()



    if not finish:
        window.blit(back,(0,0))

        text = funt2.render('Счет: ' + str(score), True, (209, 84, 134 ))
        text_lose = funt2.render('Пропущено: ' + str(lost), True, (238, 109, 67))
        window.blit(text,(10, 20))
        window.blit(text_lose, (10, 50))
        bullets.update()
        bullets.draw(window)
        monsters.draw(window)
        monsters.update()
        ship.reset()
        ship.update()
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('bobr.png', randint(80, win_height - 80), -20, 80, 52, randint(2,20))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))

        if score >=max_score:
            finish = True
            window.blit(win,(200,200))
        display.update()
    else:     
        finish=False
        score = 0
        lost= 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy('bobr.png', randint(80, win_height - 80), -20, 80, 52, randint(2,20))
            monsters.add(monster)

       
    time.delay(50)