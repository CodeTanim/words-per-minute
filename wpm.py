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






def wpm_test(screen):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    screen.nodelay(True)
    

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)
 
        screen.clear()
        display_text(screen, target_text, current_text, wpm)
        screen.refresh()

        if  "".join(current_text) == target_text:
           screen.nodelay(False)
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




def main(screen):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLUE)
    
    start_screen(screen)

    while True:
        wpm_test(screen)
        screen.addstr(3, 0, "You have completed the test! Your WPM is displayed right above this text. Press any key to continue... ")
        key = screen.getkey()

        if ord(key) == 27:
            break

wrapper(main)