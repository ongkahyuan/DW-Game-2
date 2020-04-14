import time
import os
from shops import clear

while True:
    clear()
    f = open("line_count.txt", "r")
    print(f.readline())
    f.close()
    time.sleep(0.5)