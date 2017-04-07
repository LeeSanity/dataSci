import csv


def read_to_dict():
    users = []
    movies = []
    movie_ratings = {}
    with open('Movie_Ratings.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        for i, row in enumerate(reader):
            if i == 0:
                for j in range(len(row)):
                    if j == 0:
                        continue
                    else:
                        users.append(row[j])
                        movie_ratings[row[j]] = {}
            else:
                movies.append(row[0])
                for j in range(len(row)):
                    if j == 0:
                        continue
                    else:
                        if row[j] != '':
                            movie_ratings[users[j-1]][row[0]] = int(row[j])
                        else:
                            movie_ratings[users[j-1]][row[0]] = 0
    return movie_ratings
