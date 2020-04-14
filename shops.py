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
        self.image_path = 'assets/default.txt'
        self.image = []
        self.action = ''
        self.action_list = ["leave", "shop"]
        self.for_sale_lib = {}
        self.for_sale_pro = {}
        self.items_bought = []
        self.libraries = []
        self.lines = []
        self.projects = []
        self.insufficient = False
        self.invalid = False
    
    def load_image(self):
        self.image = []
        f = open(self.image_path,'r')
        for line in f:
            self.image.append(line)
        f.close()
    
    def clear(self): 
        if os.name == 'nt': 
            os.system('cls') 
        else: 
            os.system('clear')
    
    def print_ASCII(self):
        for line in self.image: 
            print(line, end="")
    
    def init_prompt(self):
        self.print_ASCII()
        print("What would you like to do?")
        print("Shop / Leave")
        answer =  input().lower()
        if answer in self.action_list:
            self.action = answer
            # self.display()
            # return None
        else:
            self.invalid = True
            
            # self.display(invalid=True)
            
    def update_with_inventory(self, lines, libraries, projects):
        self.libraries = libraries
        self.projects = projects
        self.lines = lines
        
    def update_inventory(self):
        return self.lines, self.libraries
    
    def next_purchase(self,item):
        print("You have " + str(round(self.lines)) + " left.")
        print("would you like to buy something else? ")
        print("Y/N, or A to repeat purchase")
        answer = input().lower()
        if answer == "n":
            self.action = ''
        elif answer == 'y':
            pass
        elif answer == 'a':
            self.purchase(item)
        else:
            self.invalid = True
        
    
    def purchase(self, item):
        if item.lower() in self.for_sale_lib:
            price = self.for_sale_lib[item]
            if price <= self.lines:
                self.lines -= price
                self.clear()
                self.libraries.append(item.lower())
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
                self.projects.append(item.lower())
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
        print("We have the following items: ")
        for ind, (item, price) in enumerate(self.for_sale_lib.items()):
            print(str(item) + ': ' + str(price) + " lines")
        print("\n")
        for ind, (item, price) in enumerate(self.for_sale_pro.items()):
            print(str(ind+1) + '. ' + str(item) + ': ' + str(price) )
        print("What would you like buy?")
        print("<type item name> / Leave")
        answer =  input().lower()
        if item.lower() in self.for_sale_lib or item.lower() in self.for_sale_pro:
            self.purchase(answer)
        elif answer == "leave":
            self.action = ''
            # return None
            # self.display()
        else:
            self.invalid = True
            # self.display(invalid=True)
            
    def leave_prompt(self):
        if len(self.items_bought) > 0:
            print("You have purchased: ")
            for index, item in enumerate(self.items_bought):
                print(str(index+1) + '. ' + str(item))
        print("Press enter to return...")
        input()
        self.action = ''
        return None
        # self.action = 'exit'
        # self.display()
        # print("Y / N")
        # answer = input()
        # if answer.lower() == "n":
        #     self.action = ''
        #     self.display()
        # else:
        #     self.action = ''
    
    def display(self, invalid = False, insufficient = False):
        self.load_image()
        self.items_bought = []
        self.clear()
        if self.invalid:
            self.invalid = False
            print("invalid action!")
        if self.insufficient:
            self.insufficient = False
            print("insufficient lines!")
        if self.action == '':
            self.init_prompt()
            self.display()
        elif self.action == "shop":
            self.shop_prompt()
            self.display()
        elif self.action == "leave":
            self.leave_prompt()
        else:
            self.invalid = True
            self.display()
        # elif self.action == "exit":
        #     self.action = ''

class library_shop(shop):
    def __init__(self):
        shop.__init__(self)
        self.image_path = "assets/library.txt"
        self.for_sale_lib = {'pygame':10,'turtle':20,'threading':30}
        
class project_shop(shop):
    def __init__(self):
        shop.__init__(self)
        self.image_path = "assets/projects.txt"
        self.for_sale_pro = {'DW1D':10,'pygame game':20,'SOAR Project':30}


class shop_selector(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.libraries = []
        self.projects = []
        self.stopped = False
        self.in_shop = False
        self.shop = ''
        

        
    def library_shop(self):
        # while self.in_shop == True:
        self.clear()
        print("\033[2;37;40m This is a library\033[0;37;40m \n")
        print("make purchase")
        print("\033[2;37;40m \033[0;37;40m \n")
        print("What would you like to do?")
        self.shop = input()
        self.in_shop = True
        # self.shop = ''
            
    def project_shop(self):
        # while self.in_shop == True:
        self.clear()
        print("\033[2;37;40m This is a project shop\033[0;37;40m \n")
        print("make purchase")
        print("\033[2;37;40m \033[0;37;40m \n")
        self.shop = input()
        self.in_shop = True
        # self.shop = ''
            
    def home(self):
        # while self.in_shop == False:
        self.clear()
        print("\033[2;37;40m This is home\033[0;37;40m \n")
        print("Welcome home")
        print("number of lines = ")
        print("\033[2;37;40m \033[0;37;40m \n")
        
            
    def stop(self):
        self.stopped = True
    
    def display(self, lines):
        if self.shop == "library":
            self.library_shop()
        elif self.shop == "project":
            self.project_shop()
        else:
            self.home()    
        
    def run(self):
        while not self.stopped:
            if self.shop == "library":
                self.library_shop()
            elif self.shop == "project":
                self.project_shop()
            else:
                self.home()
            time.sleep(4)    
        
    