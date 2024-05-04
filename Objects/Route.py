from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import TypeAlias

@dataclass(frozen=True)
class Stop:
    name: str
    coord: tuple[float,float]
    event: bool
    date: datetime
    partner: str


Route: TypeAlias = list[Stop]
    
    