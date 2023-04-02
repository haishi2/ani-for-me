"""
CSC111 Project: Dataset Formatting Functions

This module contains functions to prep chosen dataset csv file for use in the main algorithm
by editing the information contained. 

This file is Copyright (c) 2023 Hai Shi, Liam Alexander Maguire, Amelia Wu, and Sanya Chawla.
"""
import calendar
import csv
import re
from typing import Any
import python_ta
# from typing import Any, List, Tuple(Uncomment if needed, but List and Tuple are unused imports)

# RECOMPILE DATA of BOTH profiles and reviews whenever a new vet_user keyword is added
# when recompiling, use reviews(accidentally edited).csv, profiles.csv, and animes.csv
# (use the files that I provided since i removed a bunch of entries and columns)

# recompile order: read_and_write_animes. read_and_write_profiles, read_and_write_reviews, \
# and then run the duplicate clearers any way


def read_uids() -> list:
    """A function that reads a csv file containing pre-flagged anime uids.
    Function returns a list of uids to remove.
    """
    uids = []
    with open('data/uids_to_remove.csv', 'r') as reader:
        line = reader.readline()
        while line != '':
            uids.append(line[:-1])
            line = reader.readline()
    return uids


uids_to_remove = read_uids()
anime_uids_added = []


def vet_user(user: str) -> bool:
    """ A function that returns True if the user's name is appropriate.
    User is appropriate if their username does not contain any of a chosen list of keywords.
    If the user's name contains a keyword, the function returns False.
    """
    user = user.lower()
    keywords = ['nigger', 'nigga', 'retard', 'faggot', 'fag', 'pedo', 'racist', 'chink', 'fuck', 'bitch', 'whore',
                'skank', 'wanker', 'bastard', 'dyke', 'asshole', 'dick', 'lolicon', 'fap']
    return not any(keyword in user for keyword in keywords)


def read_and_write_reviews() -> None:
    """Function that writes a separate 'formatted_reviews.csv' file to contain the original dataset's information,
    but with flagged inappropriate users in uids_to_remove removed.
    The csv file will contain information on reviews with...
    The first column being uid(user who made the review),
    The second column will be anime id(anime being reviewed), 
    The third column is the anime's overall rating(out of 10),
    And the following are the ratings for the anime in each category on MyAnimeList
    (ex. {'Overall': '8', 'Story': '8', 'Animation': '8', 'Sound': '10', 'Character': '9', 'Enjoyment': '8'})
    """
    big_lines = []
    # index 0 is uid, 1 is anime id, 2 is overall rating, and then the rest are the ratings for each category
    # (ex. {'Overall': '8', 'Story': '8', 'Animation': '8', 'Sound': '10', 'Character': '9', 'Enjoyment': '8'})
    with open('data/original_data/reviews(accidentally edited).csv', 'r',
              encoding="utf-8") as reader:
        line = reader.readline()
        line = line[:-9]
        # counter = 0(variable not used)
        while line != '':
            # if you want up to a certain amount
            # while counter <= 50:
            lines = line.split(',')
            cond1 = lines[1] not in uids_to_remove
            cond2 = vet_user(lines[0])
            try:
                if cond1 and cond2:
                    for i in range(3, 9):
                        lines[i] = re.search(r'\d+', lines[i]).group()

                    big_lines.append(lines)
            except AttributeError:
                pass

            line = reader.readline()
            line = line[:-9]
            # counter += 1
    # import pprint
    # pprint.pprint(big_lines)
    with open('data/formatted/formatted_reviews.csv', "w", newline='', encoding="utf-8") as f:
        w = csv.writer(f, delimiter=",")
        w.writerows(big_lines)


