# importing the modules necessary to run the game

import pandas as pd
import random

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import os

# Error-handling Function to ensure usernames contain only alphanumeric characters

def validate_username(username):
    """
    Function to check if the username is valid, or only contains alphanumeric characters.
    If the username is not valid, it returns False, and asks the user to choose a username
    that only uses letters and numbers.

    Parameters:
    1. username (str): The username entered by the user.

    Returns:
    1. False (bool)
    2. True (bool)

    """

    if not username.isalnum():
        print("Invalid username format. Please use only letters and numbers.")
        return False
    return True

# Error-handling Function to load images from files

def load_image(filename):
    """
    Function to check if the image file exists. If the file does not exist, it and prints "Image file not found:" followed by the file name. This function allows the game
    to continue being played even if an image is missing using a try/except block.

    Parameters:
    1. filename

    Returns:
    1. img (file): The image file associated with the organ.
    """

    try:
        img = mpimg.imread(filename)
        return img
    except FileNotFoundError:
        print("Image file not found:", filename)
        return None
    
# Function checks if file called scoresheet exists and if not, creates one

def set_up_scoresheet():
    """
    Function to check if a file called 'scoresheet.csv' exists. If the file does not exist, it creates one
    with initial data for a scoresheet. The initial data includes a dictionary with usernames, high scores,
    and times played. The function creates a Pandas DataFrame from the dictionary and sets the 'usernames' column
    as the index for the DataFrame.

    Parameters:
    None

    Returns:
    None
    """
    if not(os.path.exists('scoresheet.csv')):

        # Initialize a dictionary with default values for the score sheet
        score_dict = {'usernames':['Test1'], 'high_score':0, 'times_played':0}

        # Create a DataFrame using the dictionary and set the index to 'usernames'
        score_data = pd.DataFrame(score_dict).set_index('usernames')

         # Save the DataFrame to a CSV file named 'scoresheet.csv'
        score_data.to_csv('scoresheet.csv')

def start_game():
    """
    Function to start the game. It first sets up the scoresheet by calling the set_up_scoresheet() function.
    Then, it prompts the user to enter their username and loads the scoresheet from 'scoresheet.csv' into a
    Pandas DataFrame. If the user's username is already in the scoresheet, it welcomes them back and retrieves
    their high score. If the username is not found, it creates a new entry for the user in the scoresheet with
    an initial high score of 0 and times played set to 0.

    Parameters:
    None

    Returns:
    1. username (str): The username entered by the user.
    2. high_score (int): The high score of the user, either retrieved from the scoresheet or set to 0 for new users.
    3. score_data (DataFrame): The Pandas DataFrame containing the scoresheet data.
    """

    # Calls the scoresheet function to create a dataframe with columns of existing usernames and their respective scores
    set_up_scoresheet()

    print("Welcome to the Guess Who (Biology Version)!")
    username = input("Please enter your username: ")

    # Checks if inputted username is valid or not and prompts user to input new username if not valid
    while not validate_username(username):
        username = input("Please enter a valid username: ")

    # Loads the scoresheet
    score_data = pd.read_csv('scoresheet.csv').set_index('usernames')

    # Checks if username exists in scoresheet, and presents the user's high score if it does
    if username in score_data.index:
        print(f"Welcome back, {username}!")
        high_score = score_data.loc[username, 'high_score']

    # If the username does not exist in the scoresheet, a new entry is created in the dataframe for the user, with their high score initialized at 0
    else:
        print(f"Welcome, {username}!")
        high_score = 0
        print("A new entry has been created for you.")
        score_data.loc[username] = [0, 0]

    return username, high_score, score_data

