"""
Main runs everything and renders html template
"""
import json
import sched
import time
import logging

from flask import render_template, Flask, request, redirect
from covid_data_handler import parse_csv_data, process_covid_csv_data, schedule_covid_updates
from covid_news_handling import schedule_news_updates, news_data_update, filtering_news
from time_handler import hhmmss_to_seconds, current_time_seconds

# Opening, reading and defining config file
with open('config.json', 'r', encoding='utf-8') as f:  # Encoding because of newsapi key
    config = json.load(f)

logging.basicConfig(filename=config["log_file"], level=logging.INFO, format="%(asctime)s : %(levelname)s : "
                                                                            "%(filename)s : %(message)s")
s = sched.scheduler(time.time, time.sleep)

# Processing covid csv data and declaring it into variable to be called
loc_last7days_cases, loc_location = process_covid_csv_data(parse_csv_data(config["local_covid_file"]), False)
nat_last7days_cases, current_hospital_cases, total_deaths, nat_location = process_covid_csv_data(
    parse_csv_data(config["national_covid_file"]), True)

# Cached data that resets on program restart
filtered_terms = []  # List of removed articles for filter
updatedash = []  # List for update dashboard UI

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route('/index')
def index():
    s.run(blocking=False)
    text_field = request.args.get("two")
    update_time = request.args.get("update")
    filter_text = request.args.get("notif")

    with open(config["news_dashboard_file"], 'r', encoding='utf-8') as json_news:
        newsdash = json.load(json_news)

    if update_time == "":
        return redirect(request.path)

    if text_field:
        time_interval = hhmmss_to_seconds(update_time) - current_time_seconds()
        if request.args.get("news"):
            schedule_news_updates(time_interval, s)
            updatedash.append({
                'title': text_field,
                'content': config["news_up_text"] + str(update_time)
            })
            logging.info("User entered scheduled update for news dashboard with text field '{}'".format(text_field))
            # Kinda bad code, makes sure it doesn't prematurely redirect into /index so if both boxes are ticked it
            # would run below code before returning
            if request.args.get("covid-data") is None:
                return redirect(request.path)
        if request.args.get("covid-data"):
            schedule_covid_updates(time_interval, s)
            updatedash.append({
                'title': text_field,
                'content': config["covid_up_text"] + str(update_time)
            })
            logging.info("User entered scheduled update for covid data with text field '{}'".format(text_field))
            return redirect(request.path)

    if filter_text:
        filtered_terms.append({"title": filter_text})
        news_data_update(config["news_dashboard_file"], filtering_news(newsdash, filtered_terms))
        return redirect(request.path)

    return render_template(config["template"], title="ECM1400 Test",
                           image="masks.png",
                           location=loc_location,
                           local_7day_infections=loc_last7days_cases,
                           nation_location=nat_location,
                           national_7day_infections=nat_last7days_cases,
                           hospital_cases=config["hospital_case_text"] + current_hospital_cases,
                           deaths_total=config["death_case_text"] + total_deaths,
                           news_articles=newsdash,
                           updates=updatedash)


if __name__ == "__main__":
    app.run()
