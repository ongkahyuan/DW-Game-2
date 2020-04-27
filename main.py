import os
from assets.shops import *
from assets.player import inventory
from libdw import sm

class selector(sm.SM):
    """
    Class that determines the state of the game. Inherits the state machine class for extra marks. 
    
    States
    ====
    - intro
    Display intro to the game
    - main
    The main game loop. Runs all the shops.
    - monitor
    To do real time monitoring of the number of lines
    - end
    Shows the end sreeen and score. 
    - leave
    Exits the loop
    """
    def __init__(self):
        self.start_state = "intro"
        
    def get_next_values(self,state,inp):
        next_state = state
        if state == "intro":
            if inp == "continue":
                next_state = "main"
            elif inp == "exit":
                next_state = "end"
        elif state == "main":
            if inp == "back":
                next_state = "intro"
            elif inp == "monitor":
                next_state = "monitor"
            elif inp == "exit":
                next_state = "end"
            elif inp == "main":
                next_state = state
        elif state == "monitor":
            if inp == "exit":
                next_state = "main"
        elif state == "end":
            if inp == "again":
                next_state = "intro"
            elif inp == "back":
                next_state = "main"
            elif inp == "exit":
                next_state = "leave"
        elif state == "leave":
            next_state = state
        return next_state, None

class main():
    """
    Class that contains all gamestates. 
    
    Methods
    ====
    -.load_image(state)
    Loads ASCII images associated with a given gamestate into memory. Saves them in attribute self.image
    -.print_ASCII()
    Prints loaded images to terminal
    -.display_inventory()
    Prints inventory items to terminal
    -.intro/end_screen()
    Displays intro and end screen
    -.main_screen()
    Main game screen. Provides access to shops. 
    If player enters a shop, it pauses production of lines, sends inventory state to the shop, and calls the shop function. 
    Upon exit, it takes the updated inventory (post shop modification) and resumes line production.
    -.monitor_screen()
    Shows monitor screen by enabling inventory thread printing to terminal.
    
    Attributes
    ====
    -.invalid
    Bool. Set to True when an invalid input is given, and set to False after error message is displayed 
    """
    def __init__(self):
        self.invalid = False
        self.image_paths = {"main":"assets/logo.txt", "intro":"assets/welcome.txt","end":"assets/end.txt", "end_speech": "assets/end_speech.txt"}
        
    def load_image(self, state):
        self.image = []
        try:
            f = open(self.image_paths[state],'r')
            for line in f:
                self.image.append(line)
            f.close()
        except:
            f = open("assets/default.txt",'r')
            for line in f:
                self.image.append(line)
            f.close()
    
    def print_ASCII(self):
        for line in self.image: 
            print(line, end="")
        
    def display_inventory(self):
        print("\nYour Inventory is as follows\n................................")
        print("  Libraries:")
        if len(inventory_obj.libraries) >0:
            for library, number in inventory_obj.libraries.items():
                print("  - {}: {}\n".format(library, number))
        else:
            print("  - None\n")
        print("  Projects:")
        if len(inventory_obj.projects) >0:
            for project, number in inventory_obj.projects.items():
                print("  - {}: {}".format(project, number))
        else:
            print("  - None\n")
        print("\nLine Rate: {} lines/sec".format(round(inventory_obj.multiplier*5,1)))
        print("Lines: {} (on last refresh) \n................................\n".format(round(inventory_obj.lines)))
    
    def intro_screen(self):
        clear()
        self.load_image("intro")
        self.print_ASCII()
        print("Enter <continue> to start <exit> to quit:\n\n>>", end = '')
        answer = input().lower()
        if answer == "continue" or answer == "exit":
            return answer
    
    def main_screen(self):
        """
        Main screen function. Returns the an input to selector class to update the state machine.
        """
        clear()
        if self.invalid:
            print("Invalid Action!")
            self.invalid = False
        self.load_image("main")
        self.print_ASCII()
        self.display_inventory()
        print('- Enter <a> to write code, <library> or <project> to enter the shop.\n- <Monitor> lets you check progress in real-time; <exit> to exit.\n\n>>',end='')
        answer = input().lower()
        if answer == 'a':
            inventory_obj.add_line()
            return "main"
        elif answer == 'library':
            #pause the production of lines
            inventory_obj.pause()
            #send current inventory state to the library object
            lib_obj.update_with_inventory(inventory_obj.lines,inventory_obj.libraries,inventory_obj.projects,round(inventory_obj.multiplier*10))
            #display library object screen
            lib_obj.display()
            #Receive updated inventory state after purchases
            inventory_obj.lines, inventory_obj.libraries, nothing= lib_obj.update_inventory()
            #resume production of lines
            inventory_obj.resume()
            return "main"
        elif answer == 'project':
            #same as above, but for project object
            inventory_obj.pause()
            pro_obj.update_with_inventory(inventory_obj.lines,inventory_obj.libraries,inventory_obj.projects,round(inventory_obj.multiplier*10))
            pro_obj.display()
            inventory_obj.lines, nothing, inventory_obj.projects= pro_obj.update_inventory()
            inventory_obj.resume()
            return "main"
        elif answer == "exit" or answer == "back" or answer == "monitor":
            return answer
        else:
            self.invalid = True
            return "main"
        
    
    def monitor_screen(self):
        clear()
        inventory_obj.monitor()
        answer = input().lower()
        if answer == "":
            inventory_obj.stop_monitor()
            return "exit"
    
    def end_screen(self):
        clear()
        self.load_image("end")
        self.print_ASCII()
        print("- Number of lines that you 'coded': {}\n".format(round(inventory_obj.lines)))
        print("- Number of lines of my irl code wasted because of DW1D and ban of external libraries : 927\n")
        self.load_image("end_speech")
        self.print_ASCII()
        print("\n\nEnter <again> to start over, <back> to return to game or <exit> to quit\n\n>>",end = '')
        answer = input().lower()
        if answer == "again" or answer == "back" or answer == "exit":
            return answer
        
#Initializing objects
shop_obj = shop()
lib_obj = library_shop()
inventory_obj = inventory()
pro_obj = project_shop()
state_selector = selector()
main_obj = main()

#starting threads
inventory_obj.start()
state_selector.start()



while True:
    #calling methods based on state
    if state_selector.state == "intro":
        state_selector.step(main_obj.intro_screen())
    elif state_selector.state == "main":
        state_selector.step(main_obj.main_screen())
    elif state_selector.state == "monitor":
        state_selector.step(main_obj.monitor_screen())
    elif state_selector.state == "end":
        state_selector.step(main_obj.end_screen())
    elif state_selector.state == "leave":
        break
    else:
        break 

#ending threads
inventory_obj.stop()

