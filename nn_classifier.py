items = {
	"Dr Dog/Fate": [2.5, 4, 3.5, 3, 5, 4, 1],
	"Phoenix/Lisztomania": [2, 5, 5, 3, 2, 1, 1],
	"Heartless Bastards/Out at Sea": [1, 5, 4, 2, 4, 1, 1],
	"Todd Snider/Don't Tempt Me": [4, 5, 4, 4, 1, 5, 1],
	"The Black Keys/Magic Potion": [1, 4, 5, 3.5, 5, 1, 1],
	"Glee Cast/Jessie's Girl": [1, 5, 3.5, 3, 4, 5, 1],
	"La Roux/Bulletproof": [5, 5, 4, 2, 1, 1, 1],
	"Mike Posner": [2.5, 4, 4, 1, 1, 1, 1],
	"Black Eyed Peas/Rock That Body": [2, 5, 5, 1, 2, 2, 4],
	"Lady Gaga/Alejandro": [1, 5, 3, 2, 1, 2, 1]
}

users = {
	"Angelica": {
		"Dr Dog/Fate": "L",
		"Phoenix/Lisztomania": "L",
		"Heartless Bastards/Out at Sea": "D",
		"Todd Snider/Don't Tempt Me": "D",
		"The Black Keys/Magic Potion": "D",
		"Glee Cast/Jessie's Girl": "L",
		"La Roux/Bulletproof": "D",
		"Mike Posner": "D",
		"Black Eyed Peas/Rock That Body": "D",
		"Lady Gaga/Alejandro": "L"
	},
	"Bill": {
		"Dr Dog/Fate": "L", "Phoenix/Lisztomania": "L",
		"Heartless Bastards/Out at Sea": "L",
		"Todd Snider/Don't Tempt Me": "D",
		"The Black Keys/Magic Potion": "L",
		"Glee Cast/Jessie's Girl": "D",
		"La Roux/Bulletproof": "D", "Mike Posner": "D",
		"Black Eyed Peas/Rock That Body": "D",
		"Lady Gaga/Alejandro": "D"}
}


def read_data(file_dir):
	data = []
	f = open(file_dir, 'r')
	for line in f:
		item = line.strip('\n').split('\t')
		if item[0] != 'comment':
			item_tuple = (item[0], item[1], item[2:4])
			data.append(item_tuple)
	return data


def distance(vector1, vector2, r):
	dis = 0
	length = len(vector1)
	for i in range(length):
		dis += pow(abs(vector1[i]-vector2[i]), r)
	return pow(dis, 1/r)


def nearest_neghbor(item_name, item_vector, all_items):
	nearests = []
	nearest = ''
	min_dis = 10000
	for k, v in all_items.items():
		if k != item_name:
			current_dis = distance(item_vector, v, 1)
			if current_dis < min_dis:
				min_dis = current_dis
				nearest = k
			nearests.append((k, current_dis))
	nearests.sort(key=lambda item: item[1])
	print(nearests)
	return nearest


def classifier(user, item_name, item_vector):
	nearest = nearest_neghbor(item_name, item_vector, items)
	return users[user][nearest]


def main():
	# nearest_neghbor("Chris Cagle/ I Breathe In. I Breathe Out", [1, 5, 2.5, 1, 1, 5, 1], items)
	# print(classifier('Angelica', 'Cagle', [1, 5, 2.5, 1, 1, 5, 1]))
	print(read_data("data/athletesTrainingSet.txt"))

if __name__ == '__main__':
	main()

