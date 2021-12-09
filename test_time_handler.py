import logging

from time_handler import hhmmss_to_seconds, current_time_seconds


def test_hhmmss_to_seconds():
    assert hhmmss_to_seconds("01:00:00") == 3600
    assert hhmmss_to_seconds("01:00") == 3600  # Function has to be able to convert both hhmm and hhmmss into seconds
    logging.info("Test passed for function: hhmmss_to_seconds")


def test_current_time_seconds():
    assert current_time_seconds()
