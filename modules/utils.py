import os
import datetime


class VideoDateTime:

    def __init__(self, starting_datetime, ending_datetime):
        self.starting_datetime = starting_datetime
        self.ending_datetime = ending_datetime

    def __str__(self):
        return ("Start: " + str(self.starting_datetime)) + "\n" + ("End:   " + str(self.ending_datetime))


def parse_datetime(video_path):
    """
    Parse date and time from video naming
    :param video_path:
    :return:
    """
    try:
        filename = os.path.basename(video_path)

        yearmonthday = filename.split("_")[2]

        year = 2000 + int(yearmonthday[:2])
        month = int(yearmonthday[2:4])
        day = int(yearmonthday[4:6])

        start_hourminutesecond = filename.split("_")[3]
        start_hour = int(start_hourminutesecond[:2])
        start_minute = int(start_hourminutesecond[2:4])
        start_second = int(start_hourminutesecond[4:6])

        start_datetime = datetime.datetime(year, month, day, start_hour, start_minute, start_second)

        ending_hourminutesecond = filename.split("_")[4]
        ending_hour = int(ending_hourminutesecond[:2])
        ending_minute = int(ending_hourminutesecond[2:4])
        ending_second = int(ending_hourminutesecond[4:6])

        ending_datetime = datetime.datetime(year, month, day, ending_hour, ending_minute, ending_second)

        video_datetime = VideoDateTime(start_datetime, ending_datetime)
    except:
        return None

    return video_datetime




if __name__ == "__main__":
    datetime = parse_datetime("C:\\Education\\untitled\\videos\\14_04_171019_081736_082929_0129986476.avi")
    print(datetime)