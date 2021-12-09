"""
Module containing all the functions used for fetching news from newsapi-python and handling and filtering dashboards
"""

import json
import logging
import sched
import time

from newsapi import NewsApiClient

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

newsapi = NewsApiClient(api_key=config["api_key"])
s = sched.scheduler(time.time, time.sleep)


def news_API_request(covid_terms="Covid COVID-19 coronavirus"):
    """
    Fetches specific news from newsapi-python then filtering it to return only the titles and content. Also fetches
    news based on relevancy.

    Args:
        covid_terms (str): Defaults to "Covid COVID-19 coronavirus", searches for specific news based on terms

    Returns:
        news (list[dict[str, any]]): News articles
    """
    news = []
    r = newsapi.get_everything(
        q=covid_terms,
        sort_by=config["sort_by"]
    ).get("articles")
    for x in r:
        x = {
            "title": x["title"],
            "content": x["description"]
        }
        news.append(x)
    logging.info("News fetched from newsapi")
    return news


def filtering_news(news: list, filtered_news: list):
    """
    Filters news to remove unwanted removed articles

    Args:
        news (list): List of articles to remove from
        filtered_news (list): List of titles to filter the unwanted news with

    Returns:
        news (list): List of articles with undesired articles removed
    """
    for x in filtered_news:
        for y in news:  # Nested loop to loop through the titles since it is a list of dictionaries
            if y["title"] == x["title"]:
                news.remove(y)
                logging.info("News filtered, removed {}".format(x["title"]))
                break
    return news


def news_data_update(file_name: str, file_data: list):
    """
    Updates news dashboard in the form of a json file

    Args:
        file_name (str): Name of file to overwrite to
        file_data (list): Data to write over the file with

    Return:
        None
    """
    with open(file_name, 'w', encoding='utf-8') as f:  # Opens json file as "f" with writing permissions.
        # Code only works with encoding='utf-8'.
        json.dump(file_data, f, ensure_ascii=False, indent=4)
    logging.info("News data files updated")


def schedule_news_updates(update_interval, update_name):
    """
   Schedule Covid Updates with covid_data_update():

    Args:
        update_interval (int): Delay of when to update
        update_name (str): Name of the scheduled update which is returned

    Returns:
        None
    """
    update_event = update_name.enter(update_interval, 1, news_data_update, ("news_dashboard.json", news_API_request()))
    logging.info("Covid data update scheduled for the next: {} Seconds".format(update_interval))
