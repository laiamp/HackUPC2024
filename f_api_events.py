# python -m pip install holiday-event-api

import holidays
import sys
date = "06/05/2024"
timezone = "Madrid/Europe"
api_key = 'YFAuf4V91WCV37YHqNXSZzsATzlEfOOI'


if __name__ == "__main__":

    if (len(sys.argv) != 2):
        raise Exception("Lacking city name")
    else:
        timezone = sys.argv[1] + "/Europe"

    try:
        client = holidays.client(api_key)
        events = client.getEvents()


    except Exception as e:
        print(f"An error has ocurred {e}")





