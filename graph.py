"""copyright and usage info here"""
from __future__ import annotations
import datetime
import re

import python_ta

import anime_and_users as aau

#TODO see which instance attributes should be made private, add preconditions
class Review:
    """An edge that connects a user and an anime which contains the ratings the user gave

    Instance Attributes
    - endpoints: The two nodes linked by this review
    - ratings: the ratings that the user gave for the individual categories
    """
    endpoints: tuple[aau.User, aau.Anime]
    ratings: dict[str, int]

    def __init__(self, e1: aau.User, e2: aau.Anime, ratings: dict[str, int]) -> None:
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
        self.animes[anime._UID] = anime
        return anime

    def add_friends(self, user: str, friend_user: str) -> None:
        """Connect this user and the friend_user together
        Preconditions:
            - both users exist in the graph
        """
        self.users[user].friends_list.append(self.users[friend_user])
        self.users[friend_user].friends_list.append(self.users[user])

    #float is path score between 0 - 10 (actual path score avgd with the similarity)
    def get_all_path_scores(self, depth: int, username: str) -> dict[aau.Anime: float]:
        """Find all anime at a certain depth and calculate a path score for each anime based on
        the reviews given to it and the user's priorities, and returns the anime with the top 10 path scores
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


def tag_keywords_and_strip(query: str) -> list[str]:
    """Takes a query for an anime and simplfies it into its keywords, with only alphanumeric characters and all lowercase
    Preconditions:
            -
    """
    # re.sub works by subbing anything not in the range of the character ranges provided with the second param
    #the plus after the list brackets are to remove repetition of anything in the set of characters after the first match
    #the caret is used to tell the regex to match any characters that are not in this set
    query_cleaned = re.sub('[^0-9a-zA-z]+', ' ', query)
    query_keywords = query_cleaned.split(' ')
    #add any extra connecting words here (in lowercase)
    connecting_words = ['in', 'the', 'and', 'wa', 'no', 'of', 'to']

    for keyword in query_keywords:
        if keyword.lower() in connecting_words or keyword in ('', '\n'):
            query_keywords.remove(keyword)
        # else:
        #     #this shouldn't be needed since its already cleaned at the syart
        #     query_keywords[query_keywords.index(keyword)] = \
        #         re.sub('[^0-9a-zA-z]+', ' ', query_keywords[query_keywords.index(keyword)].lower())

    return query_keywords

def search(query: str, graph: ReccomenderGraph) -> list[aau.Anime]:
    """Searches for all animes in a ReccomenderGraph with at least a 33% keyword match and returns them
    Preconditions:
            -
    """
    pass

# read files in this order: anime, user, reviews
# files: ['csc111_project_formatted_files_and_code/data/formatted_and_duplicates_removed/anime_formatted_no_duplicates.csv', 'csc111_project_formatted_files_and_code/data/formatted_and_duplicates_removed/profiles_formatted_no_duplicates.csv', 'csc111_project_formatted_files_and_code/data/formatted_and_duplicates_removed/reviews_formatted_no_duplicates.csv']
#TODO may be an error here where some users aren't read in, if there are any errors in the future investigate this
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
            genres = set()
            i = 2
            while all(char.isalpha() for char in lines[i]):
                genres.add(lines[i])
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
            favorite_animes = set()
            for i in range(1, len(lines)):
                favorite_animes.add(graph.animes[int(lines[i])])

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
    # python_ta.check_all(config={
    #     'extra-imports': ['anime_and_users', 'datetime', 're'],  # the names (strs) of imported modules
    #     'allowed-io': ['import_profile', 'save_profile', 'read_file'],
    #     # the names (strs) of functions that call print/open/input
    #     'max-line-length': 120
    # })
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
