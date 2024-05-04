from datetime import datetime, timedelta
from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    name: str
    age: int
    initial_date: datetime
    final_date: datetime
    city_orig: str
    city_dest: str
    topics: dict[str,int]
    budget:int