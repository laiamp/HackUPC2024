# python -m pip install holiday-event-api

date = "06/05/2024"
timezone = "America/Chicago"
import holidays

try:
    client = holidays.client('vo9Q7D7KAYmuuF9tiXhga94hUpG20bYQ')
    print("2")

    events = client.getEvents()

except Exception as e:
    print(f"An error has ocurred {e}")