# Example of playing the game

from classes import Player
from functions import play_game

maze_demo = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", "#", " ", " ", " ", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", "#", "#", "#", "#", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
]
start_pos = (1,1)
start_lives = 3
position = (1,1)
finish = (3,5)
obstacles = [(2,1)]

# Creating instance of Player class

player1 = Player(maze_demo, start_pos, finish, obstacles, lives=3)

# Playing the game

play_game(player1)