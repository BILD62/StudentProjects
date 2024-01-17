"""A collection of function for doing my project."""

def play_game(player):
    
    """ Function to play the game. 
    :param player: An instance of the Player class that is playing the game."""
    
    print("Welcome to game! You will have {} lives.".format(player.lives))

    while True:

        print("You are at {} right now.".format(player.position))
        player.visualize()

        direction = input("You want to move in which direction? (up/down/left/right): ")

        if direction != "up" and direction != "down" and direction != "left" and direction != "right":
            print("Input not accepted, please pick up/down/left/right.")
            continue

        player.move(direction)
        player.update_lives()

        if player.position == player.finish:
            print("You are at {} right now.".format(player.position))
            player.visualize()
            print("Congrats you made it!!!")
            again = input("Would you like to play again? MUST BE VALID INPUT OR ELSE GAME ENDS (Y/N): ")
            if again != "Y" and again != "N":
                print("Input not accepted. Thank you for playing!!")
                player.reset_game()
                break
            elif again == "Y":
                player.reset_game()
                continue
            else:
                print("Thank you for playing!!")
                break
        elif player.lives == 0:
            again = input("Would you like to play again? MUST BE VALID INPUT OR ELSE GAME ENDS (Y/N): ")
            if again != "Y" and again != "N":
                print("Input not accepted. Thank you for playing!!")
                player.reset_game()
                break
            elif again == "Y":
                player.reset_game()
                continue
            else:
                print("Thank you for playing!!")
                break