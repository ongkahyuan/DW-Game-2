import time
import threading
from shops import clear
       
class inventory(threading.Thread):
    def __init__(self, tick_time = 0.1):
        threading.Thread.__init__(self)
        self.libraries = {}
        self.projects = {}
        self.lines = 0
        self.tick_time = tick_time
        self.multiplier = 0
        self.stopped = False
        self.paused = False
        self.verbose = False
        self.lib_multiplier_dict = {'opencv':0.05,
                                    'pygame':0.6,
                                    'threading':4}
        self.pro_multiplier_dict = {'dw1d':10,
                                    'pygame game':100,
                                    'soar project':1000}
        
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
            if self.verbose:
                clear()
                print("Lines: {}".format(round(self.lines)))
                # print(f.readline())
                # f.close()
                print("press enter to exit:\n>>", end = '')
            self.set_multiplier()
            self.lines += 1* self.multiplier
            # f = open("line_count.txt", "w+")
            # f.write(str(round(self.lines)))
            # f.close()
            time.sleep(self.tick_time)
        self.lines = 0
        # f = open("line_count.txt", "w+")
        # f.write(str(round(self.lines)))
        # f.close()
            
            