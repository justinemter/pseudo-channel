import pytest
import datetime

@pytest.mark.parametrize("commercial, expected", [
    (["1", "1501900754", "3", "001 - Kit_Kat_Commercial_-_Give_Me_A_Break_1988", "30890", "/library/metadata/3854"], 35890)
])
def test_pad_the_commercial_dur(commercial, expected):

    commercial_as_list = list(commercial)

    commercial_as_list[4] = int(commercial_as_list[4]) + (5 * 1000)

    assert int(commercial_as_list[4]) == expected

def test_inject_commercials():

    pass