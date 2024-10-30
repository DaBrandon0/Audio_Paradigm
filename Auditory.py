import winsound
import time
import random

error_rate = 20
trials = 3
score = 0
i = 0
while ( input("Press the enter key to continue:") != ""):
    monkey = 1
while (1 == 1):
    tf = random.randint(1,100)
    sound = random.randint(100,1500)
    error_sound = random.randint(100,1500)
    time.sleep(2)
    winsound.Beep(sound, 1000)
    time.sleep(2)
    if(error_rate > tf):
        winsound.Beep(sound, 1000)
    else:
        while (sound == error_sound):
            error_sound = random.randint(100,1500)
        winsound.Beep(error_sound, 1000)
    ans = input("Did the sounds match?(y/n):")
    if(error_rate > tf):
        if (ans == "yes"):
            score = score + 1
        else:
            score = score
    else:
        if (ans == "n"):
            score = score + 1
        else:
            score = score
    i = i + 1
    if (i == trials):
        print("Score:",score)
        if(input("Replay(y/n)?") == "y"):
            i = 0
        else:
            quit

    

    

