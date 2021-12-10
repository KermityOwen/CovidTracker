"""
Module containing all the functions used to handle and fetch live covid data from the uk-covid19 api
"""
import sched
import logging
import json
import time

from uk_covid19 import Cov19API

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
s_covid = sched.scheduler(time.time, time.sleep)


def parse_csv_data(data):
    """
    Parses CSV Data into a List of Strings.

    Args:
        data (string): name of the csv file

    Returns:
        line_data (list[str]): list of lines from csv files
    """
    f1 = open(data)  # Opens file as "f"
    line_data = []  # Declaring temporary empty list
    for x in f1.readlines():  # Loops through file's lines
        line_data.append(x)  # Appends lines to the list as a string
    return line_data  # Return


def process_covid_csv_data(parsed_data, national_scale=True):
    """
    Process Parsed Covid Data and Returns a Group of Variables

    Args:
        parsed_data: Parsed CSV Data
        national_scale (bool): Defaults to True. True for national, false for ltla

    Returns:
        single_weekly, current_hospital[1], total_death[1], location (int, str, str, str): Information about Covid Cases
    """
    daily_cases, current_hospital, total_death, single_weekly, location = [], [], [], 0, ""  # Declaring variables
    for x in range(len(parsed_data)):
        line_split = parsed_data[x].split(",")  # Split every string into a list
        # \/ Saving data into the variables declared earlier
        location = line_split[1]
        if line_split[4] != "":
            total_death.append(line_split[4])
        current_hospital.append(line_split[5])
        daily_cases.append(line_split[6])
    for i in range(0, 7):  # Looping through the last 7 days of daily cases into one weekly case variable
        single_weekly += int(str(daily_cases[i + 2]).strip())  # [i+2] to ignore first incomplete data entry
    # \/ returns values based on it argument of whether or not it's national or local scale
    if national_scale:
        logging.info("National CSV data processed")
        return single_weekly, current_hospital[1], total_death[1], location
    else:
        logging.info("Local CSV data processed")
        return single_weekly, location


def covid_API_request(location: str = "England", location_type: str = "nation"):
    """
    Fetch Covid Data from the UK-Covid API

    Args:
        location (str): location of tracking (Eg. "Exeter", "England")
        location_type (str): location type of tracking (Eg. "ltla", "nation")

    Returns:
        data (str): data of covid cases in csv format
    """
    # \/ declaring location ranges and the filter for what to fetch
    location_thingy = [
        'areaType=' + location_type,
        'areaName=' + location
    ]
    reformatted_stuff = {
        "areaCode": "areaCode",
        "areaName": "areaName",
        "areaType": "areaType",
        "date": "date",
        "cumDailyNsoDeathsByDeathDate": "cumDailyNsoDeathsByDeathDate",  # heh cum
        "hospitalCases": "hospitalCases",
        "newCasesBySpecimenDate": "newCasesBySpecimenDate"
    }
    api = Cov19API(filters=location_thingy, structure=reformatted_stuff)  # Declare api
    data = api.get_csv()  # Fetch data into csv format
    return data


def covid_data_update(local_file_name=config["local_covid_file"], national_file_name=config["national_covid_file"]):
    """
    Update CSV File to Most Recent Covid Data

    Args:
        local_file_name (str): Defaults to "local_covid_data", File name of local covid data to be updated.
        national_file_name (str): Defaults to "national_covid_data", File name of national covid data to be updated.

    Returns:
        None
    """
    f1, f2 = open(local_file_name, "w"), open(national_file_name, "w")  # Opens files as "f" and "f2"
    f1.write(covid_API_request(config["local_location"], "ltla"))  # Writes fetched data from API to files
    f2.write(covid_API_request(config["national_location"], "nation"))
    f1.close()  # Closes the files
    f2.close()
    logging.info("Covid data files updated.")


def schedule_covid_updates(update_interval: int, update_name: sched.scheduler, repeat=False):
    """
    Schedule Covid Updates with covid_data_update():

    Args:
        update_interval (int): Delay of when to update
        update_name (scheduler): Name of the update event to be cancelled if needed
        repeat (bool): Defaults to false, Whether or not the update event is repeated every 24hours

    Returns:
        None
    """
    update_name = s_covid.enter(update_interval, 1, covid_data_update, ())  # Enter update as a scheduled event
    if repeat:
        update_name = s_covid.enter(86400, 1, schedule_covid_updates(update_interval, update_name, True))
    logging.info("Covid data update scheduled for the next: {} Seconds".format(update_interval))
