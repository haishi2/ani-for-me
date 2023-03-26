"""copyright and usage info here"""
from __future__ import annotations
import datetime
import re
from typing import Optional

import python_ta

import graph as g


# IMPORTANT: the parameter for the number of episodes in user.priorities should be written as 'num-episodes'
# TODO see which instance attributes should be made private, add preconditions

class Anime:
    """A class representing a anime node in the ReccomenderTree

    Private Instance Attributes
    - title: the title of the anime
    - num_episodes: the number of episodes the anime has
    - genres: the genres of the anime
    - air_dates: the dates that the anime aired between
    - UID: the unique identifier for the anime
    - tags: the search tags for this anime
    Instance Attributes
    - reviews: the reviews for this anime
    Representation Invariants:
        - (air_dates[1] - air_dates[0]).days > 0
    """
    _title: str
    _num_episodes: int
    _genres: set[str]
    _air_dates: tuple[datetime.date, datetime.date]
    _UID: int
    reviews: dict[User, g.Review]
    _tags: set[str]

    def __init__(self, title: str, num_episodes: int, genres: set[str],
                 air_dates: tuple[datetime.date, datetime.date], uid: int):
        """Initialize a new anime"""
        self._title = title
        self._num_episodes = num_episodes
        self._genres = genres
        self._air_dates = air_dates
        self._UID = uid
        self.reviews = {}
        self._tags = g.tag_keywords_and_strip(self._title)

    def get_num_episodes(self) -> int:
        return self._num_episodes

    def get_genres(self) -> set[str]:
        return self._genres

    def get_uid(self) -> int:
        return self._UID

    def get_title(self) -> str:
        return self._title

    def get_air_dates(self) -> tuple[datetime.date, datetime.date]:
        return self._air_dates

    def get_tags(self)-> set[str]:
        return self._tags

    def calculate_average_ratings(self) -> dict[str, float]:
        """Calculate the average ratings for this anime over all of its reviews.
        Preconditions:
            -
        """
        if self.reviews == {}:
            return {'story': 0, 'animation': 0, 'sound': 0, 'character': 0, 'enjoyment': 0, 'overall': 0}
        ratings_dict = {'story': 0, 'animation': 0, 'sound': 0, 'character': 0, 'enjoyment': 0, 'overall': 0}
        for review in self.reviews:
            for key in self.reviews[review].ratings:
                ratings_dict[key] += self.reviews[review].ratings[key]

        return {section: round(ratings_dict[section] / len(self.reviews), 2) for section in ratings_dict}


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
    favorite_animes: set[Anime]
    matching_genres: set[str]
    friends_list: list[User]
    # priorities contains all of the categories of a review ('story', 'animation', 'sound', 'character', 'enjoyment', 'overall') and an
    # average of the amount of episodes from the user's favorite anime to get their preferred amount of episodes
    #TODO IMPORTANT: the keys should be ('story', 'animation', 'sound', 'character', 'enjoyment', 'overall', 'num-episodes)
    priorities: dict[str, int]
    weights: dict[str, float]
    favorite_era: tuple[datetime.date, datetime.date]

    # reviews, priorities, and friends_list are optional since they could be loaded in from a users csv file, the regular
    # database users don't have these properties
    # TODO IMPORTANT: the keys should be ('story', 'animation', 'sound', 'character', 'enjoyment', 'overall', 'num-episodes)
    def __init__(self, username: str, favorite_animes: set[Anime],
                 favorite_era: Optional[tuple[datetime.date, datetime.date]] = None,
                 reviews: Optional[dict[Anime, g.Review]] = None, priorities: Optional[dict[str, int]] = None,
                 friends_list: Optional[list[User]] = None) -> None:
        """intialize a new user and calculate their priority weights
        Preconditions:
            - favorite era[0] < favorite_era[1]
        """
        self.username = username
        self.favorite_animes = favorite_animes
        if friends_list is None:
            self.friends_list = []
        else:
            self.friends_list = friends_list
        if favorite_era is None:
            self.favorite_era = tuple()
        else:
            self.favorite_era = favorite_era
        if reviews is None:
            self.reviews = {}
        else:
            self.reviews = reviews
        if priorities is None:
            self.priorities = {}
            self.matching_genres = set()
            self.weights = {}
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
            - favorite anime isn't empty or reviews isn't empty
        """
        num_animes = len(self.favorite_animes.union({anime for anime in self.reviews}))
        genres_count = {}
        episodes_count = 0
        visited_anime = []
        for anime in self.favorite_animes:
            episodes_count += anime.get_num_episodes()
            visited_anime.append(anime)
            for genre in anime.get_genres():
                if genre not in genres_count.keys():
                    genres_count[genre] = 1
                else:
                    genres_count[genre] += 1

        for anime in self.reviews:
            if anime not in visited_anime:
                episodes_count += anime.get_num_episodes()
                for genre in anime.get_genres():
                    if genre not in genres_count.keys():
                        genres_count[genre] = 1
                    else:
                        genres_count[genre] += 1

        # stripping the spaces from the genre so comparisons are possible
        self.matching_genres = {re.sub('[^a-zA-Z]+', '', genre) for genre in genres_count if
                                genres_count[genre] >= int(num_animes / 2)}
        self.priorities['num-episodes'] = int(episodes_count / num_animes)

    def calculate_priority_weights(self) -> None:
        """Calculate the priority weights for each category in priority except for num_episodes
        Preconditions:
            -
        """
        # this should sum up to 100% because its taking parts out of the sum for each as their percentage share weight
        total = sum(self.priorities.values()) - self.priorities['num-episodes']
        for priority in self.priorities:
            if priority not in ('num-episodes', 'overall', 'enjoyment'):
                self.weights[priority] = self.priorities[priority] / total

    def calculate_similarity_rating(self, anime) -> float:
        """Calculate a similarity rating between 1 and 10 to give a prediction for how much the user will like the anime
        Preconditions:
            -
        """
        anime_avg_ratings = anime.calculate_average_ratings()
        weighted_avg = sum([self.weights[key] * anime_avg_ratings[key] for key in self.priorities if
                            key not in ('num-episodes', 'overall', 'enjoyment')]) / 10

        overlap_start_date = max(self.favorite_era[0], anime.get_air_dates[0])
        overlap_end_date = min(self.favorite_era[1], anime.get_air_dates[1])
        date_overlap_delta = (overlap_end_date - overlap_start_date).days + 1
        user_era_length = (self.favorite_era[1] - self.favorite_era[0]).days + 1
        date_score = round(date_overlap_delta / user_era_length, 2)

        shared_members = len(self.matching_genres.intersection(anime.get_genres()))
        total_members = len(self.matching_genres.union(anime.get_genres()))
        genre_match_index = round(shared_members / total_members, 2)

        episode_rating = round(self.calculate_epsisode_rating(anime), 2)

        return round((0.5 * weighted_avg + 0.3 * genre_match_index + 0.1 * episode_rating + 0.1 * date_score), 2) * 10

    def calculate_epsisode_rating(self, anime) -> float:
        """Calulcates a normalized score for the number of standard deviations an anime is away from the
        users avereage length.
        """
        stddev = 39.64
        mid = self.priorities['num-episodes']
        # NOTE: the numbers 1 and 773 come from the minimum and maximum of the episode counts (excluding outliers)
        # and the standard deviation was calulated with the outliers removed
        # outliers were animes with id [6277, 23349, 2471, 32448, 22221, 12393, 8213, 10241]
        max_std_deviations_l = (mid - 1) / stddev
        max_std_deviations_r = (773 - mid) / stddev

        if anime.get_num_episodes() < mid:
            deviations_distance = (mid - anime.num_epsiodes) / stddev
            return 1 - (deviations_distance / max_std_deviations_l)
        else:
            deviations_distance = (anime.get_num_episodes() - mid) / stddev
            return 1 - (deviations_distance / max_std_deviations_r)

    def reccomend_based_on_friends(self) -> dict[Anime: float]:
        """Reccomend anime based on what the user's friends have watched
        Preconditions:
            -
        """
        # this is going to be done solely by the similarity rating
        already_watched = self.favorite_animes.union(self.reviews.keys())
        animes_to_rank = set()
        scores = {}
        for friend in self.friends_list:
            friend_watched = friend.favorite_animes.union(friend.reviews.keys())
            animes_to_rank = animes_to_rank.union(friend_watched.difference(already_watched))

        for anime in animes_to_rank:
            scores[anime] = self.calculate_similarity_rating(anime)

        return scores


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
    python_ta.check_all(config={
        'extra-imports': ['graph', 'typing'],  # the names (strs) of imported modules
        'allowed-io': ['import_profile', 'save_profile'],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