# don't limit the amount here
# people without reviews will still be in the csv file, they'll just only have a username
def read_and_write_profiles() -> None:
    """A function that writes a separate profiles_formatted.csv file to contain an updated 
    selection of users.
    Only users that have appropriate names will be added to the new file.
    """
    big_lines = []
    # idx 1 username, idx 2 onwards favorite anime
    with open('data/original_data/profiles.csv', 'r', encoding="utf-8") as reader:
        line = reader.readline()

        while line != '':
            lines = line.split(',')
            cond2 = vet_user(lines[0])
            try:
                if cond2:
                    for i in range(1, len(lines)):
                        if lines[i] == '[]\n':
                            lines[i] = ''
                        else:
                            lines[i] = re.search(r'\d+', lines[i]).group()
                        if lines[i] in uids_to_remove or lines[i] not in anime_uids_added:
                            lines[i] = ''
                # removing blank indices
                stuff_to_remove = []
                for i in range(len(lines)):
                    if lines[i] == '':
                        stuff_to_remove.append(lines[i])
                while stuff_to_remove:  # CHANGED THIS FOR STYLE, BUT IT STILL MEANS 'while stuff_to_remove != []'
                    lines.remove(stuff_to_remove.pop())

                if cond2:
                    big_lines.append(lines)
            except AttributeError:
                pass

            line = reader.readline()

    # import pprint
    # pprint.pprint(big_lines)
    with open('data/formatted/profiles_formatted.csv', "w", newline='', encoding="utf-8") as f:
        w = csv.writer(f, delimiter=",")
        w.writerows(big_lines)


# don't limit the amount here
def read_and_write_animes() -> None:
    """A function that reads animes from the original dataset and 
    writes animes_formatted.csv to only include appropriate anime.
    """
    # idx 1 is anime id, idx2 is title, next idxs are genres til dates, start dates first, end date second, last idx is
    # episodes
    big_lines = []
    with open('data/original_data/animes.csv', 'r', errors="ignore", encoding='utf-8') as reader:
        line = reader.readline()

        while line != '':
            lines = line.split(',')
            cond1 = lines[0] not in uids_to_remove

            try:
                if cond1:
                    # fixing genres
                    anime_uids_added.append(lines[0])
                    i = 2
                    start_idx = 2
                    end_idx = 2
                    while "]" not in lines[i]:
                        end_idx += 1
                        i += 1

                    for j in range(start_idx, end_idx + 1):
                        genre = ''
                        for char in lines[j]:
                            if char.isalpha():
                                genre += char
                        lines[j] = genre

                    # i subtract 1 here to correct for index counting starting at 0
                    if len(lines) - end_idx - 1 != 4 or lines[end_idx + 4] == '\n' or lines[end_idx + 4] == '':
                        uids_to_remove.append(lines[0])
                        raise AttributeError
                    else:
                        months = {month: index for index, month in enumerate(calendar.month_abbr) if month}
                        start_date_numbers = re.findall(r'\b\d+\b', lines[end_idx + 1])
                        end_date_numbers = re.findall(r'\b\d+\b', lines[end_idx + 2])
                        if len(end_date_numbers) != 2 or len(start_date_numbers) != 1:
                            uids_to_remove.append(lines[0])
                            raise AttributeError
                        start_date = str(months[lines[end_idx + 1][1:4]]) + '/' + start_date_numbers[0] \
                            + '/' + end_date_numbers[0]
                        end_date = str(months[lines[end_idx + 2][9:12]]) + '/' + end_date_numbers[1] \
                            + '/' + lines[end_idx + 3][1:5]

                        lines[end_idx + 4] = re.search(r'\d+', lines[end_idx + 4]).group()
                        lines[end_idx + 1] = start_date
                        lines[end_idx + 2] = end_date
                        lines.pop(end_idx + 3)

                    big_lines.append(lines)
            except AttributeError:
                pass

            # if cond1:
            #     big_lines.append(lines)
            line = reader.readline()

    with open('data/formatted/animes_formatted.csv', "w", newline='', encoding="utf-8") as f:
        w = csv.writer(f, delimiter=",")
        w.writerows(big_lines)


def remove_anime_duplicates() -> list[tuple[str]]:
    """Removes the duplicate anime in the csv.

    Note:
    Must return tuples here to avoid a hashing error when converting a nested list to a set.
    """
    with open('data/formatted/animes_formatted.csv', 'r', errors="ignore",
              encoding='utf-8') as read_obj:
        csv_reader = csv.reader(read_obj)
        lst_of_csv = list(csv_reader)

    no_dupe_animes = list(set(tuple(anime) for anime in lst_of_csv))
    return no_dupe_animes


