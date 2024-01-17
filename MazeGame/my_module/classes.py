"""Classes used throughout project"""

class Player:

    def __init__(self, maze, start, finish, obstacles, lives=3):
        """
        Initializing instance-specific variables.
        :param maze: maze for the game
        :param start: starting position
        :param finish: end position
        :param obstacles: positions of obstacles
        :param lives: live count
        """
        self.maze = maze
        self.start_pos = start
        self.start_lives = lives
        self.position = start
        self.finish = finish
        self.obstacles = obstacles
        self.lives = lives

    def check_collision(self):
        
        """Check whether the player's current position overlaps with the position of any obstacles 
        and return a boolean value indicating whether a collision has occurred."""
            
        for obstacle in self.obstacles:
            if self.position == obstacle:
                return True
        return False
    
    def update_lives(self):
        
        """Update the player's life counts based on the outcome of various events in the game."""
        
        for obstacle in self.obstacles:
            if self.check_collision() == True:
                self.lives -= 1
                print("You collided with a poison! You lost 1 life and have {} lives left.".format(self.lives))
                if self.lives == 0:
                    print("Game over...")
                    return
                else:
                    self.position = self.start_pos
                    return
    
    def move(self, direction):
        """
        Move the player's avatar in the maze based on the input direction (up, down, left, or right)
        check whether the player's movement is blocked by walls or other obstacles 
        and update the player's position accordingly.
        :param direction: input movement of the player
        """
        x, y = self.position
        # Assume maze is wrapped by '#'
        if direction == "up":
            y -= 1
        elif direction == "down":
            y += 1
        elif direction == "left":
            x -= 1
        elif direction == "right":
            x += 1
            
        if self.maze[y][x] != "#":
            self.position = (x,y)
        else:
            print("You hit a wall, please pick another direction.")
                 
    def check_finish(self):
        
        """Check if player is at end position."""
        
        if self.position == self.finish:
            return True
        else:
            return False
        
    def reset_game(self):
        
        """Resetting the current game to initial setting which allows the player to start a new game."""
        
        self.lives = self.start_lives
        self.position = self.start_pos
        
    def visualize(self):
        
        """Visualizing the maze and the player's avatar."""
        
        for y in range(len(self.maze)):
            for x in range(len(self.maze[0])):
                if (x,y) == self.position:
                    print("[O]", end="")
                else:
                    print("[{}]".format(self.maze[y][x]), end="")
            print()
