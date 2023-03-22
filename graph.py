"""copyright and usage info here"""
import datetime

import python_ta

from anime_and_users import User, Anime


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
        #take the result from the helper in User and for each path, calculate its path score
        raise NotImplementedError

    #calc_path_scores should take a list of reviews since to calculate the path score we need to average the ratings on each path
    #weighted by the user's preferences
    def calculate_path_score(self, path: list[Review]) -> float:
        """Helper function for get_all_path_scores that calculates the path score for the given path
        Preconditions:
            -
        """
        #remember to average the caluclated path score with the similarity rating for the anime at the endpoint
        raise NotImplementedError

#read files in this order: anime, user, reviews
#remember that the users in csv files dont have friends_list or priorities, so use the (param) = notation when making
#user classes
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
            username = lines[0]
            for i in range(1, len(lines)):


def import_profile(file: str, graph: ReccomenderGraph) -> None:
    """loads a user from a csv file and adds them into the graph
    Preconditions:
        - files are formatted correctly
        - user doesn't exist in graph
        - every anime in the user csv file exists in the graph
        - avery user in the friends_list exists
    """
    raise NotImplementedError


#write reviews in as anime name, ratings alternating for every review so can read back in and access the animes by ids
#and create new reviews
def save_profile(user: User, file_name: str) -> None:
    """save the user's profile into a csv file
    Preconditions:
        -
    """


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
    python_ta.check_all(config={
        'extra-imports': ['anime_and_users'],  # the names (strs) of imported modules
        'allowed-io': ['import_profile', 'save_profile'],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
