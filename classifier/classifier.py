
class Classifier(object):
	def __init__(self, train_file_dir, test_file_dir):
		self.train_items = self.read_data(train_file_dir)
		self.test_items = self.read_data(test_file_dir)
		self.normalize_train_items = self.normalize(self.train_items)
		self.normalize_test_items = self.normalize(self.test_items)

	def read_data(self, file_dir):
		data = []
		f = open(file_dir, 'r')
		for line in f:
			item = line.strip('\n').split('\t')
			if item[0] != 'comment':
				item_tuple = (item[0], item[1], item[2:4])
				data.append(item_tuple)
		return data

	def normalize(self, items):
		height_list = []
		weight_list = []
		for item in items:
			height_list.append(item[2][0])
			weight_list.append(item[2][1])
		normalized_height = self.normalize_column(height_list)
		normalized_weight = self.normalize_column(weight_list)
		normalized_items = []
		for i in range(len(normalized_height)):
			normalized_items.append((items[i][0], [normalized_height[i], normalized_weight[i]]))
		return normalized_items

	def normalize_column(self, data_list):
		normalized_data_list = []
		length = len(data_list)
		median = self.get_median(data_list)
		asd = self.get_absolute_standard_deviation(data_list)
		for i in range(length):
			modified_standard_score = (int(data_list[i]) - median)/asd
			normalized_data_list.append(modified_standard_score)
		return normalized_data_list

	def get_median(self, data_list):
		length = len(data_list)
		if length % 2 != 0:
			return data_list[(length-1)/2]
		else:
			return (int(data_list[int(length/2)]) + int(data_list[int(length/2) - 1]))/2

	def get_absolute_standard_deviation(self, data_list):
		length = len(data_list)
		median = self.get_median(data_list)
		asd = 0.0
		for i in range(length):
			asd += abs(int(data_list[i]) - median)
		asd /= length
		return asd

	def distance(self, vector1, vector2, r):
		dis = 0.0
		length = len(vector1)
		for i in range(length):
			dis += pow(abs(float(vector1[i]) - float(vector2[i])), r)
		return pow(dis, 1 / r)

	def nearest_neighbors(self, k, item_name, item_vector):
		nearests = []
		for item in self.normalize_train_items:
			if item[0] != item_name:
				current_dis = self.distance(item_vector, item[1], 1)
				nearests.append((item[0], current_dis))
		nearests.sort(key=lambda s_item: s_item[1])
		return nearests[0:k]

	def get_type(self, name, items):
		for item in items:
			if name == item[0]:
				return item[1]

	def classify(self, item_name, item_vector):
		nearest = self.nearest_neighbors(1, item_name, item_vector)
		return self.get_type(nearest[0][0], self.train_items)

	def test(self):
		total_count = 0
		right_count = 0
		for item in self.normalize_test_items:
			if self.get_type(item[0], self.test_items) == self.classify(item[0], item[1]):
				right_count += 1
			total_count += 1
		print('%d right classified in %d tests: %f' % (right_count, total_count, right_count / total_count))


def main():
	classifier = Classifier("../data/athletesTrainingSet.txt", "../data/athletesTestSet.txt")
	classifier.test()


if __name__ == '__main__':
	main()
