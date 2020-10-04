"""=============================================================================
Project: StorageTest
Author: Austin Pischer
Date: 2020-10-04

File Name: runtests.py
File Description: This script runs one groups of tests. Each group of tests

============================================================================="""

# ==============================================================================
# Import Library Modules
# ==============================================================================
import mysql.connector
# https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.html
from mysql.connector import errorcode
import string
import random
import sys  # For sys.exit() https://www.geeksforgeeks.org/python-exit-commands-quit-exit-sys-exit-and-os-_exit/
import os
import matplotlib.pyplot as pyplot
import numpy

# ==============================================================================
# Import Local Modules
# ==============================================================================
from austin import testfile
from austin import statements
from austin import database
from austin import drive

# ==============================================================================
# Function Definitions
# ==============================================================================


def GetRandomString(StringLength):
    """
    Explanation: Joining a set of elements (with size of k) whose elements
    are randomly chosen from the set of ascii characters. Each element
    is joined by an empty separator string ('').
    """
    return(''.join(random.choices(string.ascii_lowercase, k=StringLength)))


def MakeDirectory(Path):
    try:
        os.mkdir(Path)
    except FileExistsError as Error:
        print(Error)


def RemoveDirectory(Path):
    try:
        os.rmdir(Path)
    except OSErrorr as Error:
        print(Error)


def GetVolumeNames(Cursor):
    Cursor.execute("SELECT drive_id, volume_name FROM drives")
    return(Cursor.fetchall())


def GetDrivePaths(Cursor):
    Cursor.execute("SELECT drive_id, drive_letter FROM drives")
    QueryResults = Cursor.fetchall()
    Paths = {}
    for Pair in QueryResults:
        # Key is root path of each drive, value is drive ID
        # todo refactor DirectoryName
        Paths[os.path.join(Pair[1] + ":" + os.sep)] = Pair[0]
    return(Paths)


# ===============================================================================
# Start of script execution
# ===============================================================================


# Connect to local database
Database = database.MySQL("root",
                          "VGwYqWqef^Zz4SV!txNnEM*!",
                          "127.0.0.1",
                          "storage_test")

# Make sure the database has the proper tables to store test data
Database.CreateTables(statements.CreateTable)

# Add or update the test drives in the database
for Drive in drive.DriveList:
    Error = Database.Insert(statements.Insert['drives'], Drive.Record)
    if(Error == errorcode.ER_DUP_ENTRY):
        Database.Update(statements.Update['drives'], Drive.Record)


# Set up the properties of this group of tests
FileSize_Bytes = 1*1000000  # 1 Megabyte
FileContents = GetRandomString(FileSize_Bytes)
KnownChecksum = testfile.GetChecksum(FileContents)
# Add this group of tests to the database
GroupRecord = {
    'filesize_in_bytes': FileSize_Bytes,
    'checksum': KnownChecksum,
}
Database.Insert(statements.Insert['test_groups'], GroupRecord)
GroupID = Database.Cursor.getlastrowid()  # Get the auto incremented id value


# Test Setup
Cycles = 100
DrivePaths = GetDrivePaths(Database.Cursor)

# List of directories to be cleaned up after running tests
TestDirectories = []
HaveTestDirectoriesBeenCreated = False

# Execute test "Cycles" times on each drive
for Test in range(Cycles):
    for DrivePath in DrivePaths:

        TestDirectory = os.path.join(DrivePath, "StorageTest")
        
        # Intent here is for test directories to only be created once per group
        if(HaveTestDirectoriesBeenCreated == False):
            MakeDirectory(TestDirectory)
            TestDirectories.append(TestDirectory)

        # Write the test file
        # print("KNOW:{}".format(FileContents))
        File = testfile.TestFile(TestDirectory, 'TestFile.txt', FileContents)
        print("File Created at {}: {}".format(
            TestDirectory, os.listdir(TestDirectory)))

        # Gather data error info
        DataError = 1
        if KnownChecksum == File.Checksum:
            DataError = 0

        # Pack test data
        # Accessing "Paths" dictionary value given key value "Path"
        DriveID = DrivePaths[DrivePath]

        # Add this test to the database
        TestRecord = {
            'group_id': GroupID,
            'drive_id': DriveID,
            'write_duration': File.WriteTime.Duration,
            'read_duration': File.ReadTime.Duration,
            'data_error': DataError,
        }
        Database.Cursor.execute(statements.Insert['tests'], TestRecord)
        Database.Connection.commit()  # Commit test record to the database

        File.Delete()
        print("File Deleted at {}: {}".format(
            TestDirectory, os.listdir(TestDirectory)))
    HaveTestDirectoriesBeenCreated = True

# Clean up empty test directories
for TestDirectory in TestDirectories:
    RemoveDirectory(TestDirectory)

Database.Cursor.close()
Database.Connection.close()
