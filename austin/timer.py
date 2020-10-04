"""=============================================================================
Project: StorageTest
Author: Austin Pischer
Date: 2020-10-04

File Name: timer.py
File Description: This file defines the Timer class. The Timer class is meant
to abstract the process of getting the runtime duration of a section of code.
The Timer class also makes the code that uses it more readable.
============================================================================="""

# ==============================================================================
# Import Module from Library
# ==============================================================================
import time

# ==============================================================================
# Timer Class
# ==============================================================================
class Timer:
    def __init__(self):
        self.Start = 0.0
        self.End = -1.0
        self.Duration = self.End-self.Start

    def StartTimer(self):
        self.Start = time.time()

    def EndTimer(self):
        self.End = time.time()
        self.CalculateDuration()

    def CalculateDuration(self):
        self.Duration = self.End-self.Start

# END OF FILE