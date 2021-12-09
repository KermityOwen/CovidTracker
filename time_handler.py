"""
Module contains functions for handling time format conversions and fetching current time in GMT UTC+0.
"""
import logging
import time


def hhmmss_to_seconds(hhmmss):
    """
    Translates HHMMSS or HHMM formatted time into seconds.

    Args:
        hhmmss (str): String in HHMMSS or HHMM format

    Returns:
        seconds (int): Converted seconds
    """
    hhmmss_split = hhmmss.split(":")
    try:
        seconds = (int(hhmmss_split[0]) * 60 * 60) + (int(hhmmss_split[1]) * 60) + int(hhmmss_split[2])
    except IndexError:  # If IndexError then it would be HHMM instead of HHMMSS so run below code \/
        seconds = (int(hhmmss_split[0]) * 60 * 60) + (int(hhmmss_split[1]) * 60)
    return seconds


def current_time_hhmmss():
    """
    Fetches current time in GMT UTC+0

    Returns:
        (str): Current time in GMT UTC+0
    """
    return str(time.gmtime().tm_hour) + ":" + str(time.gmtime().tm_min) + ":" + str(time.gmtime().tm_sec)


def current_time_seconds():
    """
    Fetches current time in seconds

    Returns:
        (int): Current time in seconds
    """
    logging.info("Current time fetched")
    return hhmmss_to_seconds(current_time_hhmmss())
