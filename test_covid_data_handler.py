import json
import logging
import sched
import time

from covid_data_handler import parse_csv_data, process_covid_csv_data, covid_API_request, schedule_covid_updates, \
    covid_data_update

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)


def test_parse_csv_data():
    parse_test = parse_csv_data(config["national_covid_file"])
    assert isinstance(parse_test, list)
    assert isinstance(parse_test[5], str)  # Parsed CSV data has to be a list of strings
    logging.info("Test passed for function: parse_csv_data")


def test_process_csv_data():
    loc_l7d, loc_l = process_covid_csv_data(parse_csv_data(config["local_covid_file"]), False)
    nat_l7d, hosp_cases, t_deaths, nat_l = process_covid_csv_data(parse_csv_data(config["national_covid_file"]), True)
    assert loc_l7d and loc_l  # Processing CSV data for a local scale has to return its 2 variables
    assert nat_l7d and hosp_cases and t_deaths and nat_l  # Processing CSV data for a national scale has to return
    # its 4 variables
    logging.info("Test passed for function: process_csv_data")


def test_covid_API_request():
    data = covid_API_request()
    assert isinstance(data, str)  # Requested data from UK-covid19 is in csv format and must be returned as a string
    logging.info("Test passed for function: covid_API_request")


def test_covid_data_update():
    covid_data_update()
    assert config["local_covid_file"]
    assert config["national_covid_file"]
    logging.info("Test passed for function: covid_data_update")


def test_schedule_covid_updates():
    s_test = sched.scheduler(time.time, time.sleep)
    schedule_covid_updates(10, s_test)
    assert s_test.queue  # Checks declared scheduler for a scheduled event
    logging.info("Test passed for function: schedule_covid_update")
