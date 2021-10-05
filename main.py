import pygame
import random
import os

# game init
FPS=60
WHITE=(255,255,255)
BLACK=(0,0,0)
GREEN=(0,255,0)
RED=(255,0,0)
YELLOW=(255,255,0)
WIDTH=900
HEIGHT=1000

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("SPACE WAR 1")
screen=pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

background_img=pygame.image.load(os.path.join("Background.png")).convert()
player_img=pygame.image.load(os.path.join("Player.png")).convert()
rock_img=pygame.image.load(os.path.join("Rock.png")).convert()
bullet_img=pygame.image.load(os.path.join("Bullet.png")).convert()
play_mini_img=pygame.transform.scale(player_img,(25,19))
pygame.display.set_icon(play_mini_img)

shoot_sound=pygame.mixer.Sound(os.path.join("shoot.wav"))
boom_sound=pygame.mixer.Sound(os.path.join("boom.wav"))
pygame.mixer.music.load(os.path.join("background.ogg"))
pygame.mixer.music.set_volume(0.3)

font_name=pygame.font.match_font('arial')
def draw_text(surf,text,size,x,y):
    font=pygame.font.Font(font_name,size)
    text_surface=font.render(text,True,WHITE)
    text_rect=text_surface.get_rect()
    text_rect.centerx=x
    text_rect.top=y
    surf.blit(text_surface,text_rect)

def draw_health(surf,hp,x,y):
    if hp<0:
        hp=0
    BAR_LENGTH=100
    BAR_HEIGHT=10
    fill=hp/100*BAR_LENGTH
    outline_rect=pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect=pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,RED,fill_rect)
    pygame.draw.rect(surf,BLACK,outline_rect,2)

def draw_init():
    screen.blit(pygame.transform.scale(background_img, (900, 1000)), (0, 0))
    draw_text(screen,"SPACE WAR 1",64,WIDTH/2,HEIGHT/4)
    draw_text(screen,"awsd-move plane        plane space-shoot",22,WIDTH/2,HEIGHT/2)
    draw_text(screen,"press any botton start game",18,WIDTH/2,HEIGHT*3/4)
    pygame.display.update()
    waiting=True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting=False
                return False


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(player_img,(50,40))
        self.image.set_colorkey(WHITE)
        self.rect=self.image.get_rect()
        self.radius=20
        self.rect.centerx=WIDTH/2
        self.rect.bottom=HEIGHT-20
        self.speedx =7
        self.health=100

    def update(self):
        key_pressed=pygame.key.get_pressed()
        if key_pressed[pygame.K_d]:
            self.rect.x+=self.speedx
        if key_pressed[pygame.K_a]:
            self.rect.x-=self.speedx
        if key_pressed[pygame.K_w]:
            self.rect.y-=self.speedx
        if key_pressed[pygame.K_s]:
            self.rect.y+=self.speedx
        if self.rect.right >WIDTH:
            self.rect.right=WIDTH
        if self.rect.left < 0:
            self.rect.left=0
        if self.rect.top < 0:
            self.rect.top=0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom=HEIGHT
    def shoot(self):
        bullet= Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori=pygame.transform.scale(rock_img.copy(),(50,40))
        self.image=pygame.transform.scale(rock_img.copy(),(50,40))
        self.image_ori.set_colorkey(WHITE)
        self.rect=self.image.get_rect()
        self.radius=self.rect.width/2
        self.rect.x=random.randrange(0,WIDTH-self.rect.width)
        self.rect.y=random.randrange(-100,-40)
        self.speedy =random.randrange(2,10)
        self.speedx = random.randrange(-3, 3)
        self.total_degree=0
        self.rot_degree=random.randrange(-3,3)

    def rotate(self):
        self.total_degree+=self.rot_degree
        self.total_degree=self.total_degree%360
        self.image=pygame.transform.rotate(self.image_ori,self.total_degree)
        center=self.rect.center
        self.rect=self.image.get_rect()
        self.rect.center=center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top>HEIGHT or self.rect.left>WIDTH or self.rect.right<0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(bullet_img,(10,20))
        self.image.set_colorkey(WHITE)
        self.rect=self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy =-10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom<0:
            self.kill()



pygame.mixer.music.play(-1)
show_init=True

running=True
while running:
    if show_init:
        close=draw_init()
        if close:
            break
        show_init=False
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(12):
            rock = Rock()
            all_sprites.add(rock)
            rocks.add(rock)
        score = 0
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                player.shoot()

    all_sprites.update()
    hits=pygame.sprite.groupcollide(rocks,bullets,True,True)
    for hit in hits:
        boom_sound.play()
        score+=1
        r=Rock()
        all_sprites.add(r)
        rocks.add(r)

    hits=pygame.sprite.spritecollide(player,rocks,True,pygame.sprite.collide_circle)
    for hit in hits:
        r=Rock()
        all_sprites.add(r)
        rocks.add(r)
        player.health-=50
        if player.health<=0:
            show_init=True


    screen.fill(BLACK)
    screen.blit(pygame.transform.scale(background_img,(900,1000)),(0,0))
    all_sprites.draw(screen)
    draw_text(screen,str(score),28,WIDTH/2,10)
    draw_health(screen,player.health,15,30)
    pygame.display.update()

pygame.quit()