import pygame
from pygame.locals import *
from random import randint

screen = pygame.display.set_mode((900, 900))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
fps = 4
pygame.init()