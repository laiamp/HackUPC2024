# python -m pip install holiday-event-api

import holidays
date = "06/05/2024"
timezone = "Madrid/Europe"

try:
    client = holidays.client('YFAuf4V91WCV37YHqNXSZzsATzlEfOOI')
    events = client.getEvents()

    print (f"Found {len(events.events)} events, including {events.events[0].name}\n")


except Exception as e:
    print(f"An error has ocurred {e}")