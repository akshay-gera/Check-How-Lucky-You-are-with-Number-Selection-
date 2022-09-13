# So you think you're lucky with numbers?
## Check your luck today, before buying your next Lotto Max ticket! :D

You make a guess between numbers 1-20, and the system will match how close you are to computer's randomized choice of number (Seek Number). If you see a lot of matches on a particular day, maybe its your lucky day. Better to hit the lottery store next. :D
For your each selection, the data  generated flows in your SQL Database to record each game you've played. This is a cool feature for you have history of your scores.
At end of every game session you can see a summary statistics of your game session. 
The system is designed to give you a score on how close your guess is from the randomized number. The scoring rubric is as follows:

-Correct guess = 5 points
-within 1 of the correct number without going over = 3 points
-within 2 of the correct number without going over = 2 points
-within 3 of the correct number without going over = 1 point
-higher than the correct number = -1 point
-all other possibilities = 0 points

Game Rules:
1) Input numbers between 1-20(inclusive)
2) Enter Q or q to quit game
3) Any other input numerical/character is not accepted

## Sample screenshot of a particular session  playing 3 sessions of game 

<img width="416" alt="image" src="https://user-images.githubusercontent.com/98545133/190002729-f0d98f9c-a34b-4552-96b7-d4314996b624.png">


## Sample screenshot of how after 3 sessions my SQL table looks like

<img width="631" alt="image" src="https://user-images.githubusercontent.com/98545133/189778825-1be606d9-ee76-486f-bdc8-f2e98b9d385f.png">
