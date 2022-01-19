import curses
from curses import wrapper
import time
import random

# Add comments, to make sure you know each and every part of this program!!!

def start_screen(screen):
    screen.clear() # Clears all of the current content on the terminal screen
    screen.addstr( 10, 35, "Hello! Welcome to the typing speed game!", curses.color_pair(3)) # Introduces the program
    screen.addstr( 11, 42, "Press any key to begin!", curses.color_pair(3))  #  Telling the user that any key and be pressed to continue the program
    screen.getkey() # get any key input to update the screen and begin the game. 
    screen.refresh() # Refresh the screen to update it to the next phase







def display_text(screen, target, current, wpm = 0):
    # A function primarily for displaying text on the terminal screen
    screen.addstr(target)
    screen.addstr(2, 0, f"WPM: {wpm}")
     
     # A for loop that iterates and overlays the current text with the color you want. It will be
     # a green overlay for the correct key presses and red for incorrect presses. 
    for i, char in enumerate(current):
        # The target text will have been loaded by load_text function, which will be initialized in the wpm_test function and passed as the parameter for "target" in this function.
        # correct_char is then set to be the characters of the target, and the color is overlayed to be green when the current (text taken as input is matches the correct characters aka target)
        correct_char = target[i]
        color = curses.color_pair(1)
        
         
        if char != correct_char:
            # In the event that the inputted characters in current string array does not match the correct chars, then color of the text will be overlayed with red.
            color = curses.color_pair(2)

        # starting from the beginning of the target string, begin to overwrite the target string with the color that matches. red for wrong, green for right. 
        # thats the effect this line will have. it is simply writing the inputted characters out to the terminal screen and making it green if it matches the target/correct char.
        screen.addstr(0, i, char, color)






def load_text():
    # Load and return a random sentence from the text file. 
    with open("test.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()




def free_space():
    # After updating the score and sorting it from highest to lowest. Delete any score below 
    # the top 5 spot to free up some space. 

    with open('high_score.txt', 'r') as file:
        # read a list of lines into content. Essentially making an array of sort.
        lines = file.readlines()

    file.close()

    i = 0
    if len(lines) > 5:

        del_amount = len(lines)-5
        while i < del_amount:
            del lines[5]
            i +=1


    new_lines = open('high_score.txt', 'w')

    for line in lines:
        new_lines.write(line)

    new_lines.close()
 

    

def update_score(wpm):
    # Try a more in place approach by iterating through lines and using the replace function by having an already sorted list. 


    score = wpm
    file = open("high_score.txt", "a")
    file.write(str(score)+"\n")
    file.close()



    # Now to sort the text file and write to the high_score text file. 
    new_file = open("high_score.txt", "r")
    #Below a list is made from the scores text file.
    lines = new_file.readlines()

    new_file.close()

    lines.sort(reverse = True)

    with open("high_score.txt", "w") as ofile:
        for line in lines:
            ofile.write(line)

    ofile.close()
   




def wpm_test(screen):
    target_text = load_text() # The target sentence string that you want to use for your typing test. A random text will be loaded. 
    current_text = []
    start_time = time.time()
    screen.nodelay(True)
    wpm = 0
    

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)
 
        screen.clear()
        display_text(screen, target_text, current_text, wpm)
        screen.refresh()

        if  "".join(current_text) == target_text:
           screen.nodelay(False)
           update_score(wpm)
           free_space()
           break

        try:
            key = screen.getkey()
        except:
            continue


        if ord(key) == 27:
            # if escape is pressed then exit the loop and the program. 
            break

        if key in ("KEY_BACKSPACE", '\b', '\x7f'):
            if len(current_text) > 0: 
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)





def display_score(screen):
    file = open("high_score.txt", "r")
    lines = file.readlines()

    screen.addstr(8,0, "The top 5 scores are displayed below:")
    j = 10
    i = 0
    k = 1
    while i < len(lines):
        screen.addstr(j, 0, str(k))
        screen.addstr(j, 1, ") ")
        screen.addstr(j, 2," ")
        screen.addstr(j, 3, lines[i])
        j += 1
        i += 1
        k += 1




def main(screen):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLUE)
    
    start_screen(screen)

    while True:
        wpm_test(screen)
        screen.addstr(3, 0, "You have completed the test! Your WPM is displayed right above this text. Press any key to continue... ")
        screen.addstr(4,0, "Press esc to exit.")

        # Displays the top 5 high scores. 
        display_score(screen)

        #gets key to potentially end/exit out of the program
        key = screen.getkey()





        
        if ord(key) == 27:
            break

    
           
            


wrapper(main)