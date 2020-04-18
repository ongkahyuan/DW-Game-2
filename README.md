# DW-Game-2: Code Master
## Introduction to the game:

Welcome to Code Master! Loosely based on Universal Paperclips, the aim of this game to is become the best coder - and we all know that more is better - so that means writing the most lines of code.

At its core, the game is simple: enter "a" to code a line. That will add one line to the player's inventory. There are other ways to produce code however: libraries and projects.

As in real life, the code libraries here do the heavy lifting. They increase the lines of code you produce per second. They can be "purchased" with the lines of code that you have in your inventory. 

Projects on the other hand, demand many more lines of code. But they also produce more lines of code per second. These are a late game item, purchasable in the store. 

## Game Structure Overview

The structure of the game is as follows:

> 1. Intro Screen
> 2. The Actual Game
>    - Main Screen
>      - Monitor (to check state of lines)
>      - Library (shop, to buy items)
>      - Projects (shop, to buy items)
> 3. End Screen

The intro screen provides an overview of the game, while the exit screen shows a summary of the score. 

The main screen on the other hand, is the main space of interaction for the player. From here, the player can see an inventory of their items, as well as visit the various shops to purchase items. The monitor screen also allows real-time monitoring of line production.

## Code Structure



```
main.py
|-- class selector(sm.SM)
|-- class main()
assets
|-- player.py
	|-- class inventory(threading.Thread)
|-- shops.py
	|-- class shop()
	|-- class library(shop)
	|-- class project(shop)
|-- default.txt
|-- end.txt
|-- end_speech.txt
|-- library.txt
|-- logo.txt
|-- projects.txt
|-- welcome.txt
```

### State Machines

The game consists of a nested state machine. The diagram is as follows:

![State Diagram](assets\states.png)



The section in blue is a loop that uses the sm.SM class. This is the main game loop, and is how the player progresses through the various stages of the game. The pseudo-code below shows an approximation of the process flow:

```python
sm = state_machine()
main_obj = main()

sm.start()
while True:
    if sm.state() ==  "intro":
        #run intro screen method, which returns next state:
        sm.step(main.intro_screen())
    elif sm.state() == "main":
    	#run main screen method, which returns next state:
        sm.step(main.main_screen())
    elif sm.state() == "end":
        #run main screen method, which returns next state:
        sm.step(main.end_screen())
    elif sm.state() == "leave":
        break
#end
```

In contrast, the red section, held within the "shop" type object (and it's variations, library and project), is done recursively in something that approximates to a state machine.  It is called when the `main_screen()` method calls the shop object's `display()` method. The pseudocode for this section, which allows the player to access shops and make purchases, is shown below:

```python
def display(self):
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
```

### Parallel Processing

The `player(threading.Thread)` class runs in parallel on a separate thread. This is to keep track of the number of lines produced by the player in real time. The thread is started in the main script. 