import json
import logging
import sched
import time

from covid_news_handling import news_API_request, news_data_update, schedule_news_updates

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)


def test_news_API_request():
    test = news_API_request()
    assert isinstance(test, list)
    assert isinstance(test[1], dict)  # news_API_request must return a list of dictionaries
    logging.info("Test passed for function: news_API_request")


def test_news_data_update():
    news_data_update(config["news_dashboard_file"], news_API_request())
    assert config["news_dashboard_file"]
    logging.info("Test passed for function: covid_data_update")


def test_schedule_news_updates():
    s_test = sched.scheduler(time.time, time.sleep)
    schedule_news_updates(10, s_test)
    assert s_test.queue  # Checks declared scheduler for a scheduled event
    logging.info("Test passed for function: schedule_covid_update")
