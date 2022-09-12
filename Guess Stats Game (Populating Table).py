# importing libraries

import random
from tkinter import N
import pyodbc
from datetime import datetime

# Creating a function for calculating points as per the scoring logic (mentioned in readme file)
def CalculatePoints(user_guess,seek_number):
    if user_guess==seek_number:
        Points=5
    elif user_guess-seek_number in [1,-1]:
        Points=3
    elif user_guess-seek_number in [2,-2]:
        Points=2
    elif user_guess-seek_number in [3,-3]:
        Points=1
    elif user_guess > seek_number:
        Points=-1
    else:
        Points=0
    return Points

# Creating a connection with SQL server and with my locally created database through PyODBC library 
insertconn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                    'Server=LAPTOP-R24KKR36;'
                    'Database=AkshayGeraGuessingStats;'
                    'Trusted_Connection=yes;',autocommit=True)

myinsertcursor = insertconn.cursor()

# Creating variables with SQL commands for ease of use in the code below
InsertStatement= "insert into AkshayGeraGuessingStats.dbo.GuessStats VALUES(?,?,?,?)"

#Initializing Game Play Number with 0
GamePlayNumber=0

# We like to have an updated Game Session number. 
# Catching the last max value of Game session number from existing database and incrementing it by 1
# For the first observation, giving the Game Session Value as 0 through if statement
if myinsertcursor.execute("select MAX(GameSessionNumber) from GuessStats").fetchone()[0] == None:
    GameSessionNumber=0
else:
    GameSessionNumber = int(myinsertcursor.execute("select MAX(GameSessionNumber) from GuessStats").fetchone()[0])
GameSessionNumber=GameSessionNumber+1

# Creating a list of points earned and match list variables which will be populate below
Points_Earned=[]
Match_list=[]

# Creating a while loop which will keep interacting with the user and respond 
# The while loop keeps on accepting values and returns the set responses
while True:
    # Putting all the accepted values under the try branch to avoid exceptions when user inputs erroneous values (will go to except argument then)
    try:
        # The main welcome statement for the user whic asks for user input
        user_guess=input('Enter a guess number between 1 to 20 or Press Q to quit\t')

        # If user plans to quit the game, only specific input can get user out of the game
        if user_guess in ['Q','q']:
            print('Goodbye')
            
            print('________________________________\n'

            # Summary statistics for the session will be displayed
            'Thanks for playing.\n','\n',
            'Your stats this session:\n'
            '#Correct guesses:\t',sum(Match_list),'\n',
            '#Guesses attempted:\t',GamePlayNumber,'\n',
            'Points Scored:\t',sum(Points_Earned),'\n','\n',
            'Player Average(per session)\n'
            'Avg# Correct guesses per session:\t', int(myinsertcursor.execute("select SUM(Match) from GuessStats").fetchone()[0])/GameSessionNumber,'\n'
            'Avg# Guesses attempted per session:\t', int(myinsertcursor.execute("select COUNT(*) from GuessStats").fetchone()[0])/GameSessionNumber,'\n',
            'Avg Points Scored per Session:\t', int(myinsertcursor.execute("select SUM(PointsScored) from GuessStats").fetchone()[0])/GameSessionNumber , '\n'
            '________________________________\n')
            
            # While loop breaks right away when Q/q is inputted
            break
        
        # User selects a numerical value between 1 to 20 (inclusive)
        elif int(user_guess) in list(range(1,21)):
            GamePlayNumber=GamePlayNumber+1
            seek_number = random.randint(1,20)
            user_guess=int(user_guess)
            
            # Initializing a value of match with 0 which will keep on populating if matches between user selected number is found
            match=0
            if seek_number==user_guess:
                match=match+1
            else:
                match=match+0
            Points=CalculatePoints(user_guess,seek_number)
            Points_Earned.append(Points)
            Match_list.append(match)
            
            print('Game Session Number:\t', GameSessionNumber,'\n' 
                    'Guess Number:\t', GamePlayNumber, '\n',
                    '\n'
                    'This Guess\n',
                    'Your Guess:\t',user_guess,'\n'
                    'Correct Number:\t',seek_number,'\n',
                    'Points Earned:\t', Points,'\n' '\n'
                    '________________________________\n'
                    'Session Summary\n'
                    'Correct Guesses:\t',sum(Match_list),'\n',
                    'Total Points this session:\t',sum(Points_Earned),'\n'
                    '_________________________________')
            # Try condition added to capture if there is any exception occuring while inserting the data into SQL database
            try:
                # Inserting the user input values and stats generated into SQL database
                count = myinsertcursor.execute("""
                                                INSERT INTO AkshayGeraGuessingStats.dbo.GuessStats (GameSessionNumber, GamePlayNumber, Guess, SeekNumber, Match, PointsScored) 
                                                VALUES (?,?,?,?,?,?)""", GameSessionNumber, GamePlayNumber, user_guess, seek_number, match, Points).rowcount 
                # confirmation generated for successful push into SQL database
                print('Rows inserted: ' + str(count))
            
            # Returns exception value as a string for better comprehension of errors occuring during SQL push
            except Exception as e:
                print('Error inserting record: ', str(e))
            
            # continue keeps the while loop running till the bottom
            continue
        
        # If the user input is numerical but outside accepted range of 1-20
        else:
            print('Enter number between 1 to 20 (both inclusive)')

    # When user inputs any other value other than numerical or Quit command, it will remind user to input only accepted values
    # It will also return the actual python error as a string
    except Exception as e:
        print('**', user_guess ,'is not a valid entry, enter a guess between 1 and 20 or Q to quit: __** ', str(e))




