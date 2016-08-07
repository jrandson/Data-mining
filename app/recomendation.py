#!/usr/bin/env python

from math import sqrt
from music_rates import music_rates
import codecs


users2 = {"Amy": {"Taylor Swift": 4, "PSY": 3, "Whitney Houston": 4},
		  "Ben": {"Taylor Swift": 5, "PSY": 2},
          "Clara": {"PSY": 3.5, "Whitney Houston": 4},
          "Daisy": {"Taylor Swift": 5, "Whitney Houston": 3}}

class Recommender:

	def __init__(self, data, k=1, metric='pearson', n=5):
		
		self.k = k
		self.metric = metric
		self.n = n
		self.username2id = {}
		self.userid2name = {}
		self.productid2name = {}

		self.frequencies = {}
		self.deviations = {}

		

		if self.metric == 'pearson':
			self.fn = self.pearson

		if type(data).__name__ == 'dict':
			self.data = data

	def convertProductID2name(self, id):
		"""Given product id number return product name"""
		if id in self.productid2name:
			return self.productid2name[id]
		else:
			return id

	def userRatings(self, id, n):
		""" Return n top ratings """
		print "Rating for " + self.userid2name[id]
		ratings = self.data[id]
		print len(ratings)
		ratings = list(ratings.items())
		ratings = [(self.convertProductID2name(k), v) for (k,v) in ratings]

		ratings = ratings[:n]

		for rating in ratings:
			print "%s \t%i" % rating[0], rating[1]

	def loadBookBD(self, path ='BX-Dump/'):
		"""loads the BX book dataset. Path is where the BX files are located"""
 		self.data = {}
 		i = 0
		 #
		 # First load book ratings into self.data
		 #
 		f = codecs.open(path + "BX-Book-Ratings.csv", 'r', 'utf8')
 		for line in f:
 			i += 1		
		
		# separate line into fields
		fields = line.split(';')
		user = fields[0].strip('"')
		book = fields[1].strip('"')
		rating = int(fields[2].strip().strip('"'))
		if user in self.data:
 			currentRatings = self.data[user]
 		else:
 			currentRatings = {}

 		currentRatings[book] = rating
 		self.data[user] = currentRatings
 		f.close()
		
		#
		# Now load books into self.productid2name
		# Books contains isbn, title, and author among other fields
		#
 		f = codecs.open(path + "BX-Books.csv", 'r', 'utf8')
 		for line in f:
 			i += 1 		
	 		# separate line into fields
	 		fields = line.split(';')
	 		isbn = fields[0].strip('"')
	 		title = fields[1].strip('"')
	 		author = fields[2].strip().strip('"')
	 		title = title + ' by ' + author
	 		self.productid2name[isbn] = title
 		f.close()
		
		#
		# Now load user info into both self.userid2name and
		# self.username2id
		#
 		
 		f = codecs.open(path + "BX-Users.csv", 'r', 'utf8')
 		for line in f:
 			i += 1
 
 		# separate line into fields
 		fields = line.split(';')
 		userid = fields[0].strip('"')

		location = fields[1].strip('"')
 		if len(fields) > 3:
 			age = fields[2].strip().strip('"')
 		else:
 			age = 'NULL'
 		
 		if age != 'NULL':
 			value = location + ' (age: ' + age + ')'
 		else:
 			value = location
 		
 		self.userid2name[userid] = value
 		self.username2id[location] = userid
	 	f.close()
	 	
	 	print(i)

	def loadMovieBD(self,path = 'Movies/'):
		

		f = codecs.open(path + 'Movie_Ratings.csv','r', 'utf8')
		source = []
		i = 0
		for line in f:
			source.append(line)
		f.close()


		tmp = source[0].split(',')
		users = []
		for line in tmp:
			if not line.strip('"') == '':
				users.append(line.strip('"'))
		

		#prepair the ratings dictionary
		ratings = {}
		for user in users:
			ratings[user.strip("")] = {}

		#get teh movies
		movies = {}		
		for i in range(1,len(source)):
			line = source[i].split(',')
			movie = line[0]
			movies[movie] = line[1:]
		
		#populate the dictionary
		for movie in movies:
			rate = movies[movie]			
			for i in range(len(users)):
				if not rate[i].strip().strip('"') == '':
					ratings[users[i]][movie.strip('"')] = int(rate[i].strip().strip('"'))

		self.data = ratings


	def manhattam(self, rate1, rate2):

		distance = 0
		for key in rate1.keys():
			if key in rate2.keys():
				distance += abs(rate1[key] - rate2[key])

		return distance

	def euclidian(self, rate1, rate2):
		distance = 0

		for key in rate1:
			if key in rate2:
				distance += pow(abs(rate1[key] - rate2[key]),2)

		return pow(distance,0.5)

	def minkowski(self, rate1,rate2,r):
		distance = 0
		for title in rate1.keys():
			if title in rate2.keys():
				distance += pow(abs(rate1[title] - rate2[title]),r)

		return pow(distance, 1.0/r)

	def computeNearestNeighbod(self, username):
		distances = []

		for instance in self.data:
			if username != instance:
				distance = self.euclidian(self.data[instance], self.data[username])

				distances.append((instance, distance))

		distances.sort(key=lambda artistTuple: artistTuple[1], reverse=True)

		return distances

	# dados concentrados
	def pearson(self,rate1, rate2):

		sum_xy = 0
		
		sum_x = 0
		sum_y = 0

		sum_x_2 = 0
		sum_y_2 = 0
		
		n = 0

		for title in rate1:
			if title in rate2:
				sum_xy += rate1[title] * rate2[title]

				sum_x += rate1[title]
				sum_y += rate2[title]
				n += 1.0

				sum_x_2 += rate1[title]**2
				sum_y_2 += rate2[title]**2


		num =  sum_xy - (sum_x*sum_y)/n
		den = sqrt(sum_x_2 - pow(sum_x,2)/n) * sqrt(sum_y_2 - pow(sum_y,2)/n)

		if den == 0:
			return 0
		else:
			return num / den

	# dadsos sparcos
	def cossine(self,rate1, rate2):

		prod_xy = 0
		length_x = 0
		length_y = 0

		for title in rate1:
			length_x += rate1[title]**2
		
		length_x = sqrt(length_x)

		for title in rate2:		
			length_y += rate2[title]**2
		
		length_y = sqrt(length_y)

		for title in rate1:
			if title in rate2:
				prod_xy += rate1[title] * rate2[title]


		if not length_x * length_y == 0:
			return prod_xy / (length_x * length_y)
		else:
			return 0

	def recommend(self, user):
		"""Give list of recommendations"""
		#print nearest
		recomendations = {}
		# first get list of users ordered by nearness
		nearest = self.computeNearestNeighbod(user)
		#
		# now get the ratings for the user
		#
		
		userRatings = self.data[user]		
		# determine the total distance		
		total_distance = 0.0

		for i in range(self.k):
			total_distance += nearest[i][1]

		# now iterate through the k nearest neighbors
 		# accumulating their ratings

		for i in range(self.k):
			# compute slice of pie 
			weight = nearest[i][1] / total_distance
			# get the name of the person
			name = nearest[i][0]			
			# get the ratings for this person
			neighborRatings = self.data[name]
			
			# get the name of the person
 			# now find bands neighbor rated that user didn't

 			for artist in neighborRatings:
 				if not artist in userRatings:
 					if not artist in recomendations:
 						recomendations[artist] = (neighborRatings[artist] * weight)
 					else:
 						recomendations[artist] = (recomendations[artist] +
 												neighborRatings[artist]*weight)

 		# now make list from dictionary

 		recomendations = list(recomendations.items())	
 		recomendations = [(self.convertProductID2Name(k), v)
 		 					for (k,v) in recomendations]

 		# finally sort and return
 		recomendations.sort(key=lambda artistTuple: artistTuple[1],
 		 						reverse = True)

 		# Return the first n items 		 
 		return recomendations[:self.n]

	def computeDeviations(self):
		deviations = {}
		for ratings in self.data.values():
			for (item, rating) in ratings.items():
				self.frequencies.setdefault(item,{})
				self.deviations.setdefault(item,{})
				for (item2, rating2) in ratings.items():
					if item != item2:
						self.frequencies[item].setdefault(item2,0)
						self.deviations[item].setdefault(item2, 0.0)
						self.frequencies[item][item2] += 1
						self.deviations[item][item2] += rating - rating2

		for (item, ratings) in self.deviations.items():
			for item2 in ratings:
				ratings[item2] /= self.frequencies[item][item2]

		return deviations

	def slopeOneRecommendations(self, userRatings):
		recommendations = {}
		frequencies = {}
		# for every item and rating in the user's recommendations
		for (userItem, userRating) in userRatings.items():
		 # for every item in our dataset that the user didn't rate
		 for (diffItem, diffRatings) in self.deviations.items():
		    if diffItem not in userRatings and \
		       userItem in self.deviations[diffItem]:
		       freq = self.frequencies[diffItem][userItem]
		       recommendations.setdefault(diffItem, 0.0)
		       frequencies.setdefault(diffItem, 0)
		       # add to the running sum representing the numerator
		       # of the formula
		       recommendations[diffItem] += (diffRatings[userItem] +
		                                     userRating) * freq
		       # keep a running sum of the frequency of diffitem
		       frequencies[diffItem] += freq
		recommendations =  [(self.convertProductID2name(k),
		                   v / frequencies[k])
		                  for (k, v) in recommendations.items()]
		# finally sort and return
		recommendations.sort(key=lambda artistTuple: artistTuple[1],
		                   reverse = True)
		# I am only going to return the first 50 recommendations
		return recommendations[:50]



'''
2. The book website has a file containing movie
ratings for 25 movies. Create a function that loads
the data into your classifier. The recommend method
described above should recommend movies for a
specific person. 
'''

#=========================================================

def show_pearson():
	print peason(users['Angelica'], users['Bill'])
	print peason(users['Angelica'], users['Hailey'])
	print peason(users['Angelica'], users['Jordyn'])

def recomend_teste():
	r = Recomender(music_rates)
	print r.recommend('Angelica')
	print r.recommend('Chan')
	print r.recommend('Veronica')
	print r.recommend('Bill')
	#r.loadBookBD()
	#r.recommend('171118') 

	#r.userRatings('171118', 5) 

def teste():
	r = Recomender(music_rates)
	#print r.recommend('Angelica')
	#print r.recommend('Chan')
	#print r.recommend('Veronica')
	#print r.recommend('Bill')

	r.loadMovieBD()

	print r.recommend('Bryan')
	print r.recommend('vanessa')
	print r.recommend('Patrick C')
	print ''

	print r.data['Patrick C']
#==========================================================


r = Recommender(users2)
r.computeDeviations()
g = users2['Ben']
print r.slopeOneRecommendations(g)












