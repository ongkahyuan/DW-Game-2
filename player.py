import time
import threading
       
class inventory(threading.Thread):
    def __init__(self, tick_time = 0.1):
        threading.Thread.__init__(self)
        self.libraries = []
        self.projects = []
        self.lines = 0
        self.tick_time = tick_time
        self.multiplier = 0
        self.stopped = False
        self.paused = False
        
    def add_line(self):
        self.lines += 1
        
    # def add_library(self, library_name):
    #     self.libraries.append(library_name)
        
    # def add_project(self, project_name):
    #     self.projects.append(project_name)
    
    def stop(self):
        self.stopped = True
        
    def pause(self):
        self.paused = True
        
    def resume(self):
        self.paused = False
        
    def set_multiplier(self):
        self.multiplier = 0
        if not self.paused:
            for library in self.libraries:
                if library == "threading":
                    self.multiplier += 0.3
                elif library == "pygame":
                    self.multiplier += 0.1
            for project in self.projects:
                if project == "soar":
                    self.multiplier += 0.2
                elif project == "1d":
                    self.multiplier -= 1 
        else:
            self.multiplier = 0

    def run(self):
        while not self.stopped:
            self.set_multiplier()
            self.lines += 1* self.multiplier
            f = open("line_count.txt", "w+")
            f.write(str(round(self.lines)))
            f.close()
            time.sleep(self.tick_time)
        self.lines = 0
        f = open("line_count.txt", "w+")
        f.write(str(round(self.lines)))
        f.close()
            
            