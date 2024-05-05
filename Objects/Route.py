from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import TypeAlias

@dataclass(frozen=True)
class Stop:
    name: str
    coords: tuple[float,float]
    event: bool
    date: datetime
    partner: str


Route: TypeAlias = list[Stop]


def create_route(city_list, coord_list):
    Route = []
    for i in range(len(city_list)):
        if i == 2: 
            partner = None
        else:
             partner = "Ramon"
        S = Stop(city_list[i], coord_list[i], False, datetime(2024, 5, 1 + i), partner)
        Route.append(S)
    return Route


    