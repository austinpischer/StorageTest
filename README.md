# StorageTest

## Project Context
This is a small project to teach myself the basics of Python and MySQL

## Theory of Operation
This project does three main things:
1. Create a file on each drive of my computer
2. Stores data about the file creation on a local MySQL database (i.e. write/read times)
3. Creates a graph showing the average write/read speed of each drive

"runtests.py" creates files and stores data in the database.
"getgraph.py" creates a graph with data queried from the database.

All other source code files are supplementary to these 2 scripts and thus live in the "austin" subdirectory.

The database schema is represented by the following diagram ( created at https://dbdiagram.io/d ):
// TODO

After executing runtests.py (test file size = 100 Megabytes, write/read cycles = 250 times to each drive)
and then executing getgraph.py, the following graph is created:
// TODO

## Rules for Code Appearance
1. No line of code should exceed 80 characters in length
2. The exception to rule one is for comments with links
3. Each file should have a header comment with expository information
4. Each file should have an end of file comment after the last line of code
5. Each logical subsection of the code should have a noticable subsection comment
(Visual Studio Code snippets for these comments can be found in the .vscode directory)
6. Variable/Function/Class names should be written in UpperCamelCase
7. Optimize for read-time over write time -- name things what they are, not what is convenient to write.
