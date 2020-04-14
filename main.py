import os
from shops import *
from player import inventory

shop_obj = shop()
lib_obj = library_shop()
inventory_obj = inventory()
pro_obj = project_shop()

inventory_obj.start()

def main_screen(invalid = False):
    while True:
        clear()
        if invalid:
            print("Invalid!")
        print(lib_obj.action)
        print("Total Lines: " + str(round(inventory_obj.lines)))
        print("libraries: " + str(inventory_obj.libraries))
        print("Coding Rate: " + str(round(inventory_obj.multiplier*10)) + " lines / sec")
        print('press <enter> to write code, or <library> or <project> to enter the shop, or <exit> to exit:')
        answer = input().lower()
        if answer == '':
            inventory_obj.add_line()
        elif answer == 'library':
            print("in")
            inventory_obj.pause()
            lib_obj.update_with_inventory(inventory_obj.lines,inventory_obj.libraries,inventory_obj.projects)
            lib_obj.display()
            inventory_obj.lines, inventory_obj.libraries= lib_obj.update_inventory()
            inventory_obj.resume()
        elif answer == 'project':
            inventory_obj.pause()
            pro_obj.update_with_inventory(inventory_obj.lines,inventory_obj.libraries,inventory_obj.projects)
            pro_obj.display()
            inventory_obj.lines, inventory_obj.projects= pro_obj.update_inventory()
            inventory_obj.resume()
        elif answer == "exit":
            break
        else:
            main_screen(invalid=True)
            

main_screen()    

# lib_obj.display()

# shop_obj.display()
inventory_obj.stop()
input("press enter to exit: ")

# shop_obj = shop_selector()

# # shop_obj.start()

# while True:
#     print("in")
#     if shop_obj.shop == '':
#         shop_obj.display()
#     elif shop_obj.shop != '' and shop_obj.in_shop == True:
#         shop_obj.display()
#         print("would you like to leave? (Y/N):")
#         leave = input()
#         if leave =="Y":
#             shop_obj.in_shop = False
#             shop_obj.shop = ''
#         else:
#             continue
#     else:
#         print("exception!")
            
# shop_obj.stop()

# for i in range(10):
#     print("blah")
    
# input("press enter")

# def clear(): 
#     # for windows 
#     if os.name == 'nt': 
#         _ = os.system('cls') 
  
#     # for mac and linux(here, os.name is 'posix') 
#     else: 
#         _ = os.system('clear')

# clear()


# print("\033[2;37;40m Underlined text\033[0;37;40m \n")
# print("\033[1;37;40m Bright Colour\033[0;37;40m \n")
# print("\033[3;37;40m Negative Colour\033[0;37;40m \n")
# print("\033[5;37;40m Negative Colour\033[0;37;40m\n")
 
# print("\033[1;37;40m \033[2;37:40m TextColour BlackBackground          TextColour GreyBackground                WhiteText ColouredBackground\033[0;37;40m\n")
# print("\033[1;30;40m Dark Gray      \033[0m 1;30;40m            \033[0;30;47m Black      \033[0m 0;30;47m               \033[0;37;41m Black      \033[0m 0;37;41m")
# print("\033[1;31;40m Bright Red     \033[0m 1;31;40m            \033[0;31;47m Red        \033[0m 0;31;47m               \033[0;37;42m Black      \033[0m 0;37;42m")
# print("\033[1;32;40m Bright Green   \033[0m 1;32;40m            \033[0;32;47m Green      \033[0m 0;32;47m               \033[0;37;43m Black      \033[0m 0;37;43m")
# print("\033[1;33;40m Yellow         \033[0m 1;33;40m            \033[0;33;47m Brown      \033[0m 0;33;47m               \033[0;37;44m Black      \033[0m 0;37;44m")
# print("\033[1;34;40m Bright Blue    \033[0m 1;34;40m            \033[0;34;47m Blue       \033[0m 0;34;47m               \033[0;37;45m Black      \033[0m 0;37;45m")
# print("\033[1;35;40m Bright Magenta \033[0m 1;35;40m            \033[0;35;47m Magenta    \033[0m 0;35;47m               \033[0;37;46m Black      \033[0m 0;37;46m")
# print("\033[1;36;40m Bright Cyan    \033[0m 1;36;40m            \033[0;36;47m Cyan       \033[0m 0;36;47m               \033[0;37;47m Black      \033[0m 0;37;47m")
# print("\033[1;37;40m White          \033[0m 1;37;40m            \033[0;37;40m Light Grey \033[0m 0;37;40m               \033[0;37;48m Black      \033[0m 0;37;48m")


# input("wait...")