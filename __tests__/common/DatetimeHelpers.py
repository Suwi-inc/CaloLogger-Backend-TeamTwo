from datetime import datetime


def is_time_between(begin_time, end_time, check_time):
    if begin_time < end_time:
        return begin_time <= check_time <= end_time
    else:  # crosses midnight
        return check_time >= begin_time or check_time <= end_time
