import pygame

class Piece():
  def __init__(self, x, y, dir, size):
    self.dir = dir
    self.size = size
    self.x = x
    self.y = y
    self.rect = pygame.Rect(x,y, size, size)