from dataclasses import dataclass
from datetime import datetime


@dataclass
class Anime:
    title: str
    # num_episodes: int
    # genres: list[str]
    # air_dates: tuple[datetime.date, datetime.date]
    # uid: int
    ratings: dict[str: int]
