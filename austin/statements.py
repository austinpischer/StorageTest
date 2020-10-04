"""=============================================================================
Project: StorageTest
Author: Austin Pischer
Date: 2020-10-04

File Name: statements.py
File Description: This file contains MySQL statements to be executed by the 
MySQL cursor execute() function. These statements are grouped in dictionaries
by type to make the code that references them as readable as possible.

Some statements use extended formatting: %(<key>)s
Those statements must be passed to execute() with a dictionary whose keys 
math the keys in the statement. The result is that 
execute(<statement>, <dictionary>) will replace the extended formatting with
the values of the corresponding dictionary keys.
============================================================================="""

# ==============================================================================
# Create Table Statement Dictionary
# ==============================================================================
# https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
CreateTable = {
    'tests': (
        "CREATE TABLE IF NOT EXISTS tests ("
        " test_id INTEGER AUTO_INCREMENT PRIMARY KEY,"
        " timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,"
        " group_id INTEGER,"
        " drive_id INTEGER,"
        " write_duration FLOAT,"
        " read_duration FLOAT,"
        " data_error BOOL"
        ")"),
    'test_groups': (
        "CREATE TABLE IF NOT EXISTS test_groups ("
        " group_id INTEGER AUTO_INCREMENT PRIMARY KEY,"
        " filesize_in_bytes INTEGER,"
        " checksum VARCHAR(255)"
        ")"),
    'drives': (
        "CREATE TABLE IF NOT EXISTS drives ("
        " drive_id INTEGER AUTO_INCREMENT PRIMARY KEY,"
        " drive_letter VARCHAR(255) UNIQUE,"
        " volume_name VARCHAR(225),"
        " drive_type VARCHAR(255),"
        " manufacturer VARCHAR(255),"
        " model VARCHAR(255),"
        " capacity_in_gigabytes INT,"
        " filesystem VARCHAR(255)"
        ")"),
}

# ==============================================================================
# Insert Record Statement Dictionary
# ==============================================================================
# https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html
Insert = {
    'tests': (
        "INSERT INTO tests ("
        " group_id,"
        " drive_id,"
        " write_duration,"
        " read_duration,"
        " data_error"
        ") VALUES ("
        "%(group_id)s,"
        " %(drive_id)s,"
        " %(write_duration)s,"
        " %(read_duration)s,"
        " %(data_error)s"
        ")"),
    'test_groups': (
        "INSERT INTO test_groups ("
        " filesize_in_bytes,"
        " checksum"
        ") VALUES ("
        "%(filesize_in_bytes)s,"
        " %(checksum)s"
        ")"),
    'drives': (
        "INSERT INTO drives ("
        " drive_letter,"
        " volume_name,"
        " drive_type,"
        " manufacturer,"
        " model,"
        " capacity_in_gigabytes,"
        " filesystem"
        ") VALUES ("
        "%(drive_letter)s,"
        " %(volume_name)s,"
        " %(drive_type)s,"
        " %(manufacturer)s,"
        " %(model)s,"
        " %(capacity_in_gigabytes)s,"
        " %(filesystem)s"
        ")"),
}

# ==============================================================================
# Update Record Statement Dictionary
# ==============================================================================
Update = {
    'drives': (
        "UPDATE drives "
        "SET"
        " volume_name = %(volume_name)s,"
        " drive_type = %(drive_type)s,"
        " manufacturer = %(manufacturer)s,"
        " model = %(model)s,"
        " capacity_in_gigabytes = %(capacity_in_gigabytes)s,"
        " filesystem = %(filesystem)s"
        # Not sure if drive_letter will be placed here regardless of order of dictionary used in cursor.execute()
        " WHERE drive_letter = %(drive_letter)s"
    ),
}
# END OF FILE
