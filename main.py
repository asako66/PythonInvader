from tokenize import group
import pygame
from pygame.locals import *
import sys

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


def main():
  # 初期設定
  pygame.init()
  screen = pygame.display.set_mode(SCREEN.size)
  pygame.display.set_caption("Invader")
  clock = pygame.time.Clock()

  # 登場する人もの背景の作成

  # Sprite登録
  group = pygame.sprite.RenderUpdates()
  Player.containers = group
  Beam.containers = group

  player = Player()

  while True:
    # 画面（screen）をクリア
    screen.fill((0,0,0))

    # ゲームに登場する人もの背景の位置Update
    group.update()

    # 画面（screen）上に登場する人もの背景を描画
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

    # 描画スピードの調整（FPS）
    clock.tick(60)

if __name__ == "__main__":
  main()
