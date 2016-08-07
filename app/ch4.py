users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
         "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
         "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5, "Slightly Stoopid": 1.0},
         "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},
         "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0, "Vampire Weekend": 1.0},
         "Jordyn":  {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 4.0},
         "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0, "Slightly Stoopid": 4.0, "The Strokes": 5.0},
         "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5, "The Strokes": 3.0}
        }

musics = {"Dr Dog/Fate": {"piano": 2.5, "vocals": 4, "beat": 3.5, "blues": 3, "guitar": 5, "backup vocals": 4, "rap": 1},
         "Phoenix/Lisztomania": {"piano": 2, "vocals": 5, "beat": 5, "blues": 3, "guitar": 2, "backup vocals": 1, "rap": 1},
         "Heartless Bastards/Out at Sea": {"piano": 1, "vocals": 5, "beat": 4, "blues": 2, "guitar": 4, "backup vocals": 1, "rap": 1},
         "Todd Snider/Don't Tempt Me": {"piano": 4, "vocals": 5, "beat": 4, "blues": 4, "guitar": 1, "backup vocals": 5, "rap": 1},
         "The Black Keys/Magic Potion": {"piano": 1, "vocals": 4, "beat": 5, "blues": 3.5, "guitar": 5, "backup vocals": 1, "rap": 1},
         "Glee Cast/Jessie's Girl": {"piano": 1, "vocals": 5, "beat": 3.5, "blues": 3, "guitar":4, "backup vocals": 5, "rap": 1},
         "La Roux/Bulletproof": {"piano": 5, "vocals": 5, "beat": 4, "blues": 2, "guitar": 1, "backup vocals": 1, "rap": 1},
         "Mike Posner": {"piano": 2.5, "vocals": 4, "beat": 4, "blues": 1, "guitar": 1, "backup vocals": 1, "rap": 1},
         "Black Eyed Peas/Rock That Body": {"piano": 2, "vocals": 5, "beat": 5, "blues": 1, "guitar": 2, "backup vocals": 2, "rap": 4},
         "Lady Gaga/Alejandro": {"piano": 1, "vocals": 5, "beat": 3, "blues": 2, "guitar": 1, "backup vocals": 2, "rap": 1}}

from math import sqrt

from numpy import array

def euclidian(rate1, rate2):
   distcance = 0
   for mood in rate1:
      distcance += (rate2[mood] - rate1[mood])**2

   return sqrt(distcance)

def manhattam(rate1, rate2):
   distcance = 0
   for mood in rate1:
      distcance += abs(rate2[mood] - rate1[mood])

   return distcance

def computeNearestNeighbor(music,musics):
   distances = []
   for item in musics:
      if item != music:
         d = manhattam(musics[item],musics[music])
         distances.append((item,d))

   distances.sort(key=lambda musicTuple: musicTuple[1], reverse=False)

   return distances

def standardScore(musics):
   new_musics = {}  

   dim = {}
   for item in musics:
      for item2 in musics[item]:
         if item2 in dim:
            dim[item2].append(musics[item][item2])
         else:
            dim[item2] = []         

   for item in musics:
      new_item = {}
      for aspect in musics[item]:
         maximum = max(dim[aspect])
         minimum = min(dim[aspect])
         norm_value = (musics[item][aspect] - minimum)/float(maximum-minimum)
         new_item.setdefault(aspect,norm_value)

      new_musics.setdefault(item,new_item)

   return new_musics

def disctionary_to_vector(musics):
   music_list = {}
   for item in musics:
      music_list[item] = []
      for item2 in musics[item]:
         music_list[item].append(musics[item][item2])

   return music_list



def modifiedStardScore(musics):
   new_musics = {}
   
   dim = {}
   for item in musics:
      for item2 in musics[item]:
         if item2 in dim:
            dim[item2].append(musics[item][item2])
         else:
            dim[item2] = []         

   for item in musics:
      new_item = {}
      for aspect in musics[item]:

         median = getMedian(dim[aspect])
         asd = absoluteStardDeviation(dim[aspect]);         
         socore = (musics[item][aspect] - median)/float(asd)
         
         new_item.setdefault(aspect,norm_value)

      new_musics.setdefault(item,new_item)

   return new_musics

def getMedian(values):

   if len(values) == 0:
      return 0

   if len(values) == 1:
      return values[0]

   i = len(values)/2
   if len(values) % 2 == 0:      
      return (values[i-1] + values[i])*0.5
   else:
      return values[i]

def absoluteStandardDeviation(values):
   soma = 0
   median = getMedian(values)
   for item in values:
      soma += abs(item - median)

   return soma/float(len(values))


def teste_recommending():
   normalize(musics)
   print ''

   recommendings = computeNearestNeighbor('Phoenix/Lisztomania', musics)

   for item in recommendings:
      print item

def test_modifiedScore():
   s = [21,15,12,3,7]

   for i in s:
      asd = absoluteStandardDeviation(s)
      median = getMedian(s)
      score = (i - median)/float(asd)
      print score


standardScore2(musics)