def organ_guessing_game_round(score, rd, organs_dict):
    """
    Function to play a round of the organ guessing game. It randomly selects an organ from the provided
    organs_dict and gives hints to the player to guess the organ. The player has three chances to guess
    the correct organ. If the player guesses correctly, their score increases by 1. If the player quits
    the game, the function returns early with a score of 0, round 7, and an empty dictionary. After each
    round, the selected organ is removed from the organs_dict.

    Parameters:
    1. score (int): The current score of the player.
    2. rd (int): The current round number.
    3. organs_dict (dict): A dictionary containing organs as keys and their corresponding hints as values.

    Returns:
    1. score (int): The updated score after the round.
    2. rd (int): The updated round number.
    3. organs_dict (dict): The updated organs dictionary with the selected organ removed.
    """

    # The try block tests the block of code for errors
    try:
        # Sets current organ equal to a random element from a list version of the organ dictionary. Sets incorrect guess equal to 0, and adds 1 to round.
        current_organ = random.choice(list(organs_dict.items()))
        incorrect_guesses = 0
        rd = rd + 1

        print("Round", rd, "!")
        if rd == 7:
            print("Final round!")
        print("Can you guess which organ I'm thinking of?")
        print("Here's your first hint: " + current_organ[1]['hint1'])

        # Loops until the user guesses right, or until they guess wrong 3 times
        while incorrect_guesses < 3:
            guess = input("Your guess: ").lower()
            # Used to handle if the user enters a plural and if no answer is entered 
            guess_corrected = guess.rstrip(guess[-1]) if len(guess) > 0 else ' ' 

            # Ends the game prematurely if the user types 'quit'
            if guess == 'quit':
                print("You've quit the game!")
                return 0, 7, {}

            # If the guess is right, or a plural of the right guess,
            # will update the user's score and exit the loop
            elif current_organ[0] == guess or current_organ[0] == guess_corrected:
                print("You guessed correctly! Congrats!")
                img = load_image(current_organ[1]['image'])
                if img is None:
                    print("Error loading image.")
                else:
                    imgplot = plt.imshow(img)
                    plt.show()
                score = score + 1
                break

            # If the user guessed wrong, shows new hints and asks for input again
            else:
                incorrect_guesses += 1
                print("Incorrect guess! Try again.")
                if incorrect_guesses == 1:
                    print("Here's another hint: " + current_organ[1]['hint2'])
                elif incorrect_guesses == 2:
                    print("Here's your last hint: " + current_organ[1]['hint3'])

        # If the user guessed wrong 3 times
        if incorrect_guesses == 3:
            print("The answer is: ", current_organ[0])
            img = load_image(current_organ[1]['image'])
            if img is None:
                print("Error loading image.")
            else:
                imgplot = plt.imshow(img)
                plt.show()
            print("Try again next time!")

        # Removes the current organ from the dictionary, so it can't be called again
        del organs_dict[current_organ[0]]

        return score, rd, organs_dict

    # The except block handle errors, in this case Exception (includes all exceptions)
    except Exception as e:
        print("An error occurred during the game:", e)
        
        return 0, 7, {}

def play_organ_guessing_game():

    """
    Function to play the organ guessing game. Loads the organs dictionary containing organ names
    and corresponding hints. The player starts with a score of 0 and plays rounds of guessing organs
    until all organs have been guessed. Displays welcome message and iteratively calls the
    organ_guessing_game_round function for each round.

    Parameters:
    None

    Returns:
    1. score (int): The final score of the player after playing the game.
    """

    # Dictionary containing organ names, hints, and images
    organs_dict = {
        "heart":{
            "hint1":"Pumps blood",
            "hint2":"Inside the ribcage",
            "hint3":"Has 4 chambers",
            "image":"Images/Heart.jpg"},
        "lung":{
            "hint1":"Absorbs oxygen",
            "hint2":"Inside the ribcage",
            "hint3":"Removes carbon dioxide",
            "image":"Images/Lungs.png"},
        "stomach":{
            "hint1":"A muscular hollow organ",
            "hint2":"Has a mucus lining to protect itself from enzymes and acid",
            "hint3":"Digests food",
            "image":"Images/Stomach.png"},
        "kidney":{
            "hint1":"Remove waste products from the blood and produce urine",
            "hint2":"Filter system for your body",
            "hint3":" Two reddish-brown bean-shaped organs",
            "image":"Images/Kidney.jpg"},
        "brain":{
            "hint1":"Has numerous folds to maximize surface area",
            "hint2":"Contains 4 major lobes",
            "hint3":"Main part of the nervous system",
            "image":"Images/Brain.jpg"},
        "liver":{
            "hint1":"Storage location for fat-soluble vitamins and handles cholesterol homeostasis",
            "hint2":"Produces an important digestive liquid called bile",
            "hint3":"Clearing the blood of drugs and other poisonous substances",
            "image":"Images/Liver.png"},
        "large intestine":{
            "hint1":"Absorb water and salts from the material that has not been digested",
            "hint2":"Formation and storage of feces",
            "hint3":"Producing and absorbing vitamins",
            "image":"Images/LargeIntestine.jpg"}}


    # Initialize score and round count
    score = 0 
    rd = 0 

    print("Welcome to the Organ Guessing Game!")

    # Continue playing rounds until all organs are guessed
    while len(organs_dict) > 0:
        score, rd, organs_dict = organ_guessing_game_round(score,rd,organs_dict)

    return score

