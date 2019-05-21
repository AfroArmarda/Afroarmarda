def GetHighScores():
    #makes the whole file into a list
    scoreSheet = open("Highscores.txt").read().splitlines()

    highScore1 = 0
    highScore2 = 0
    highScore3 = 0 

    #finds the highscore 
    for i in range (len(scoreSheet)):
        i += 1
        if i %2 != 0:                   #The list goes name then score and repeats this 
            score = int(scoreSheet[i])  #so this finds every other element in the list
                                        #and then finds the highest ones 
            if score > highScore1:
                highScore1 = score
                name1 = scoreSheet[i-1]
                
    #finds the second highest score 
    for i in range (len(scoreSheet)):
        i += 1
        if i %2 != 0:                   #This does the same but makes sure its lower 
            score = int(scoreSheet[i])  #than the highest score 

            if score > highScore2 and score < highScore1:
                highScore2 = score
                name2 = scoreSheet[i-1]

    #finds the third highest score 
    for i in range (len(scoreSheet)):
        i += 1
        if i %2 != 0:
            score = int(scoreSheet[i])

            if score > highScore3 and score < highScore2:
                highScore3 = score
                name3 = scoreSheet[i-1]
                
    #converts them back to strings as they need to be to be displayed on screen
    highScore1 = str(highScore1)
    highScore2 = str(highScore2)
    highScore3 = str(highScore3)
    
    return highScore1, highScore2, highScore3, name1, name2, name3

#This writes names and scores to the list

def WriteHighScores(name, numRound):
    scoreSheet = open("Highscores.txt", "a+")
    space = """
"""
    scoreSheet.write(space)
    scoreSheet.write(name)
    scoreSheet.write(space)
    scoreSheet.write(numRound)
    scoreSheet.close()
    


##    print(highScore1, highScore2, highScore3)
##
##ll = open("testFile.txt").read().splitlines()
##
##highScore1 = 0
##highScore2 = 0
##highScore3 = 0 
##
##for i in range (len(ll)):
##    i += 1
##    if i %2 != 0:
##        score = int(ll[i])
##
##        if score > highScore1:
##            highScore1 = score
##            name1 = ll[i-1]
##
##for i in range (len(ll)):
##    i += 1
##    if i %2 != 0:
##        score = int(ll[i])
##
##        if score > highScore2 and score < highScore1:
##            highScore2 = score
##            name2 = ll[i-1]
##
##for i in range (len(ll)):
##    i += 1
##    if i %2 != 0:
##        score = int(ll[i])
##        
##
##        if score > highScore3 and score < highScore2:
##            highScore3 = score
##            name3 = ll[i-1]
##
##highScore1 = str(highScore1)
##highScore2 = str(highScore2)
##highScore3 = str(highScore3)
##
##print(name1, highScore1,"     ",name2, highScore2,"     ",name3, highScore3,)
##
####print(highScore1, highScore2, highScore3)
