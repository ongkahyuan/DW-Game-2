import threading
import os
import time

def clear(): 
    """"To clear the terminal"""
    if os.name == 'nt': 
        os.system('cls') 
    else: 
        os.system('clear')

class shop():
    """
    Generic shop class. Works as a state machine, with main "loop" being .display() (which is actually called recursively)
    Yes, I realise I could have made a base class for both main and shop objects because of the repeated functions. 
    Yes, I could have unified the state machine methods, with both either using this recursive method or the state machine class.
    No, I didn't think it was worth the effort for a project of this scale. 
    Yes, I only realised too late that I hadn't implemented sm.SM and did it last minute in main.py 
    
    Methods
    ====
    -.load_image(state)
    Loads ASCII images associated with a given gamestate into memory. Saves them in attribute self.image
    -.print_ASCII()
    Prints loaded images to terminal    
    -.init_prompt()
    Displays the initial shop prompt
    -.update_with_inventory(lines, libraries, projects, rate)
    Takes inventory from the main loop and stores it as attributes in the object
    -.update_inventory()
    Returns the update inventory to the main loop
    -.next_purchase()
    Display next purchase prompt
    -.purchase()
    Display purchase prompt
    -.shop_prompt()
    Display the shopping screen
    -.leave_prompt()
    Asks if you want to leave, gives a summary of items purchased, and guilt trips where necessary
    -.display()
    Main shop loop. Functions as the state machine of sorts.
    -.display_inventory()
    Displays player inventory
    """
    def __init__(self):
        self.image_paths = {'home':'assets/default.txt'}
        self.image = []
        self.state = 'home'
        self.state_list = ["leave", "shop"]
        self.for_sale_lib = {}
        self.for_sale_pro = {}
        self.items_bought = []
        self.libraries = {}
        self.lines = 0
        self.projects = {}
        self.insufficient = False #set to true when there are insufficient funds
        self.invalid = False #set to true when invalid response is given
        self.lib_multiplier_dict = {} #stores the multiplier amounts for objects for sale
        self.pro_multiplier_dict = {}
    
    def load_image(self, state):
        self.image = [] #self image is empty, just like me
        try:
            f = open(self.image_paths[state],'r')
            for line in f:
                self.image.append(line)
            f.close()
        except:
            pass
    
    def print_ASCII(self):
        for line in self.image: 
            print(line, end="")
    
    def init_prompt(self):
        print("What would you like to do?")
        print("Shop / Leave\n\n>>",end='')
        answer =  input().lower()
        if answer in self.state_list:
            self.state = answer
        else:
            self.invalid = True
            
    def update_with_inventory(self, lines, libraries, projects, rate):
        self.libraries = libraries
        self.projects = projects
        self.lines = lines
        self.lines_rate = rate
        
    def update_inventory(self):
        return self.lines, self.libraries, self.projects
    
    def next_purchase(self,item):
        self.display_inventory()
        print("You have " + str(round(self.lines)) + " lines left.", end= ' ')
        print("would you like to buy something else? \n")
        print("Y/N, or A to repeat purchase\n\n>>",end='')
        answer = input().lower()
        if answer == "n":
            self.state = 'leave'
        elif answer == 'y':
            self.state = 'shop'
        elif answer == 'a':
            self.purchase(item)
        else:
            self.invalid = True
    
    def purchase(self, item):
        self.display_inventory()
        if item.lower() in self.for_sale_lib:
            price = self.for_sale_lib[item]
            if price <= self.lines:
                self.lines -= price
                clear()
                try:
                    self.libraries[item.lower()] += 1
                except:
                    self.libraries[item.lower()] = 1
                self.items_bought.append(item.lower())
                print('bought ' + str(item) + "!")
                self.next_purchase(item)
            elif price > self.lines:
                self.insufficient = True
        elif item.lower() in self.for_sale_pro:
            price = self.for_sale_pro[item]
            if price <= self.lines:
                self.lines -= price
                clear()
                try:
                    self.projects[item.lower()] += 1
                except:
                    self.projects[item.lower()] = 1
                self.items_bought.append(item.lower())
                print('bought ' + str(item) + "!")
                self.next_purchase(item)
            elif price > self.lines:
                self.insufficient = True
        else:
            self.invalid = True
        
    
    def shop_prompt(self):
        self.display_inventory()
        print("We have the following items: ")
        for ind, (item, price) in enumerate(self.for_sale_lib.items()):
            print("{} : {} lines, {} lines/sec".format(item, price, self.lib_multiplier_dict[item]*10))
        for ind, (item, price) in enumerate(self.for_sale_pro.items()):
            print("{} : {} lines, {} lines/sec".format(item, price, self.pro_multiplier_dict[item]*10))
        print("\nWhat would you like?")
        print("<type item name> / Leave\n\n>>",end='')
        answer =  input().lower()
        if answer in self.for_sale_lib or answer in self.for_sale_pro:
            self.purchase(answer)
        elif answer == "leave":
            self.state = 'leave'
        else:
            self.invalid = True

            
    def leave_prompt(self):
        self.illegal_items = ['opencv', 'python']
        self.wasted = ['dw1d', 'pygame game']
        #check is any items are bought
        if len(self.items_bought) > 0:
            print("You have purchased: ")
            for index, item in enumerate(self.items_bought):
                print(str(index+1) + '. ' + str(item))
            #checks for hypocrisy
            if any(item in self.items_bought for item in self.illegal_items):
                print("\nOh, you're using external libraries? After you told us not to? Hmmmmm...\n")
                print("Type <do as i say and not as i do> to continue:\n\n>>",end='')
                if input().lower() != "do as i say and not as i do":
                    self.display()
                else:
                    pass
            #checks for undermining of efforts
            elif any(item in self.items_bought for item in self.wasted):
                print("\nAhh investing time in DW projects? Would be a shame if those projects were cancelled...\n")
                print("Type <based on a true story> to continue:\n\n>>",end = '')
                if input().lower() != "based on a true story":
                    self.display()
                else:
                    pass
            else:
                print("Press enter to return:\n\n>>", end= '')
                input()
        #clear list of items bought
        self.items_bought = []
        self.state = 'home'
        return None

    
    def display(self):
        clear()
        self.load_image(self.state)
        self.print_ASCII()
        #checks for invalid actions
        if self.invalid:
            self.invalid = False
            print("invalid action!")
        #checks for insufficient funds
        if self.insufficient:
            self.insufficient = False
            print("insufficient lines!")
        if self.state == 'home':
            self.init_prompt()
            self.display()
        elif self.state == "shop":
            self.shop_prompt()
            self.display()
        elif self.state == "leave":
            self.leave_prompt()
        else:
            self.invalid = True
            self.display()
            
    def display_inventory(self):
        print("\nYour inventory is as follows\n................................")
        print("  Libraries:")
        if len(self.libraries) >0:
            for library, number in self.libraries.items():
                print("  - {}: {}\n".format(library, number))
        else:
            print("  - None\n")
        print("  Projects:")
        if len(self.projects) >0:
            for project, number in self.projects.items():
                print("  - {}: {}".format(project, number))
        else:
            print("  - None\n")
        print("\nLines: {} \n................................\n".format(round(self.lines)))

class library_shop(shop):
    """inherits shop class. Changes relevant attributes"""
    def __init__(self):
        shop.__init__(self)
        self.image_paths = {'home':"assets/library.txt"}
        self.for_sale_lib = {'opencv':10,
                             'pygame':100,
                             'threading':500}
        self.lib_multiplier_dict = {'opencv':0.05,
                                    'pygame':0.6,
                                    'threading':4}
        
class project_shop(shop):
    """inherits shop class. Changes relevant attributes"""
    def __init__(self):
        shop.__init__(self)
        self.image_paths = {'home':"assets/projects.txt"}
        self.for_sale_pro = {'dw1d':1000,
                             'pygame game':10000,
                             'soar project':100000}
        self.pro_multiplier_dict = {'dw1d':10,
                                    'pygame game':100,
                                    'soar project':1000}
