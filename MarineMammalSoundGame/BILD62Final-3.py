import pygame as pg
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import time
import random
import pandas as pd  


mammals = ({'Marine Mammal Name': ['Humpback Whale', 'Beluga Whale', 'Killer Whale',
                                'Common Bottlenose Dolphin', 'Leopard Seal',
                                'Crabeater Seal', 'Harp Seal', 'Striped Dolphin'],
	        'Pitch of Frequency': ['Low', 'High', 'High', 'High', 'High', 
                            'Low', 'Low', 'High'],
            'File Name': ['MarineMammalSoundhumpback-whale.mp3',
                        'MarineMammalSoundbeluga-whale.mp3',
                        'MarineMammalSoundkiller-whale.mp3',
                        'MarineMammalSoundbottlenose-dolphin.mp3',
                        'MarineMammalSoundleopard-seal.mp3',
                        'MarineMammalSoundcrabeater-seal.mp3',
                        'MarineMammalSoundharp-seal.mp3',
                        'MarineMammalSoundstriped-dolphin.mp3']})  

marine_mammal_df = pd.DataFrame(mammals)  # Created marine mammal dataframe from dictionary 


def play_sound(sound):
    '''Plays .mp3 sound files that are downloaded for a marine mammal acoustic database.
    Input: dictionary of .mp3 files from marine_mammal_df
    Return: plays audio'''
    try:
        run_time = 5  
        pg.mixer.init()
        pg.mixer.music.load(marine_mammal_df['File Name'][sound - 1])
        pg.mixer.music.play()
        time.sleep(run_time)
    except:
        print("Please ensure that you have included the correct files matching name and mp3 file type")
    return()


def play_game():
    '''Guessing Game will count the number of times player answers correctly and store this information to make a bar graph.
    Input: player's answer 
    Return: number of time player answers correctly (num_correct)'''
    sound = random.randint(1,8)  # Marine mammal sounds are randomized
    play_sound(sound)

    num_correct = [0,0,0,0,0,0,0,0]
    response = input("What marine mammal is making this noise? ")  

    while response.lower() != 'quit':  # If player types "quit" the game will stop
        correct = marine_mammal_df['Marine Mammal Name'][sound - 1]
        
        if response.lower() == correct.lower():  # Determines if user input is correct or not 
            print("You are correct, it is a " + correct) 
            num_correct[sound - 1] += 1   
        else:
            print("Incorrect, it was a " + correct + ". Let's try again!")  

        sound = random.randint(1,8)  # Marine mammal sounds are randomized
        play_sound(sound)
        response = input("What marine mammal is making this noise? ") 
            
    print("Thanks for playing! Here is how you did!")   # Bar graph of results will be generated when game stops
    return num_correct


def update_plot(num_correct):
    '''Bar graph of players efficacy will update when player answers the guessing game correctly.
    Input: number of time player answers correctly (num_correct)
    Return: bar graph of player's efficacy '''
    fig = plt.figure(figsize = (12,6)) 
    ax = fig.add_subplot(111)

    ax.bar(marine_mammal_df['Marine Mammal Name'], height=num_correct, width=0.4, bottom=None, align='center')  

    plt.xlabel('Marine Mammal Name')
    plt.ylabel('# of Times Guessed Correctly')
    plt.title('Player Efficacy of "Guess Who?" Game')

    ax.tick_params(axis='x', labelrotation = 45)  

    plt.show()


print(marine_mammal_df)
num_correct = play_game()
update_plot(num_correct)