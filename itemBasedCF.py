data = {'David': {'Kacey Musgraves': 0, 'Imagine Dragons': 3, 'Daft Punk': 5, 'Lorde': 4, 'Fall Out Boy': 1},
        'Matt': {'Kacey Musgraves': 0, 'Imagine Dragons': 3, 'Daft Punk': 4, 'Lorde': 4, 'Fall Out Boy': 1},
        'Ben': {'Kacey Musgraves': 4, 'Imagine Dragons': 3, 'Daft Punk': 0, 'Lorde': 3, 'Fall Out Boy': 1},
        'Chris': {'Kacey Musgraves': 4, 'Imagine Dragons': 4, 'Daft Punk': 4, 'Lorde': 3, 'Fall Out Boy': 1},
        'Torri': {'Kacey Musgraves': 5, 'Imagine Dragons': 4, 'Daft Punk': 5, 'Lorde': 0, 'Fall Out Boy': 3}
        }

data_ = {'Amy': {'Taylor Swift': 4, 'PSY': 3, 'Whitney Houston': 4},
         'Ben': {'Taylor Swift': 5, 'PSY': 2, 'Whitney Houston': 0},
         'Clara': {'Taylor Swift': 0, 'PSY': 3.5, 'Whitney Houston': 4},
         'Daisy': {'Taylor Swift': 5, 'PSY': 0, 'Whitney Houston': 3}
         }

users_ = list(data_.keys())
users = list(data.keys())
movies = list(data['David'].keys())


def cal_average_rating():
    average = {}
    for i in range(len(users)):
        rates = data[users[i]]
        ave = 0
        count = 0
        for v in rates.values():
            if v != 0:
                ave += v
                count += 1
        average[users[i]] = ave/count
    return average


def cosine_similarity(item1, item2):
    average = cal_average_rating()
    numerator = 0.0
    denominator_left = 0.0
    denominator_right = 0.0
    for user in users:
        if data[user][item1] != 0 and data[user][item2] != 0:
            numerator += (data[user][item1]-average[user])*(data[user][item2]-average[user])
            denominator_left += pow(data[user][item1]-average[user], 2)
            denominator_right += pow(data[user][item2]-average[user], 2)
    similarity = numerator/(pow(denominator_left, 1/2)*pow(denominator_right, 1/2))
    return similarity


def predict(user, item):
    similarity_matrix = {}
    for movie in movies:
        similarity_matrix[movie] = {}
        # if i != (len(movies)-1):
        #     for j in range(len(movies)-1-i):
        #         similarity_matrix[movies[i]][movies[i+j+1]] = cosine_similarity(movies[i], movies[i+j+1])
        for movie1 in movies:
            if movie != movie1:
                similarity_matrix[movie][movie1] = cosine_similarity(movie, movie1)
    max_rate = 5
    min_rate = 1
    numerator = 0.0
    denominator = 0.0
    similar_movies = movies
    similar_movies.remove(item)
    for similar_item in similar_movies:
        denormalized_rate = (2*(data[user][similar_item]-min_rate)-(max_rate-min_rate))/(max_rate-min_rate)
        numerator += similarity_matrix[item][similar_item]*denormalized_rate
        denominator += abs(similarity_matrix[item][similar_item])
    #   print('movie: %s rate: %f denor: %f' % (similar_item, similarity_matrix[item][similar_item], denormalized_rate))
    p = numerator/denominator
    normalized_p = (p+1)*(max_rate-min_rate)/2 + min_rate
    return normalized_p


def card(item1, item2):
    count = 0
    for user in users_:
        if data_[user][item1] != 0 and data_[user][item2] != 0:
            count += 1
    return count


def slope_one(username, item):
    deviation = {}
    artists = list(data_['Amy'].keys())
    devi = 0
    for artist in artists:
        deviation[artist] = {}
        for artist_ in artists:
            if artist != artist_:
                card_num = card(artist, artist_)
                for user in users_:
                    if data_[user][artist] != 0 and data_[user][artist_] != 0:
                        devi += data_[user][artist] - data_[user][artist_]
                devi = devi/card_num
                deviation[artist][artist_] = devi
                devi = 0
    print(deviation)
    numerator = 0.0
    denominator = 0.0
    for k, v in data_[username].items():
        if k != item and v != 0:
            numerator += (deviation[item][k] + v)*card(item, k)
            denominator += card(item, k)
    p = numerator/denominator
    print('here')
    return p


if __name__ == "__main__":
    pass
    # print(predict('David', 'Kacey Musgraves'))
    # print(slope_one('Ben', 'Whitney Houston'))
