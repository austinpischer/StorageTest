"""=============================================================================
Project: StorageTest
Author: Austin Pischer
Date: 2020-10-04

File Name: testfile.py
File Description: This file defines the TestFile class. The TestFile class
is meant to abstract the process of creating and deleting a file, generating
a checksum for the file, and measuring the amount of time it takes to write and
then read the file to the drive.
============================================================================="""

# ==============================================================================
# Import Library Modules
# ==============================================================================
import hashlib
import os

# ==============================================================================
# Import local modules
# ==============================================================================
from austin import timer  # Written for this project

# ==============================================================================
# Helper Function
# ==============================================================================


def GetChecksum(String):
    Checksum = hashlib.sha256()
    Checksum.update(String.encode('ascii'))
    return Checksum.hexdigest()  # Outputs readable checksum

# ==============================================================================
# Test File Class
# ==============================================================================


class TestFile:
    def __init__(self, Path, Name, Contents):
        self.Path = Path
        self.Name = Name
        self.FullPath = os.path.join(Path, Name)
        self.Handle = self.CreateFile()

        self.WriteTime = timer.Timer()
        self.ReadTime = timer.Timer()

        self.Contents = Contents
        self.PopulateFile()
        self.Checksum = self.GetVerificationChecksum()

    def CreateFile(self):
        if os.path.isfile(self.FullPath):
            os.remove(self.FullPath)
        return open(self.FullPath, 'wt+')  # w = write, t = text, + = also read

    def Delete(self):
        # TODO: Potentially redundant functions
        self.Handle.close()
        os.remove(self.FullPath)

    def PopulateFile(self):
        self.WriteTime.StartTimer()
        self.Handle.write(self.Contents)
        self.WriteTime.EndTimer()

    def GetVerificationChecksum(self):
        self.Handle.seek(0)
        self.ReadTime.StartTimer()
        FileContents = self.Handle.read()
        # print("READ:{}".format(FileContents))
        self.ReadTime.EndTimer()
        return(GetChecksum(FileContents))
# END OF FILE
