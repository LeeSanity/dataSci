import math

class Normalization(object):
	def __init__(self):
		self.data_file_suffix = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
		self.result = {}


	def get_normailized_data(self):
		for suffix in self.data_file_suffix:
			file_name = 'pima-' + suffix
			file_dir = '../data/pima/' + file_name
			bucket_data = []
			for line in open(file_dir, 'r'):
				item = line.strip('\n').split('\t')
				bucket_data.append(item)
			self.result[file_name] = self.normalize(bucket_data)
		return self.result

	def normalize(self, original_data_list):
		medians = []
		asds = []
		reshape = []
		a = zip(*original_data_list)
		for data in a:
			reshape.append(list(data))
		for i in range(len(reshape)-1):
			medians.append(self.get_median(reshape[i]))
			asds.append(self.get_asd(reshape[i]))
		normalized_data_list = []
		for item in original_data_list:
			modified_item = []
			for index, item_attr in enumerate(item[:-2]):
				modified_attr = round((float(item_attr) - medians[index]) / asds[index], 5)
				modified_item.append(modified_attr)
			modified_item.append(item[-1])
			normalized_data_list.append(modified_item)
		return normalized_data_list

	def get_median(self, alist):
		length = len(alist)
		if length % 2 != 0:
			return float(alist[int((length-1)/2)])
		else:
			return (float(alist[int(length/2)]) + float(alist[int(length/2) - 1]))/2

	def get_asd(self, alist):
		length = len(alist)
		median = self.get_median(alist)
		asd = 0.0
		for i in range(length):
			asd += abs(float(alist[i]) - median)
		asd /= length
		return asd


class KNNClassfier(object):
	def __init__(self, r, k, data_set):
		self.k = k
		self.r = r
		self.data_set = data_set
		self.train_set = []
		self.test_set = []
		self.right = {'0': {'0': 0, '1': 0}, '1': {'0': 0, '1': 0}}

	def distance(self, vector1, vector2):
		dis = 0.0
		length = len(vector1) - 1
		for i in range(length):
			dis += pow(abs(float(vector1[i]) - float(vector2[i])), self.r)
		return pow(dis, 1 / self.r)

	def nearest_neighbors(self, item_vector):
		nearests = []
		for item in self.train_set:
			current_dis = self.distance(item_vector, item)
			nearests.append((current_dis, item))
		nearests.sort(key=lambda ite: ite[0])
		return nearests[0:self.k]

	def classify(self, item_vector):
		neighbors = self.nearest_neighbors(item_vector)
		classifier = {'0': 0, '1': 0}
		for neighbor in neighbors:
			if neighbor[1][-1] == '0':
				classifier['0'] += 1
			else:
				classifier['1'] += 1
		if classifier['0'] >= classifier['1']:
			return '0'
		else:
			return '1'

	def ten_fold(self):
		for key in self.data_set.keys():
			print("testSet:%s is testing" % key)
			self.test_set = self.data_set[key]
			train_set = []
			for key_ in self.data_set.keys():
				if key != key_:
					train_set.extend(self.data_set[key_])
			self.train_set = train_set
			for test_item in self.test_set:
				classifier = self.classify(test_item)
				self.right[test_item[-1]][classifier] += 1
		return self.right


