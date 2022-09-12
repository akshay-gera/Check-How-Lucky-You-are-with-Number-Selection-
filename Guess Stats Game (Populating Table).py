import random
from tkinter import N
import pyodbc
from datetime import datetime

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

insertconn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                    'Server=LAPTOP-R24KKR36;'
                    'Database=AkshayGeraGuessingStats;'
                    'Trusted_Connection=yes;',autocommit=True)

myinsertcursor = insertconn.cursor()

InsertStatement= "insert into AkshayGeraGuessingStats.dbo.GuessStats VALUES(?,?,?,?)"
GamePlayNumber=0
#catching the last max value of Game session number from existing database and incrementing it by 1
#  for the first observation, giving the Game Session Value as 0 through if statement
if myinsertcursor.execute("select MAX(GameSessionNumber) from GuessStats").fetchone()[0] == None:
    GameSessionNumber=0
else:
    GameSessionNumber = int(myinsertcursor.execute("select MAX(GameSessionNumber) from GuessStats").fetchone()[0])
GameSessionNumber=GameSessionNumber+1

Points_Earned=[]
Match_list=[]

while True:
    try:
        user_guess=input('Enter a guess number between 1 to 20 or Press Q to quit\t')
        if user_guess in ['Q','q']:
            print('Goodbye')
            
            print('________________________________\n'
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
            break
            
        elif int(user_guess) in list(range(1,21)):
            GamePlayNumber=GamePlayNumber+1
            seek_number = random.randint(1,20)
            user_guess=int(user_guess)
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

            try:
                count = myinsertcursor.execute("""
                                                INSERT INTO AkshayGeraGuessingStats.dbo.GuessStats (GameSessionNumber, GamePlayNumber, Guess, SeekNumber, Match, PointsScored) 
                                                VALUES (?,?,?,?,?,?)""", GameSessionNumber, GamePlayNumber, user_guess, seek_number, match, Points).rowcount 
                
                print('Rows inserted: ' + str(count))
            except Exception as e:
                print('Error inserting record: ', str(e))
            continue

        else:
            print('Enter number between 1 to 20 (both inclusive)')

    except Exception as e:
        print('**', user_guess ,'is not a valid entry, enter a guess between 1 and 20 or Q to quit: __** ', str(e))




