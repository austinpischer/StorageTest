"""=============================================================================
Project: StorageTest
Author: Austin Pischer
Date: 2020-10-04

File Name: drive.py
File Description: This file defines the Drive class. A Drive class instance
holds a record to be inserted into the MySQL database's "drives" table.

We do not define a class for other types of records, group and test, because
the record need only be defined once in runtest.py, whereas the a drive record
must be created for each drive.

This file also defines a list of Drive instances for use in runtest.py
============================================================================="""

# ==============================================================================
# Drive Class
# ==============================================================================


class Drive:
    def __init__(self,
                 drive_letter,
                 volume_name,
                 drive_type,
                 manufacturer,
                 model,
                 capacity_in_gigabytes,
                 filesystem):
        self.Record = {
            "drive_letter": drive_letter,
            "volume_name": volume_name,
            "drive_type": drive_type,
            "manufacturer": manufacturer,
            "model": model,
            "capacity_in_gigabytes": capacity_in_gigabytes,
            "filesystem": filesystem,
        }


# ==============================================================================
# Drive List
# ==============================================================================
DriveList = [
    Drive("C",
          "PrimarySSD",
          "Solid State Drive",
          "Samsung",
          "840 EVO 120GB",
          111.27,
          "NTFS"),

    Drive("D",
          "SecondarySSD",
          "Solid State Drive",
          "Samsung",
          "840 PRO Series",
          238.47,
          "NTFS"),

    Drive("E",
          "ExternalHDD",
          "Hard Disk Drive",
          "HGST",
          "Travelstar 7K1000",
          931.51,
          "NTFS"),

    Drive("F",
          "PrimaryHDD",
          "Hard Disk Drive",
          "Western Digital",
          "WD10EZEX-00ZF5A0",
          931.39,
          "NTFS"),
]
# END OF FILE