def write_anime_no_duplicates() -> None:
    """Write to a new file of the anime after having removed the duplicates."""
    animes = remove_anime_duplicates()
    with open('data/formatted_and_duplicates_removed/anime_formatted_no_duplicates.csv',
              'w', newline='',
              encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerows(animes)


# There shouldn't be any other problems but I'll leave this here in case
# def remove_user_no_reviews() -> list[list[str]]:
#     """Remove users without any reviews"""
#     with open('data/formatted/formatted_reviews.csv', 'r', errors="ignore") as read_obj:
#         csv_reader = csv.reader(read_obj)
#         lst_of_csv = list(csv_reader)
#
#     return lst_of_csv

def remove_review_duplicates() -> list[tuple[str]]:
    """Removes the duplicate reviews in the csv.
    Also removes reviews of anime called #NAME? (due to errors in the csv when using excel).

    Note:
    Must return tuples here to avoid a hashing error when converting a nested list to a set.
    """
    with open('data/formatted/formatted_reviews.csv', 'r', errors="ignore") as read_obj:
        csv_reader = csv.reader(read_obj)
        lst_of_csv = list(csv_reader)

    no_dupe_reviews = list(set(tuple(review) for review in lst_of_csv))
    no_error_anime_name = [review for review in no_dupe_reviews if review[0] != "#NAME?"]
    return no_error_anime_name


def write_review_no_duplicates() -> None:
    """Write to a new file of the reviews after having removed the duplicates.
    """
    reviews = remove_review_duplicates()
    with open('data/formatted_and_duplicates_removed/reviews_formatted_no_duplicates.csv',
              'w',
              newline='',
              encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerows(reviews)


def remove_user_duplicate() -> list[tuple[str]]:
    """Removes the duplicate users in the csv.
    Added: filtering users on their usernames with new keywords.

    Note:
    Must return tuples here to avoid a hashing error when converting a nested list to a set.
    """
    with open('data/formatted/profiles_formatted.csv', 'r', errors="ignore") as read_obj:
        csv_reader = csv.reader(read_obj)
        lst_of_csv = list(csv_reader)

    no_dupe_profiles = list(set(tuple(profile) for profile in lst_of_csv if vet_user(profile[0])))
    return no_dupe_profiles


def write_profiles_no_duplicates() -> None:
    """Write to a new file of the profiles after having removed the duplicates.
    """
    profiles = remove_user_duplicate()
    with open('data/formatted_and_duplicates_removed/profiles_formatted_no_duplicates.csv',
              'w',
              newline='',
              encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerows(profiles)


def fix_inconsistent_users() -> tuple[list[Any], list[Any]]:
    """Returns a tuple where index 0 and 1 are all reviews and profiles that have users that are both in the profiles
    and reviews data sets respectively.
    """
    with open('data/formatted_and_duplicates_removed/reviews_formatted_no_duplicates.csv',
              'r',
              errors="ignore") as read_obj:
        csv_reader = csv.reader(read_obj)
        reviews = list(csv_reader)

    with open('data/formatted_and_duplicates_removed/profiles_formatted_no_duplicates.csv',
              'r',
              errors="ignore") as read_obj:
        csv_reader = csv.reader(read_obj)
        profiles = list(csv_reader)

    users_in_reviews = [user[0] for user in reviews]
    users_in_profiles = [user[0] for user in profiles]
    users_in_both = [user for user in users_in_profiles if user in users_in_reviews]

    consistent_reviews = [review for review in reviews if review[0] in users_in_both]
    consistent_profiles = [profile for profile in profiles if profile[0] in users_in_both]
    consistent_data = (consistent_reviews, consistent_profiles)

    return consistent_data


def write_consistent_users() -> None:
    """Rewrite the profiles and reviews excluding the reviews and profiles of users that aren't present in both data
    sets.

    Also takes a while if you run it just be patient :)
    """
    consistent_data = fix_inconsistent_users()
    reviews, profiles = consistent_data[0], consistent_data[1]

    with open('data/formatted_and_duplicates_removed/profiles_formatted_no_duplicates.csv', 'w',
              newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerows(profiles)

    with open('data/formatted_and_duplicates_removed/reviews_formatted_no_duplicates.csv', 'w',
              newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerows(reviews)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    python_ta.check_all(config={
        'extra-imports': ['calendar', 'csv', 're', 'typing'],  # the names (strs) of imported modules
        'disable': ['too-many-nested-blocks', 'too-many-locals', 'unnecessary-indexing',
                    'forbidden-top-level-code', 'forbidden-global-variables'],
        'allowed-io': ['read_uids', 'read_and_write_reviews', 'read_and_write_profiles',
                       'read_and_write_animes', 'remove_anime_duplicates', 'write_anime_no_duplicates',
                       'remove_review_duplicates', 'write_review_no_duplicates', 'remove_user_duplicate',
                       'write_profiles_no_duplicates', 'fix_inconsistent_users', 'write_consistent_users'],
        # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
