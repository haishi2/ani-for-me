"""copyright and usage info here"""
from __future__ import annotations
import datetime
from typing import Optional

import python_ta

import graph as g


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
    reviews: dict[User, g.Review]

    def __init__(self, title: str, num_episodes: int, genres: list[str],
                 air_dates: tuple[datetime.date, datetime.date], UID: int):
        """Initialize a new anime"""
        self.title = title
        self.num_episodes = num_episodes
        self.genres = genres
        self.air_dates = air_dates
        self.UID = UID
        self.reviews = {}


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
        - (length of prioities must be 7)
    """
    username: str
    reviews: dict[Anime, g.Review]
    favorite_animes: list[Anime]
    matching_genres: list[str]
    friends_list: list[User]
    # priorities contains most of the categories of a review ('Story', 'Animation', 'Sound', 'Character') and an
    # average of the amount of episodes from the user's favorite anime to get their preferred amount of episodes
    priorities: dict[str, int]
    weights: dict[str, float]
    favorite_era: tuple[datetime.date, datetime.date]

    # reviews, priorities, and friends_list are optional since they could be loaded in from a users csv file, the regular
    # database users don't have these properties
    # TODO   given priority in this function only has the categories, not the avgd number of episodes
    def __init__(self, username: str, favorite_animes: list[Anime],
                 favorite_era: Optional[tuple[datetime.date, datetime.date]] = None,
                 reviews: Optional[dict[Anime, g.Review]] = None, priorities: Optional[dict[str, int]] = None,
                 friends_list: Optional[list[User]] = None) -> None:
        """intialize a new user and calculate their priority weights
        Preconditions:
            -
        """
        self.username = username
        self.favorite_animes = favorite_animes
        if friends_list is None:
            self.friends_list = []
        else:
            self.friends_list = friends_list
        if favorite_era is None:
            self.favorite_era = tuple()
        self.favorite_era = favorite_era
        if reviews is None:
            self.reviews = {}
        else:
            self.reviews = reviews
        if priorities is None:
            self.priorities = {}
            matching_genres = []
            weights = {}
        else:
            self.priorities = priorities
            self.calculate_genre_match_and_calculate_avg()
            self.calculate_priority_weights()

    def get_all_path_scores_helper(self, depth, visited_nodes: list[Anime | User]) -> list[list[g.Review]]:
        """Helper function for get_all_path_scores that calculates all the paths
        Preconditions:
            - depth >= 1
        """
        raise NotImplementedError

    def calculate_genre_match_and_calculate_avg(self) -> None:
        """Calculate the genres in at least 50% of the anime across the user's favorite anime and reviews
        Preconditions:
            - favorite anime isn't empty or reviews isnt empty
        """
        num_animes = len(self.favorite_animes) + len(self.reviews)
        genres_count = {}
        episodes_count = 0
        for anime in self.favorite_animes:
            episodes_count += anime.num_episodes
            for genre in anime.genres:
                if genre not in genres_count.keys():
                    genres_count[genre] = 1
                else:
                    genres_count[genre] += 1

        for anime in self.reviews:
            episodes_count += anime.num_episodes
            for genre in anime.genres:
                if genre not in genres_count.keys():
                    genres_count[genre] = 1
                else:
                    genres_count[genre] += 1

        self.matching_genres = [genre for genre in genres_count if genres_count[genre] >= (num_animes / 2)]
        self.priorities['num_episodes'] = int(episodes_count / num_animes)

    def calculate_priority_weights(self) -> None:
        """Calculate the priority weights for each category in priority except for num_episodes
        Preconditions:
            -
        """
        # this should sum up to 100% because its taking parts out of the sum for each as their percentage share weight
        total = sum(self.priorities.values()) - self.priorities['num_episodes']
        for priority in self.priorities:
            if priority != 'num-episodes':
                self.weights[priority] = self.priorities[priority] / total

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
        # this is going to be done solely by the similarity rating
        raise NotImplementedError


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
    python_ta.check_all(config={
        'extra-imports': ['graph', 'typing'],  # the names (strs) of imported modules
        'allowed-io': ['import_profile', 'save_profile'],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
