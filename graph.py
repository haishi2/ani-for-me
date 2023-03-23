"""copyright and usage info here"""
from __future__ import annotations
import datetime

import python_ta

import anime_and_users as aau


class Review:
    """An edge that connects a user and an anime which contains the ratings the user gave

    Instance Attributes
    - endpoints: The two nodes linked by this review
    - ratings: the ratings that the user gave for the individual categories
    """
    endpoints: tuple[aau.User, aau.Anime]
    ratings: dict[str, int]

    def __init__(self, e1: aau.User, e2: aau.Anime, ratings: dict[str, int]):
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
    users: dict[str, aau.User]
    animes: dict[int, aau.Anime]

    def __init__(self) -> None:
        """initialize an empty ReccomenderGraph
        Preconditions:
            -
        """
        self.users = {}
        self.animes = {}

    def insert_user(self, user: aau.User) -> aau.User:
        """Add a user into the graph
        Preconditions:
            -
        """
        self.users[user.username] = user
        return user

    def insert_anime(self, anime: aau.Anime) -> aau.Anime:
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

    def get_all_path_scores(self, depth: int) -> dict[aau.Anime: float]:
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
# files: ['csc111_project_formatted_files_and_code/data/formatted_and_duplicates_removed/anime_formatted_no_duplicates.csv', 'csc111_project_formatted_files_and_code/data/formatted_and_duplicates_removed/profiles_formatted_no_duplicates.csv', 'csc111_project_formatted_files_and_code/data/formatted_and_duplicates_removed/reviews_formatted_no_duplicates.csv']
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
            graph.insert_anime(aau.Anime(title, num_episodes, genres, (start_date, end_date), int(anime_id)))
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

            # print(graph.insert_user(User(username=username, favorite_animes=favorite_animes)).username, username)
            graph.insert_user(aau.User(username=username, favorite_animes=favorite_animes))
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
def save_profile(user: aau.User, file_name: str) -> None:
    """save the user's profile into a csv file
    Preconditions:
        -
    """


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
    python_ta.check_all(config={
        'extra-imports': ['anime_and_users'],  # the names (strs) of imported modules
        'allowed-io': ['import_profile', 'save_profile', 'read_file'],
        # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
    # TODO remove this before submission

    # a = read_file(['csc111_project_formatted_files_and_code/data/formatted_and_duplicates_removed/anime_formatted_no_duplicates.csv', 'csc111_project_formatted_files_and_code/data/formatted_and_duplicates_removed/profiles_formatted_no_duplicates.csv', 'csc111_project_formatted_files_and_code/data/formatted_and_duplicates_removed/reviews_formatted_no_duplicates.csv'])
    # with open(
    #         f"csc111_project_formatted_files_and_code/data/formatted_and_duplicates_removed/profiles_formatted_no_duplicates.csv",
    #         "r", newline='', encoding="utf-8") as reader:
    #     line = reader.readline()
    #     while line != '':
    #         lines = line.split(',')
    #         if lines[0][-1] == '\n' or lines[0][-1] == '':
    #             lines[0] = lines[0][0:-1]
    #         if lines[0] not in a.users:
    #             print(lines[0])
    #         line = reader.readline()
    #
    # with open(
    #         f"csc111_project_formatted_files_and_code/data/formatted_and_duplicates_removed/anime_formatted_no_duplicates.csv",
    #         "r", newline='', encoding="utf-8") as reader:
    #     line = reader.readline()
    #     while line != '':
    #         lines = line.split(',')
    #         if int(lines[0]) not in a.animes:
    #             print(lines[0])
    #         line = reader.readline()
