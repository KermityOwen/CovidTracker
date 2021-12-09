# CovidTrackerUK

CovidTrackerUK is a Python project used to track current national and local cases in the UK


## Installation

Download the sourcecode from my GitHub github/KermityOwen/CovidTracker


## Usage

There are docstring documentation on every function with structured commenting to explain how each one works.
covid_data_handler.py includes all the functions used for fetching, processing and saving live covid data to and from
 CSV files.
covid_news_handling.py includes all the functions used for getting relevant news articles from newsapi-python, it is
 also used for filtering and saving said news articles into json files as a list of dictionaries with only the title
 and article content preview
time_handler.py includes all the functions needed to fetch current time and exchange time formats from hhmm or hhmmss
 to seconds. Made primarily for the example in main.py
template/index.html is a template html created by Professor Matt Collison from the University of Exeter. Used for the
 example in main.

## Contributing
Pull requests are welcome. For any changes, major or small, just do it.
When making major changes, you should also edit and modify the tests to suit its new purpose.


## License
[MIT](https://choosealicense.com/licenses/mit/)
