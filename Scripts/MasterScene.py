import pygame
from Game import Game


g = Game()


while g.running:
	g.current_scene.draw_scene()