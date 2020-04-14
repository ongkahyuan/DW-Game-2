import threading
import os
import time

def clear(): 
    if os.name == 'nt': 
        os.system('cls') 
    else: 
        os.system('clear')




class shop():
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
        self.insufficient = False
        self.invalid = False
        self.display_inv = False
        self.lib_multiplier_dict = {}
        self.pro_multiplier_dict = {}
    
    def load_image(self, action):
        self.image = []
        try:
            f = open(self.image_paths[action],'r')
            for line in f:
                self.image.append(line)
            f.close()
        except:
            pass
    
    def clear(self): 
        if os.name == 'nt': 
            os.system('cls') 
        else: 
            os.system('clear')
    
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
            self.state = 'home'
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
                self.clear()
                try:
                    self.libraries[item.lower()] += 1
                except:
                    self.libraries[item.lower()] = 1
                self.items_bought.append(item.lower())
                print('bought ' + str(item) + "!")
                self.next_purchase(item)
            elif price > self.lines:
                self.insufficient = True
                # self.display(insufficient = True)
        elif item.lower() in self.for_sale_pro:
            price = self.for_sale_pro[item]
            if price <= self.lines:
                self.lines -= price
                self.clear()
                try:
                    self.projects[item.lower()] += 1
                except:
                    self.projects[item.lower()] = 1
                self.items_bought.append(item.lower())
                print('bought ' + str(item) + "!")
                self.next_purchase(item)
            elif price > self.lines:
                self.insufficient = True
                # self.display(insufficient = True)
        else:
            self.invalid = True
            # self.display(invalid=True)
        
    
    def shop_prompt(self):
        self.display_inventory()
        # print(self.state)
        print("We have the following items: ")
        for ind, (item, price) in enumerate(self.for_sale_lib.items()):
            print("{} : {} lines, {} lines/sec".format(item, price, self.lib_multiplier_dict[item]*10))
            # print(str(item) + ': ' + str(price) + " lines")
        for ind, (item, price) in enumerate(self.for_sale_pro.items()):
            # print(str(item) + ': ' + str(price) + " lines" )
            print("{} : {} lines, {} lines/sec".format(item, price, self.pro_multiplier_dict[item]*10))
        print("\nWhat would you like?")
        print("<type item name> / Leave\n\n>>",end='')
        answer =  input().lower()
        if answer in self.for_sale_lib or item.lower() in self.for_sale_pro:
            self.purchase(answer)
        elif answer == "leave":
            self.state = 'home'
        else:
            self.invalid = True

            
    def leave_prompt(self):
        self.illegal_items = ['opencv', 'python']
        self.wasted = ['dw1d', 'pygame game']
        if len(self.items_bought) > 0:
            print("You have purchased: ")
            for index, item in enumerate(self.items_bought):
                print(str(index+1) + '. ' + str(item))
            if any(item in self.items_bought for item in self.illegal_items):
                print("\nOh, you're using external libraries? After you told us not to? Hmmmmm...\n")
                print("Type <do as i say and not as i do> to continue:\n\n>>",end='')
                if input().lower() != "do as i say and not as i do":
                    self.display()
                else:
                    pass
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
        self.items_bought = []
        self.state = 'home'
        return None

    
    def display(self, invalid = False, insufficient = False):
        self.clear()
        self.load_image(self.state)
        self.print_ASCII()
        if self.invalid:
            self.invalid = False
            print("invalid action!")
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
        print("Lines: {} \n................................\n".format(round(self.lines)))

class library_shop(shop):
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
    def __init__(self):
        shop.__init__(self)
        self.image_paths = {'home':"assets/projects.txt"}
        self.for_sale_pro = {'dw1d':1000,
                             'pygame game':10000,
                             'soar project':100000}
        self.pro_multiplier_dict = {'dw1d':10,
                                    'pygame game':100,
                                    'soar project':1000}
