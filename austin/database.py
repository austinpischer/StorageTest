"""=============================================================================
Project: StorageTest
Author: Austin Pischer
Date: 2020-10-04

File Name: database.py
File Description: This file defines the MySQL class. This class is meant to
abstract the interface for the Python/MySQL connector specifically for this 
project.
============================================================================="""

# ==============================================================================
# Import Library Modules
# ==============================================================================
import mysql.connector
# https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.html
from mysql.connector import errorcode
import sys  # For exiting on errors

# ==============================================================================
# MySQL Class
# ==============================================================================


class MySQL:
    def __init__(self, User, Password, Host, DatabaseName):
        self.Connection = self.Connect(User, Password, Host)
        self.Cursor = self.Connection.cursor()
        self.CreateDatabase(DatabaseName)

    def Connect(self, User, Password, Host):
        # https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
        from mysql.connector import errorcode
        try:
            Connection = mysql.connector.connect(
                user=User,
                password=Password,
                host=Host,
            )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                sys.exit("Something is wrong with your user name or password")
            else:
                sys.exit(err)
        else:
            return(Connection)

    def CreateDatabase(self, Name):
        # https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html
        # Try to access database
        try:
            self.Cursor.execute("USE {}".format(Name))
        # If database doesn't exist, try to create it
        except mysql.connector.Error as err:
            print("Database {} does not exist.".format(Name))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                try:
                    self.Cursor.execute("CREATE DATABASE {}".format(Name))
                except mysql.connector.Error as err:
                    sys.exit("Failed creating database: {}".format(err))
                else:
                    print("Database {} created successfully.".format(Name))
                    self.Connection.database = Name
            else:
                sys.exit(err)  # Exit on any other database use errors

    def CreateTables(self, CreateTableStatements):
        # https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html
        for TableName in CreateTableStatements:
            CreateTableStatement = CreateTableStatements[TableName]
            try:
                # end='' replaces newline at end of print output with empty character
                print("Creating table {}: ".format(TableName))
                self.Cursor.execute(CreateTableStatement)
            except mysql.connector.Error as err:
                print(err.msg)

    def Insert(self, InsertStatement, Record):
        try:
            self.Cursor.execute(InsertStatement, Record)
        except mysql.connector.Error as err:
            print("ERROR inserting record: {}".format(err))
            return(err.errno)
        else:
            self.Connection.commit()

    def Update(self, UpdateStatement, Record):
        try:
            self.Cursor.execute(UpdateStatement, Record)
        except mysql.connector.Error as err:
            print("Error updating record: {}".format(err))
        else:
            self.Connection.commit()
            print("Updated record for {}:\\ drive.".format(
                Record['drive_letter']))
# END OF FILE
