"""copyright and usage info here"""
import datetime
from typing import Optional

import python_ta

from graph import ReccomenderGraph, Review

class Anime:
    """A class representing a anime node in the ReccomenderTree

    Instance Attributes
    - title: the title of the anime
    - num_episodes: the number of episodes the anime has
    - genres: the genres of the anime
    - air_dates: the dates that the anime aired between
    - UID: the unique identifier for the anime
    - reviews: the reviews for this anime
    Representation Invariants:
        - (air_dates[1] - air_dates[0]).days > 0
    """
    title: str
    num_episodes: int
    genres: list[str]
    air_dates: tuple[datetime.date, datetime.date]
    UID: int
    reviews: list[Review]

    def __init__(self, title: str, num_episodes: int, genres: list[str],
                 air_dates: tuple[datetime.date, datetime.date], UID: int):
        """Initialize a new anime"""

class User:
    """A class representing a user node in the ReccomenderTree
    Instance Attributes:
    - Username: the user's username
    - reviews: the reviews that the User has made
    - favorite_animes: the UIDS of the user's favorite animes
    - friends_list: the uid of the user's friends
    - priorities: how much the user values each aspect of an anime
    - weights: the weights of each priority
    - favorite_era: the user's favorite era of anime
    Representation Invariants:
        - all(0 <= priorities[priority] <= 10 for priority in priorities)
        - len(priorities) == 5
    """
    username: str
    reviews: list[Review]
    favorite_animes: list[int]
    matching_genres: list[str]
    friends_list: list[int]
    #priorities contains most of the categories of a review ('Story', 'Animation', 'Sound', 'Character') and an
    # average of the amount of episodes from the user's favorite anime to get their preferred amount of episodes
    priorities: dict[str, int]
    weights: dict[str, float]
    favorite_era: tuple[datetime.date, datetime.date]
    #reviews are optional since they could be loaded in from a users csv file
    def __init__(self, username: str, favorite_animes: list[int],friends_list: list[int],
                 priorities: dict[str, int], favorite_era: tuple[datetime.date, datetime.date],
                 reviews: Optional[list[Review]] = None) -> None:
        """intialize a new user and calculate their priority weights
        Preconditions:
            -
        """
        raise NotImplementedError

    #visited_nodes should be list[Anime | User] or list[Review]
    def get_all_path_scores_helper(self, depth, visited_nodes: list) -> list[list[Review]]:
        """Helper function for get_all_path_scores that calculates all the paths
        Preconditions:
            - depth >= 1
        """
        raise NotImplementedError

    def calculate_genre_match(self) -> None:
        """Calculate the shared genres across the user's favorite anime and reviews
        Preconditions:
            -
        """
        raise NotImplementedError

    def calculate_priority_weights(self) -> None:
        """calculate the priority weights for each category in priority except for num_episodes"""
        raise NotImplementedError

    def add_friends(self, friend_user: str) -> None:
        """Connect this user and the friend_user together
        Preconditions:
            -
        """
        raise NotImplementedError

    def calculate_similarity_rating(self, anime) -> float:
        """Calculate a similarity rating between 1 and 10 to give a prediction for how much the user will like the anime
        Preconditions:
            -
        """
        raise NotImplementedError

    def reccomend_based_on_friends(self) -> dict[Anime: float]:
        """Reccomend anime based on what the user's friends have watched
        Preconditions:
            -
        """
        #this is going to be done solely by the similarity rating
        raise NotImplementedError


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
    python_ta.check_all(config={
        'extra-imports': ['graph', 'typing'],  # the names (strs) of imported modules
        'allowed-io': ['import_profile', 'save_profile'],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
