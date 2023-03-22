"""copyright and usage info here"""
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
        """
        raise NotImplementedError
class ReccomenderGraph:
    """A class for a graph of nodes, where the nodes are users and animes, and edges are reviews

    Instance Attributes
    - users: a list of user nodes
    - animes: a list of anime nodes
    """
    users: list[User]
    animes: list[Anime]
    def __init__(self) -> None:
        """initialize an empty ReccomenderGraph
        Preconditions:
            -
        """
        self.users = []
        self.animes = []

    #check if we should be passing in a new user, or the attributes of a user
    def insert_user(self, user: User) -> None:
        """Add a user into the graph
        Preconditions:
            -
        """
        raise NotImplementedError

    def insert_anime(self, anime: Anime) -> None:
        """Add an anime into the graph
        Preconditions:
            -
        """
        raise NotImplementedError

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


def read_file(files: list[str]) -> ReccomenderGraph:
    """Creates a ReccomenderGraph given the animes. profiles, and reviews formatted in a CSV file
    Preconditions:
            - files are formatted correctly
    """
    raise NotImplementedError


def import_profile(file: str, graph: ReccomenderGraph) -> None:
    """loads a user from a csv file and adds them into the graph
    Preconditions:
        - files are formatted correctly
        - user doesn't exist in graph
    """
    raise NotImplementedError


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