def check_user_scores(username, score, high_score, score_data):
    """
    Function to check and display the user's final score and provide feedback based on their performance.
    It also checks if the current score is higher than their previous high score and updates it accordingly.

    Parameters:
    1. username (str): The username of the player.
    2. score (int): The final score of the player after playing the game.
    3. high_score (int): The previous highest score of the player.
    4. score_data (DataFrame): The Pandas DataFrame containing the scoresheet data.

    Returns:
    1. high_score (int): The updated high score after comparing it with the current score.
    """

    # Shows the user their score
    print(username, "'s final score is ", score, sep = "")

    # Feedback on the user's score
    if score == 7:                                                 # If it’s the max score
        print('Congrats! You got a perfect score!')
    elif score < 7 and score > 4:                                  # If the score is decent
        print('You did well! But you have room for improvement.')
    else:                                                          # If the score is not great
        print('Study and see if you can do better next time!')

    # Runs if this is the user's first time playing
    if score_data.loc[username, 'times_played'] == 0:
        if score == 7:
            print('Great job on your first try!')
        else:
            print('Play again and see if you can beat your own score!')
        high_score = score

    # Runs if the user has played before
    else:
        print(username, "'s previous high score is ", int(high_score), sep = "")

        # If the new score is higher than their previous highest score
        if score > high_score:
            print('New high score!')
            high_score = score

        # If they got a perfect score this time and in the past
        elif score == high_score and score == 7:
            print('And you got another perfect!')

        # If they got a perfect score before but not this time
        elif score != 7 and high_score == 7:
            print("You didn't do as well, but your high score can't go any higher!")

        # If they have never gotten a perfect and didn’t beat their high score
        else:
            print('You didn’t beat your high score this time.')

    return high_score

def check_high_scores(username, score_data):
    """
    Function to check and display the high scores from the score data.
    It compares the current score and high score with the existing scores in the data
    and provides feedback based on the comparison.

    Parameters:
    1. username (str): The username of the player.
    2. score_data (DataFrame): The Pandas DataFrame containing score data.

    Returns:
    None
    """

    high_score_data = score_data.copy()

    # Adds back in the Test1 user if it's missing to use for comparison.
    # This ensures the DataFrame does not become empty, in case the current
    # user is the only one on the sheet
    high_score_data.loc['Test1'] = [0, 0]

    # Temporarily saves and then removes the user's current information from the
    # data, so their high score isn't compared to itself
    my_high_score = high_score_data.loc[username, 'high_score']
    my_times_played = high_score_data.loc[username, 'times_played']
    high_score_data.drop([username], axis = 0, inplace = True)

    # Compares the user's high score to the ones now in the data
    if my_high_score > high_score_data['high_score'].max(axis = 0):
        print('You have the all-time high score!')
    elif my_high_score == high_score_data['high_score'].max(axis = 0):
        print('You’re tied for the all-time high score!')
    else:
        print('See if you can beat or tie the all-time high score!')

    # Removes test value
    high_score_data.drop(['Test1'], axis = 0, inplace = True)

    # Adds back in the user's data
    high_score_data.loc[username] = [my_high_score, my_times_played]

    # Sorts by descending high scores and usernames A to Z
    high_score_data.sort_values(by = ['high_score', 'usernames'], ascending = [False, True], inplace = True)

    print(high_score_data.head())
    
def show_scores(username, score, high_score, score_data):
    """
    Function to display the user's scores and update their high score if necessary.

    Parameters:
    1. username (str): The username of the player.
    2. score (int): The final score of the player after playing the game.
    3. high_score (int): The previous highest score of the player.
    4. score_data (DataFrame): The Pandas DataFrame containing score data.

    Returns:
    1. high_score (int): The updated high score after checking the user's scores.
    """
  
    # Check if the current score is higher than the previous high score
    high_score = check_user_scores(username, score, high_score)

    return high_score

def check_replay(replay):
    """
    Function to check if the user wants to play again and sets the replay variable accordingly.

    Parameters:
    1. replay (bool): The current value of the replay variable.

    Returns:
    2. replay (bool): The updated value of the replay variable based on user input.
    """

    # Bool to keep track of whether a clear answer is given
    good_answer = False

    # Loop until the user gives a clear yes or no answer
    while good_answer == False:

        answer = input("Do you want to play again? Type 'yes' if you do, or type 'no' if you want to end here. ")
        answer_low = answer.lower()

        # Since replay = true, will keep looping the game
        if 'yes' in answer_low and 'no' not in answer_low:
            good_answer = True
            replay = True
            print("Let's play again!")

        # Since replay = false, will stop looping the game
        elif 'no' in answer_low and 'yes' not in answer_low:
            good_answer = True
            replay = False

        # If there is no clear answer given
        else:
            print("Please type only 'yes' or 'no' when asked if you want to play again.")

    return replay

def update_scoresheet(username, high_score, score_data):
    """
    Function to update the score sheet with the user's high score and number of times played.

    Parameters:
    1. username (str): The username of the player.
    2. high_score (int): The highest score achieved by the player.
    3. score_data (DataFrame): The Pandas DataFrame containing score data.

    Returns:
    1. score_data (DataFrame): The updated score data DataFrame.
    """

    try:
        score_data.loc[username, 'high_score'] = high_score
        score_data.loc[username, 'times_played'] += 1
    except Exception as e:
        print("Error updating scoresheet:", e)
    return score_data