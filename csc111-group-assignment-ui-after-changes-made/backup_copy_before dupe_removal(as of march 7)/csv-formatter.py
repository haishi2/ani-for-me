import calendar
import csv
import re
#RECOMPILE DATA of BOTH profiles and reviews whenever a new vet_user keyword is added
#when recompling, use reviews(accidentally edited).csv, profiles.csv, and animes.csv (use the files that I provided since i removed a bunch of entries and columns)
#TODO: change file paths after downloading file

def read_uids() -> list:
    uids = []
    with open('/group assignment/uids_to_remove.csv', 'r') as reader:
        line = reader.readline()
        while line != '':
            uids.append(line[:-1])
            line = reader.readline()
    return uids

def vet_user(user: str):
    user = user.lower()
    keywords = ['nigger','nigga', 'retard', 'faggot', 'fag', 'pedo', 'racist', 'chink']
    return not any(keyword in user for keyword in keywords)


def read_and_write_reviews():
    uids_to_remove = read_uids()
    big_lines = []
    # index 0 is uid, 1 is anime id, 2 is overall rating, and then the rest are the ratings for each category (ex. {'Overall': '8', 'Story': '8', 'Animation': '8', 'Sound': '10', 'Character': '9', 'Enjoyment': '8'})
    with open('/group assignment/reviews(accidentally edited).csv', 'r', encoding="utf-8") as reader:
        line = reader.readline()
        line = line[:-9]
        counter = 0
        while line != '':
        #if you want up to a certain amount
        # while counter <= 50:
            lines = line.split(',')
            cond1 = lines[1] not in uids_to_remove
            cond2 = vet_user(lines[0])
            try:
                if(cond1 and cond2):
                    for i in range(3, 9):
                        lines[i] = re.search(r'\d+', lines[i]).group()
                    # lines[3] = re.search(r'\d+', lines[3]).group()
                    # lines[4] = re.search(r'\d+', lines[4]).group()
                    # lines[5] = re.search(r'\d+', lines[5]).group()
                    # lines[6] = re.search(r'\d+', lines[6]).group()
                    # lines[7] = re.search(r'\d+', lines[7]).group()
                    # lines[8] = re.search(r'\d+', lines[8]).group()

                    big_lines.append(lines)
            except AttributeError:
                pass

            line = reader.readline()
            line = line[:-9]
            # counter += 1
    # import pprint
    # pprint.pprint(big_lines)
    with open("/group assignment/formatted_reviews.csv", "w", newline='', encoding="utf-8") as f:
        w = csv.writer(f, delimiter=",")
        w.writerows(big_lines)

#don't limit the amount here
#people without reviews will still be in the csv file, they'll just only have a username
def read_and_write_profiles():
    uids_to_remove = read_uids()
    big_lines = []
    #idx 1 username, idx 2 onwards favorite anime
    with open('/group assignment/profiles.csv', 'r', encoding="utf-8") as reader:
        line = reader.readline()

        while line != '':
            lines = line.split(',')
            cond2 = vet_user(lines[0])
            try:
                if (cond2):
                    for i in range(1, len(lines)):
                        if(lines[i] == '[]\n'):
                            lines[i] = ''
                        else:
                            lines[i] = re.search(r'\d+', lines[i]).group()
                        if(lines[i] in uids_to_remove):
                            lines[i] = ''
                # removing blank indices
                stuff_to_remove = []
                for i in range(len(lines)):
                    if lines[i] == '':
                        stuff_to_remove.append(lines[i])
                while stuff_to_remove != []:
                    lines.remove(stuff_to_remove.pop())

                if (cond2):
                    big_lines.append(lines)
            except AttributeError:
                pass

            line = reader.readline()
            # #removing blank indices
            # stuff_to_remove = []
            # for i in range(len(lines)):
            #     if lines[i] == '':
            #         stuff_to_remove.append(lines[i])
            # while stuff_to_remove != []:
            #     lines.remove(stuff_to_remove.pop())
            #
            # if (cond2):
            #     big_lines.append(lines)
            # line = reader.readline()

    # import pprint
    # pprint.pprint(big_lines)
    with open("/group assignment/profiles_formatted.csv", "w", newline='', encoding="utf-8") as f:
        w = csv.writer(f, delimiter=",")
        w.writerows(big_lines)

#don't limit the amount here
def read_and_write_animes():
    #idx 1 is anime id, idx2 is title, next idxs are genres til dates, start dates first, end date second, last idx is # episodes
    uids_to_remove = read_uids()
    big_lines = []
    with open('/group assignment/animes.csv', 'r', errors="ignore") as reader:
        line = reader.readline()

        while line != '':
            lines = line.split(',')
            cond1 = lines[0] not in uids_to_remove

            try:
                if (cond1):
                    #fixing genres

                    i = 2
                    start_idx = 2
                    end_idx = 2
                    while "]" not in lines[i]:
                        # print(lines)
                        end_idx += 1
                        i += 1

                    for j in range(start_idx, end_idx + 1):
                        genre = ''
                        for char in lines[j]:
                            if(char.isalpha()):
                                genre += char
                        lines[j] = genre

                    #fixing dates
                    #i subtract 1 here to correct for index counting starting at 0
                    if(len(lines) - end_idx - 1 != 4):
                        raise AttributeError
                    else:
                        #the date formats that aren't for movies are fixed
                        months = {month: index for index, month in enumerate(calendar.month_abbr) if month}
                        start_date = str(months[lines[end_idx + 1][1:4]]) + '/' + lines[end_idx + 1][-1] \
                                      +  '/' + lines[end_idx + 2][1:5]
                        end_date = str(months[lines[end_idx + 2][9:12]]) + '/' + lines[end_idx + 2][13:] \
                                   + '/' + lines[end_idx + 3][1:5]
                        lines[end_idx + 4] = re.search(r'\d+', lines[end_idx + 4]).group()
                        lines[end_idx + 1] = start_date
                        lines[end_idx + 2] = end_date
                        lines.pop(end_idx + 3)

                    big_lines.append(lines)
            except AttributeError:
                pass

            # if (cond1):
            #     big_lines.append(lines)
            line = reader.readline()

    with open("/group assignment/animes_formatted.csv", "w", newline='', encoding="utf-8") as f:
        w = csv.writer(f, delimiter=",")
        w.writerows(big_lines)
