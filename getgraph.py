# ==============================================================================
# Import Modules from Libraries
# ==============================================================================
import numpy
import matplotlib.pyplot as pyplot

# ==============================================================================
# Import files from local directory
# ==============================================================================
from austin import database

# ==============================================================================
# Start of script execution
# ==============================================================================
# Connect to local database
Database = database.MySQL("root",
                          "VGwYqWqef^Zz4SV!txNnEM*!",
                          "127.0.0.1",
                          "storage_test")

# Get the average read and write times of each drive
Database.Cursor.execute(
    "SELECT"
    " d.volume_name,"
    " g.filesize_in_bytes,"
    " t.write_duration,"
    " t.read_duration"
    " FROM tests t"
    " LEFT JOIN drives d USING(drive_id)"
    " LEFT JOIN test_groups g USING(group_id)"
)
QueryResults = Database.Cursor.fetchall()
DriveData = {}
for Test in QueryResults:
    VolumeName = Test[0]
    FileSizeInBytes = Test[1]
    WriteDuration = Test[2]
    ReadDuration = Test[3]

    FileSizeInMegaBytes = FileSizeInBytes/1000000

    if (not (VolumeName in DriveData)):
        DriveData[VolumeName] = {'WriteSpeeds_mbps': [], 'ReadSpeeds_mbps': []}

    DriveData[VolumeName]['WriteSpeeds_mbps'].append(
        FileSizeInMegaBytes/WriteDuration)
    DriveData[VolumeName]['ReadSpeeds_mbps'].append(
        FileSizeInMegaBytes/ReadDuration)

# Bar Graph Data
Labels = []
AverageWriteSpeeds_mbps = []
AverageReadSpeeds_mbps = []

# Populate Bar Graph Data
for Drive, Data in DriveData.items():
    # Get get volume name as label for drive data
    Labels.append(Drive)

    def GetAverage(Array):
        return(numpy.mean(numpy.array(Array)))
    AverageWriteSpeeds_mbps.append(GetAverage(Data['WriteSpeeds_mbps']))
    AverageReadSpeeds_mbps.append(GetAverage(Data['ReadSpeeds_mbps']))

print(Labels)
print(AverageWriteSpeeds_mbps)
print(AverageReadSpeeds_mbps)

# Create a grouped bar chart with labels: https://matplotlib.org/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py
# a-range as in Axis Range?, not arrange
LabelLocations = numpy.arange(len(Labels))
BarWidth = 0.35
Figure, Axes = pyplot.subplots()
WriteBars = Axes.bar(LabelLocations - BarWidth/2,
                     AverageWriteSpeeds_mbps,
                     BarWidth,
                     label='Average Write Speed (MB/s)')
ReadBars = Axes.bar(LabelLocations + BarWidth/2,
                    AverageReadSpeeds_mbps,
                    BarWidth,
                    label='Average Read Speed (MB/s)')
Axes.set_ylabel('Seconds')
Axes.set_title('Average Write/Read Speeds')
Axes.set_xticks(LabelLocations)
Axes.set_xticklabels(Labels)
Axes.legend()
# Put bar values at the top of bars


def AutoLabel(Bars):
    for Bar in Bars:
        Height = Bar.get_height()
        # https://matplotlib.org/api/_as_gen/matplotlib.pyplot.annotate.html#matplotlib.pyplot.annotate
        Axes.annotate('{}'.format(round(Height, 3)),
                      xy=(Bar.get_x()+Bar.get_width()/2, Height),
                      xytext=(0, 3),  # 3 points vertical offset
                      # Offset (in points) from the xy value
                      textcoords="offset points",
                      horizontalalignment='center',
                      verticalalignment='bottom')


AutoLabel(WriteBars)
AutoLabel(ReadBars)
Figure.tight_layout()
pyplot.show()

Database.Cursor.close()
Database.Connection.close()
# END OF FILE