class BayesianClassifier(object):
	def __init__(self):
		self.file_suffix = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
		self.data_set = self.read_data()
		self.train_set = {}
		self.test_set = []
		self.bayesian_model = {}
		self.right = {'0': {'0': 0, '1': 0}, '1': {'0': 0, '1': 0}}

	def read_data(self):
		data_set = {}
		for suffix in self.file_suffix:
			file_name = 'pima-' + suffix
			file_dir = '../data/pima/' + file_name
			bucket_data = []
			for line in open(file_dir, 'r'):
				item = line.strip('\n').split('\t')
				bucket_data.append(item)
			data_set[file_name] = bucket_data
		return data_set

	def classify_data(self, data_set):
		pre_data_set = {'0': [], '1': []}
		for data_item in data_set:
			if data_item[-1] == '0':
				pre_data_set['0'].append(data_item)
			else:
				pre_data_set['1'].append(data_item)
		return pre_data_set

	def train(self):
		bayesian_model = {'0': [], '1': [], 'p0': 0.0, 'p1': 0.0}
		for key in self.train_set.keys():
			a = zip(*self.train_set[key])
			reshape = []
			bays_model = {}
			for data in a:
				reshape.append(list(data))
			for col in reshape[:-1]:
				bays_model['mean'] = self.get_mean(col)
				bays_model['ssd'] = self.get_ssd(col)
				bayesian_model[key].append(bays_model)
		bayesian_model['p0'] = len(self.train_set['0'])/(len(self.train_set['0'])+len(self.train_set['1']))
		bayesian_model['p1'] = 1 - bayesian_model['p0']
		self.bayesian_model = bayesian_model

	def get_mean(self, a_list):
		total = 0.0
		for num in a_list:
			total += float(num)
		return total/len(a_list)

	def get_ssd(self, a_list):
		mean = self.get_mean(a_list)
		ssd = 0.0
		for num in a_list:
			ssd += pow((float(num)-mean), 2)
		return pow(ssd/(len(a_list)-1), 1/2)

	def gaussian_p(self, x, mean, ssd):
		e_part = pow(math.e, -(float(x) - mean) ** 2 / (2 * ssd ** 2))
		p = (1.0 / (math.sqrt(2 * math.pi) * ssd)) * e_part
		return p

	def classify(self, item_vector):
		probility_0 = self.bayesian_model['p0']
		for index in range(len(item_vector[:-1])):
			probility_0 *= self.gaussian_p(item_vector[index], self.bayesian_model['0'][index]['mean'], self.bayesian_model['0'][index]['ssd'])
		probility_1 = self.bayesian_model['p1']
		for index in range(len(item_vector[:-1])):
			probility_1 *= self.gaussian_p(item_vector[index], self.bayesian_model['1'][index]['mean'], self.bayesian_model['1'][index]['ssd'])
		print(probility_0, probility_1)
		# length = len(item_vector) - 1
		# pot = 0.0
		# mul_ssd = 1.0
		# for i in range(length):
		# 	pot += ((float(item_vector[i])-self.bayesian_model['1'][i]['mean'])**2/self.bayesian_model['1'][i]['ssd']**2 -
		# 		(float(item_vector[i])-self.bayesian_model['0'][i]['mean'])**2/self.bayesian_model['0'][i]['ssd']**2)
		# 	mul_ssd *= self.bayesian_model['1'][i]['ssd']/self.bayesian_model['0'][i]['ssd']
		# comp = math.exp(pot)*mul_ssd*probility_0/probility_1
		# print(comp)
		if probility_0 >= probility_1:
			return '0'
		else:
			return '1'

	def ten_fold(self):
		for key in self.data_set.keys():
			print("testSet:%s is testing" % key)
			self.test_set = self.data_set[key]
			train_set = []
			for key_ in self.data_set.keys():
				if key != key_:
					train_set.extend(self.data_set[key_])
			self.train_set = self.classify_data(train_set)
			self.train()
			for test_item in self.test_set:
				classify_result = self.classify(test_item)
				self.right[test_item[-1]][classify_result] += 1
		return self.right


def main():
	# normalize = Normalization()
	# # r=1, k=1
	# knn_1 = KNNClassfier(1, 1, normalize.get_normailized_data())
	#
	# # r=1, k=3
	# knn_2 = KNNClassfier(1, 3, normalize.get_normailized_data())
	# print(knn_1.ten_fold())
	# print(knn_2.ten_fold())

	bayes = BayesianClassifier()
	print(bayes.ten_fold())

if __name__ == '__main__':
	main()
