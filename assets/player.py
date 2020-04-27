import time
import threading
from assets.shops import clear
       
class inventory(threading.Thread):
    """
    Class that manages the player inventory. Keeps track of lines and bought items. 
    
    Methods
    ====
    - __init__(tick_time)
    Inits the object. tick_time sets the game speed and refresh rate in seconds. Default is 0.1s (10Hz)
    - .add_line() 
    Adds a line
    - .start()
    Starts a new thread, adds lines according to the rate of production
    - .pause()
    Pauses the production of lines
    - .stop()
    Ends the thread, stopping production. Only on exit. 
    - .monitor()
    Enables the continuous printing of the current number of lines to the console. Only when in monitor mode
    - .stop_monitor()
    Stops monitoring
    - .set_multiplier()
    Sets the correct rate of line production according to items in inventory
    
    Attributes
    ====
     
    """
    def __init__(self, tick_time = 0.2):
        """
        Inits the object. tick_time sets the game speed and refresh rate in seconds. Default is 0.1s (10Hz) 
        """
        threading.Thread.__init__(self)
        self.libraries = {}
        self.projects = {}
        self.lines = 150
        self.tick_time = tick_time
        self.multiplier = 0
        self.stopped = False
        self.paused = False
        self.verbose = False
        self.lib_multiplier_dict = {'opencv':0.05*2,
                                    'pygame':0.6*2,
                                    'threading':4*2}
        self.pro_multiplier_dict = {'dw1d':10*2,
                                    'pygame game':100*2,
                                    'soar project':1000*2}
        
    def add_line(self):
        self.lines += 1
    
    def stop(self):
        self.stopped = True
        
    def pause(self):
        self.paused = True
        
    def resume(self):
        self.paused = False
        
    def monitor(self):
        self.verbose = True
        
    def stop_monitor(self):
        self.verbose = False
        
    def set_multiplier(self):
        """"
        
        """
        self.multiplier = 0
        if not self.paused:
            for library, number in self.libraries.items():
                self.multiplier += self.lib_multiplier_dict[library]*number
            for project, number in self.projects.items():
                self.multiplier += self.pro_multiplier_dict[project]*number
        else:
            self.multiplier = 0

    def run(self):
        while not self.stopped:
            start = time.time()
            if self.verbose:
                clear()
                print("Lines: {}".format(round(self.lines)))
                print("press enter to exit:\n>>", end = '')
            self.set_multiplier()
            self.lines += 1* self.multiplier
            try:
                time.sleep(self.tick_time-(time.time()-start))
            except:
                print("your computer is slow")
                print(self.tick_time-(time.time()-start))
        self.lines = 0

            
            