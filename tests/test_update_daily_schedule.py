import pytest
import datetime

@pytest.mark.parametrize("prevstartime, prevendtime, nowtime, expected", [
    ("04:55:00 PM", "1900-01-01 17:23:42.304000", "1900-01-01 17:10:42.304000", True),
    ("04:55:00 PM", "1900-01-01 17:23:42.304000", "1900-01-01 16:56:42.304000", True),
    ("04:55:00 PM", "1900-01-01 17:23:42.304000", "1900-01-01 16:59:42.304000", True),
    ("04:55:00 PM", "1900-01-01 17:23:42.304000", "1900-01-01 17:02:42.304000", True),
    ("04:55:00 PM", "1900-01-01 17:23:42.304000", "1900-01-01 17:15:42.304000", True),
    ("04:55:00 PM", "1900-01-01 17:23:42.304000", "1900-01-01 17:23:43.304000", False),
    ("04:55:00 PM", "1900-01-01 17:23:42.304000", "1900-01-01 17:25:00.304000", False),
])
def test_prev_day_media_still_playing_on_update(prevendtime, prevstartime, nowtime, expected):

    prev_end_time_to_watch_for = None

    now = datetime.datetime.strptime(nowtime, '%Y-%m-%d %H:%M:%S.%f')
    
    prev_start_time = datetime.datetime.strptime(prevstartime, "%I:%M:%S %p")

    prev_end_time_format = '%Y-%m-%d %H:%M:%S.%f' if '.' in prevendtime else '%Y-%m-%d %H:%M:%S'

    prev_end_time = datetime.datetime.strptime(prevendtime, prev_end_time_format)

    assert (prev_start_time < now and prev_end_time > now) == expected