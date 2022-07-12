import pygame
from pygame.locals import *
import sys
import random

SCREEN = Rect((0,0,640,480))

class Player(pygame.sprite.Sprite):
  SPEED = 5

  def __init__(self):
    pygame.sprite.Sprite.__init__(self, self.containers)
    self.image = pygame.image.load("picture/player01.png").convert_alpha()
    self.image = pygame.transform.scale(self.image, (56,56))
    self.rect = self.image.get_rect()
    self.rect.bottom = SCREEN.bottom
    self.rect.centerx = SCREEN.centerx

  def update(self):
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_LEFT]:
      self.rect.move_ip(-Player.SPEED, 0)
    elif pressed_keys[K_RIGHT]:
      self.rect.move_ip(Player.SPEED, 0)
    self.rect.clamp_ip(SCREEN)

class Beam(pygame.sprite.Sprite):
  """ビーム"""
  SPEED = 5
  counter = 0

  def __init__(self,player):
    pygame.sprite.Sprite.__init__(self, self.containers)
    self.image = pygame.image.load("picture/beam_pink2.png").convert_alpha()
    self.image = pygame.transform.scale(self.image, (56,56))
    self.image = pygame.transform.rotate(self.image, 90)
    self.rect = self.image.get_rect()
    self.player = player
    self.rect.center = self.player.rect.center

  def update(self):
    self.rect.move_ip(0, -Beam.SPEED)
    if self.rect.top < 0:
      Beam.counter -= 1
      self.kill()

class Background:
  """背景"""
  ASA, YUGATA, YORU = 1,2,3
  background_status = ASA

  def __init__(self):
    self.image1 = pygame.image.load("picture/bg_pattern2_aozora.png")
    self.image1 = pygame.transform.scale(self.image1, (640, 480))
    self.rect1 = self.image1.get_rect()
    self.image2 = pygame.image.load("picture/bg_pattern3_yuyake.png")
    self.image2 = pygame.transform.scale(self.image2, (640, 480))
    self.rect2 = self.image2.get_rect()
    self.image3 = pygame.image.load("picture/bg_pattern4_yoru.png")
    self.image3 = pygame.transform.scale(self.image3, (640, 480))
    self.rect3 = self.image3.get_rect()

  def draw(self,screen):
    if Background.background_status == Background.ASA:
      screen.blit(self.image1, self.rect1)
    if Background.background_status == Background.YUGATA:
      screen.blit(self.image2, self.rect2)
    if Background.background_status == Background.YORU:
      screen.blit(self.image3, self.rect3)

class Ufo(pygame.sprite.Sprite):
  """UFO"""
  SPEED = 2
  move_width = 230
  prob_action = 0.0001

  def __init__(self, pos):
    pygame.sprite.Sprite.__init__(self, self.containers)
    self.image = pygame.image.load("picture/alien_ufo.png").convert_alpha()
    self.image = pygame.transform.scale(self.image, (56,56))
    self.rect = self.image.get_rect()
    self.rect.center = pos
    self.left = pos[0]
    self.right = self.left + Ufo.move_width

  def update(self):
    self.rect.move_ip(Ufo.SPEED, 0)
    if self.rect.center[0] < self.left or self.rect.center[0] > self.right:
      Ufo.SPEED = -Ufo.SPEED
    if random.random() < self.prob_action:
      Action(self)

class Action(pygame.sprite.Sprite):
  """UFOからの攻撃"""
  SPEED = 3
  counter = 0

  def __init__(self,ufo):
    pygame.sprite.Sprite.__init__(self, self.containers)
    self.image = pygame.image.load("picture/beam_blue.png").convert_alpha()
    self.image = pygame.transform.scale(self.image, (56,56))
    self.image = pygame.transform.rotate(self.image, 90)
    self.rect = self.image.get_rect()
    self.ufo = ufo
    self.rect.center = self.ufo.rect.center

  def update(self):
    self.rect.move_ip(0, Action.SPEED)
    if self.rect.bottom > SCREEN.height:
      self.kill()


def collision_det(beam_g, ufo_g):
  ufo_collided = pygame.sprite.groupcollide(ufo_g, beam_g, True ,True)
  if ufo_collided:
    Beam.counter -= 1
  for ufo in ufo_collided.keys():
    """サウンドの再生"""
    Ufo.kill_sound.play()


def main():
  # 初期設定
  pygame.init()
  screen = pygame.display.set_mode(SCREEN.size)
  pygame.display.set_caption("Invader")
  clock = pygame.time.Clock()

  # 登場する人もの背景の作成


  Ufo.kill_sound = pygame.mixer.Sound("music/System36.ogg")

  # Sprite登録
  group = pygame.sprite.RenderUpdates()
  beam_g = pygame.sprite.Group()
  ufo_g = pygame.sprite.Group()
  Player.containers = group
  Beam.containers = group, beam_g
  Ufo.containers = group,ufo_g
  Action.containers = group

  background = Background()
  player = Player()

  for i in range(0, 10):
    x = 20 + (i % 10) * 40
    for j in range(0,5):
      y = 20 + j * 40
      Ufo((x,y))

  while True:
    # 画面（screen）をクリア
    screen.fill((0,0,0))

    # ゲームに登場する人もの背景の位置Update
    group.update()

    # 画面（screen）上に登場する人もの背景を描画
    background.draw(screen)
    group.draw(screen)

    # 画面（screen）の実表示
    pygame.display.update()

    # イベント処理
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          pygame.quit()
          sys.exit()
        if event.key == K_SPACE:
          """ビームの発射"""
          if Beam.counter < 3:
            Beam.counter += 1
            Beam(player)

    """衝突判定"""
    collision_det(beam_g, ufo_g)

    # 描画スピードの調整（FPS）
    clock.tick(60)

if __name__ == "__main__":
  main()
