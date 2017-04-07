import readCSV
import math

data = readCSV.read_to_dict()


def manhattan(user1, user2):
    result = 0
    for k, v in data[user1].items():
        if (v == 0) or (data[user2][k] == 0):
            continue
        else:
            result += abs(v - data[user2][k])
    return result


def euclidean(user1, user2):
    result = 0.0
    for k, v in data[user1].items():
        if (v == 0) or (data[user2][k] == 0):
            continue
        else:
            result += pow(abs(v - data[user2][k]), 2)
    result = math.sqrt(result)
    return result


def minkowski(user1, user2, r):
    result = 0.0
    for k, v in data[user1].items():
        if (v == 0) or (data[user2][k] == 0):
            continue
        else:
            result += pow(abs(v - data[user2][k]), r)
    result = pow(result, 1 / r)
    return result


def pearson(user1, user2):
    sum_xy = 0
    sum_x = 0
    sum_y = 0
    sum_xx = 0
    sum_yy = 0
    total = 0
    for k, v in data[user1].items():
        if k in data[user2].keys():
            sum_x += v
            sum_y += data[user2][k]
            sum_xx += pow(v, 2)
            sum_yy += pow(data[user2][k], 2)
            sum_xy += v * data[user2][k]
            total += 1
    numerator = sum_xy - (sum_x * sum_y / total)
    denominator = pow(sum_xx - pow(sum_x, 2) / total, 1 / 2) * pow(sum_yy - pow(sum_y, 2) / total, 1 / 2)
    approximation = numerator / denominator
    return approximation


def cosine_similarity(user1, user2):
    dot_production = 0
    x_len = 0
    y_len = 0
    for k, v in data[user1].items():
        if k in data[user2].keys():
            dot_production += v*data[user2][k]
        x_len += pow(v, 2)
    for k, v in data[user2].items():
        y_len += pow(v, 2)
    result = dot_production/(pow(x_len, 1/2)*pow(y_len, 1/2))
    return result


def all_distance(user, mode):
    users = list(data.keys())
    result = {}
    for i in range(len(users)):
        if user != users[i]:
            if mode == 'manhattan':
                result[users[i]] = manhattan(user, users[i])
            elif mode == 'euclidean':
                result[users[i]] = euclidean(user, users[i])
            elif mode == 'pearson':
                result[users[i]] = pearson(user, users[i])
            elif mode == 'cosine':
                result[users[i]] = cosine_similarity(user, users[i])
    result = sorted(result.items(), key=lambda item: item[1])
    return result


def nearest_users(username, num):
    nearest = all_distance(username, 'cosine')
    nearest_result = {}
    keys = []
    values = []
    for k, v in nearest:
        keys.append(k)
        values.append(v)
    keys.reverse()
    values.reverse()
    for i in range(num):
        if i < len(keys):
            nearest_result[keys[i]] = values[i]
    return nearest_result


def recommend(username):
    nearests = nearest_users(username, 5)
    persons = list(nearests.keys())
    unseen = {}
    similarity_sum = 0.0
    rate = 0.0
    for k, v in data[username].items():
        if v == 0:
            for i in range(len(persons)):
                if data[persons[i]][k] == 0:
                    continue
                else:
                    similarity_sum += nearests[persons[i]]
                    rate += nearests[persons[i]] * data[persons[i]][k]
            rate = rate/similarity_sum
            unseen[k] = rate
            similarity_sum = 0.0
            rate = 0.0
    return unseen


if __name__ == "__main__":
    print(data)
    print(all_distance('Bryan', 'manhattan'))
    print(all_distance('Bryan', 'euclidean'))
    print(all_distance('Bryan', 'pearson'))
    print(all_distance('Bryan', 'cosine'))
    print(nearest_users('Bryan', 5))
    print(recommend('Bryan'))
