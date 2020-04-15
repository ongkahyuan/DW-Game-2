import os
from shops import *
from player import inventory
from libdw import sm

class selector(sm.SM):
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
                print("in")
                next_state = "leave"
        elif state == "leave":
            next_state = state
        return next_state, None

class main():
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
        print("\nLine Rate: {} lines/sec".format(round(inventory_obj.multiplier*10,1)))
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
        clear()
        self.load_image("main")
        self.print_ASCII()
        if self.invalid:
            print("Invalid!")
            self.invalid = False
        self.display_inventory()
        print('- Enter <a> to write code, <library> or <project> to enter the shop.\n- <Monitor> lets you check progress in real-time; <exit> to exit.\n\n>>',end='')
        answer = input().lower()
        if answer == 'a':
        # if answer == '':
            inventory_obj.add_line()
            return "main"
        elif answer == 'library':
            inventory_obj.pause()
            lib_obj.update_with_inventory(inventory_obj.lines,inventory_obj.libraries,inventory_obj.projects,round(inventory_obj.multiplier*10))
            lib_obj.display()
            inventory_obj.lines, inventory_obj.libraries, nothing= lib_obj.update_inventory()
            inventory_obj.resume()
            return "main"
        elif answer == 'project':
            inventory_obj.pause()
            pro_obj.update_with_inventory(inventory_obj.lines,inventory_obj.libraries,inventory_obj.projects,round(inventory_obj.multiplier*10))
            pro_obj.display()
            inventory_obj.lines, nothing, inventory_obj.projects= pro_obj.update_inventory()
            inventory_obj.resume()
            return "main"
        elif answer == "exit" or "back" or "monitor":
            return answer
        else:
            self.invalid = True
            return "main"
        
    
    def monitor_screen(self):
        clear()
        inventory_obj.monitor()
        # print("press enter ")
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
        
        
shop_obj = shop()
lib_obj = library_shop()
inventory_obj = inventory()
pro_obj = project_shop()
state_selector = selector()

inventory_obj.start()
state_selector.start()

main_obj = main()


while True:
    # print(state_selector.state)
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

# main_obj.main_screen()    

inventory_obj.stop()

