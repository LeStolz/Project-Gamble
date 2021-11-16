import pygame
from Game import Game


game = Game()
# I changed g to game
# Because g is bad
while game.running:
	game.current_scene.draw_scene()