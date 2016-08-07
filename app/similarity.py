#!/usr/bin/env python

from math import sqrt

users3 = {"David": {"Imagine Dragons": 3, "Daft Punk": 5,
			"Lorde": 4, "Fall Out Boy": 1},
		"Matt": {"Imagine Dragons": 3, "Daft Punk": 4,
			"Lorde": 4, "Fall Out Boy": 1},
		"Ben":  {"Kacey Musgraves": 4, "Imagine Dragons": 3,
			"Lorde": 3, "Fall Out Boy": 1},
		"Chris": {"Kacey Musgraves": 4, "Imagine Dragons": 4,
			"Daft Punk": 4, "Lorde": 3, "Fall Out Boy": 1},
		"Tori": {"Kacey Musgraves": 5, "Imagine Dragons": 4,
			"Daft Punk": 5, "Fall Out Boy": 3}}

users2 = {"Amy": {"Taylor Swift": 4, "PSY": 3, "Whitney Houston": 4},
		  "Ben": {"Taylor Swift": 5, "PSY": 2},
          "Clara": {"PSY": 3.5, "Whitney Houston": 4},
          "Daisy": {"Taylor Swift": 5, "Whitney Houston": 3}}

'''
	 cossine similarity, it is indicated when differente people use differents pattern of ratings
	 and when the ratings are sparces 
	 it is known as model-based
'''
def compute_similarity(band1, band2, user_ratings):
	avarages = {}	

	for (key, ratings) in user_ratings.items():
		avarages[key] = (float(sum(ratings.values()) 
						/ len(ratings.values())))
	num = 0.0
	den1 = 0.0
	den2 = 0.0
	for (user, ratings) in user_ratings.items():
		if band1 in ratings and band2 in ratings:
			avg = avarages[user]
			num += (ratings[band1] - avg)*(ratings[band2] - avg)
			den1 += (ratings[band1] - avg)**2
			den2 += (ratings[band2] - avg)**2
	return num /(sqrt(den1) *sqrt(den2))

# normalize the ratings for a scale of -1 to 1
def normalize(r):
	min_r = 1.0
	max_r = 5.0

	num = 2*(r - min_r)-(max_r - min_r)
	den = max_r - min_r

	return num / den

def denormalize(nr):
	min_r = 1.0
	max_r = 5.0

	return 0.5*((max_r - min_r)*(nr+1)) + min_r

def deviation(artist1,artist2):
	N = 0.0
	dev = 0.0
	for user in users3:
		if artist1 in users3[user] and artist2 in users3[user]:
			dev += (users3[user][artist1] - users3[user][artist2])
			N += 1

	if N == 0:
		return 0
	else:		
		return dev/ N


def compute_deviations(self):
	deviations = {}
	for ratings in self.data.values():
		for (item, rating) in ratings.items():
			self.frequency.setdefault(item,{})
			self.deviations.setdefault(item,{})
	




print 'deviation: ' + str(deviation("Imagine Dragons", "Lorde"))

print compute_similarity("Imagine Dragons","Daft Punk",users3)
print compute_similarity("Lorde","Fall Out Boy",users3)
print ''

ratings = users3['David']
for key in ratings:
	print key + ": " + str(ratings[key]) + " " + str(normalize(ratings[key]))







