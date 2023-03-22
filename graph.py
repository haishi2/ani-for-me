"""copyright and usage info here"""
from __future__ import annotations
import datetime
from typing import Optional

import python_ta

# from anime_and_users import User, Anime


class Review:
    """An edge that connects a user and an anime which contains the ratings the user gave

    Instance Attributes
    - endpoints: The two nodes linked by this review
    - ratings: the ratings that the user gave for the individual categories
    """
    endpoints: tuple[User, Anime]
    ratings: dict[str, int]

    def __init__(self, e1: User, e2: Anime, ratings: dict[str, int]):
        """Add a review and connect the two endpoints
        Preconditions:
            - user and anime both need to exist in the ReccomenderGraph
            - the review needs to not be in the current reviews in the tree
        """
        self.ratings = ratings
        self.endpoints = (e1, e2)
        e1.reviews[e2] = self
        e2.reviews[e1] = self


class ReccomenderGraph:
    """A class for a graph of nodes, where the nodes are users and animes, and edges are reviews

    Instance Attributes
    - users: a list of user nodes
    - animes: a list of anime nodes
    """
    users: dict[str, User]
    animes: dict[int, Anime]

    def __init__(self) -> None:
        """initialize an empty ReccomenderGraph
        Preconditions:
            -
        """
        self.users = {}
        self.animes = {}

    def insert_user(self, user: User) -> User:
        """Add a user into the graph
        Preconditions:
            -
        """
        self.users[user.username] = user
        return user

    def insert_anime(self, anime: Anime) -> Anime:
        """Add an anime into the graph
        Preconditions:
            -
        """
        self.animes[anime.UID] = anime
        return anime

    def add_friends(self, user: str, friend_user: str) -> None:
        """Connect this user and the friend_user together
        Preconditions:
            - both users exist in the graph
        """
        self.users[user].friends_list.append(self.users[friend_user])
        self.users[friend_user].friends_list.append(self.users[user])

    def get_all_path_scores(self, depth: int) -> dict[Anime: float]:
        """Find all anime at a certain depth and calculate a path score for each anime based on
        the reviews given to it and the user's priorities
        Preconditions:
            - depth >= 1
            """
        # take the result from the helper in User and for each path, calculate its path score
        raise NotImplementedError

    # calc_path_scores should take a list of reviews since to calculate the path score we need to average the ratings on each path
    # weighted by the user's preferences
    def calculate_path_score(self, path: list[Review]) -> float:
        """Helper function for get_all_path_scores that calculates the path score for the given path
        Preconditions:
            -
        """
        # remember to average the caluclated path score with the similarity rating for the anime at the endpoint
        raise NotImplementedError


# read files in this order: anime, user, reviews
# remember that the users in csv files dont have friends_list or priorities, so use the (param) = notation when making
# user classes
def read_file(files: list[str]) -> ReccomenderGraph:
    """Creates a ReccomenderGraph given the animes. profiles, and reviews formatted in a CSV file
    Preconditions:
            - files are formatted correctly
            - files[0] is the anime file, files[1] is the user file, files[2] is the reviews file
    """
    graph = ReccomenderGraph()
    with open(files[0], 'r',
              encoding="utf-8") as reader:
        line = reader.readline()

        while line != '':
            lines = line.split(',')
            anime_id = lines[0]
            title = lines[1]
            genres = []
            i = 2
            while all(char.isalpha() for char in lines[i]):
                genres.append(lines[i])
                i += 1

            start_date = datetime.datetime.strptime(lines[i], '%m/%d/%Y')
            end_date = datetime.datetime.strptime(lines[i + 1], '%m/%d/%Y')
            num_episodes = int(lines[i + 2])
            graph.insert_anime(Anime(title, num_episodes, genres, (start_date, end_date), int(anime_id)))
            line = reader.readline()

    with open(files[1], 'r',
              encoding="utf-8") as reader:
        line = reader.readline()

        while line != '':
            lines = line.split(',')
            if lines[0][-1] == '\n':
                username = lines[0][0:len(lines[0]) - 1]
            else:
                username = lines[0]
            favorite_animes = []
            for i in range(1, len(lines)):
                favorite_animes.append(graph.animes[int(lines[i])])
            # if(username == 'Verbin'):
            #     graph.insert_user(User(username=username, favorite_animes=favorite_animes))
            # else:
            print(graph.insert_user(User(username=username, favorite_animes=favorite_animes)).username, username)
            line = reader.readline()

    with open(files[2], 'r',
              encoding="utf-8") as reader:
        line = reader.readline()

        while line != '':
            lines = line.split(',')
            user = graph.users[lines[0]]
            anime = graph.animes[int(lines[1])]
            ratings = {}
            ratings['story'] = int(lines[4])
            ratings['animation'] = int(lines[5])
            ratings['sound'] = int(lines[6])
            ratings['character'] = int(lines[7])
            ratings['overall'] = int(lines[3])
            ratings['enjoyment'] = int(lines[8])
            Review(user, anime, ratings)
            line = reader.readline()
    return graph



def import_profile(file: str, graph: ReccomenderGraph) -> None:
    """loads a user from a csv file and adds them into the graph
    Preconditions:
        - files are formatted correctly
        - user doesn't exist in graph
        - every anime in the user csv file exists in the graph
        - avery user in the friends_list exists
    """
    raise NotImplementedError


# write reviews in as anime name, ratings alternating for every review so can read back in and access the animes by ids
# and create new reviews
def save_profile(user: User, file_name: str) -> None:
    """save the user's profile into a csv file
    Preconditions:
        -
    """


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
    reviews: dict[User, Review]

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
    reviews: dict[Anime, Review]
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
                 reviews: Optional[dict[Anime, Review]] = None, priorities: Optional[dict[str, int]] = None,
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

    def get_all_path_scores_helper(self, depth, visited_nodes: list[Anime | User]) -> list[list[Review]]:
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
        'extra-imports': ['anime_and_users'],  # the names (strs) of imported modules
        'allowed-io': ['import_profile', 'save_profile', 'read_file'],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
