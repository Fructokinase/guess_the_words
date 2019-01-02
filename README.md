# guess_the_words


A command line game that is inspired by one of Delta Airline's in-flight games.
The original game was a UI based game. The goal was, given 6 letters, guess
the 20 or so 3 ~ 6 lettered words that can be formed using the 6 letters,
within timelimit. 


# Implementation 

The game object handles a simple game logic; given a user input, check if the user input is a 
validword and if so, update the game state.

The word generator generates the solution set in a not so clever way. The default mac OS english dictionary 
was used to generate 20 or so 6-lettered words called seeds. Using the 6 letters of each seed,
each seed then generates possible 3~5 lettered words by iterating through the whole dictionary of words.
The seed that has the most solutions is chose to be used in the game.

There are two threads in the driver; One of the game and one for the timer.


# Interesting notices

In general, how good word games are tightly relate to how well they 
can generate a set of words that are common enough for the average user to know. 
I couldn't find a good way to generate those words other than to manually curate the 
solution set, which is both time costly and limiting in the solution universe



