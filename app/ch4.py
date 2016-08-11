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

class Classifier():

   def __init__(self,filename):
      self.medianAndDeviation = []
        
      # reading the data in from the file
      f = open(filename)
      lines = f.readlines()
      f.close()
      self.format = lines[0].strip().split('\t')
      self.data = []
      for line in lines[1:]:
         fields = line.strip().split('\t')
         ignore = []
         vector = []
         for i in range(len(fields)):
            if self.format[i] == 'num':
               vector.append(int(fields[i]))
            elif self.format[i] == 'comment':
               ignore.append(fields[i])
            elif self.format[i] == 'class':
              classification = fields[i]
         self.data.append((classification, vector, ignore))
      self.rawData = list(self.data)
      # get length of instance vector
      self.vlen = len(self.data[0][1])
      # now normalize the data
      for i in range(self.vlen):
         self.normalizeColumn(i)
   

   def euclidian(self,rate1, rate2):
      distcance = 0
      for mood in rate1:
         distcance += (rate2[mood] - rate1[mood])**2

      return sqrt(distcance)

   def manhattam(self,rate1, rate2):
      distcance = 0
      for mood in rate1:
         distcance += abs(rate2[mood] - rate1[mood])

      return distcance

   def computeNearestNeighbor(self,music,musics):
      distances = []
      for item in musics:
         if item != music:
            d = manhattam(musics[item],musics[music])
            distances.append((item,d))

      distances.sort(key=lambda musicTuple: musicTuple[1], reverse=False)

      return distances

   def standardScore(self,musics):
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

   def disctionary_to_vector(self,musics):
      music_list = {}
      for item in musics:
         music_list[item] = []
         for item2 in musics[item]:
            music_list[item].append(musics[item][item2])

      return music_list

   def modifiedStardScore(self,musics):
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

   def getMedian(self,values):     

      if len(values) == 0:
         return 0

      if len(values) == 1:
         return values[0]

      values.sort()

      i = len(values)/2
      if len(values) % 2 == 0:      
         return (values[i-1] + values[i])*0.5
      else:
         return values[i]

   def asd(self,values):
      soma = 0
      median = self.getMedian(values)
      for item in values:
         soma += abs(item - median)

      return soma/float(len(values))

   def medianAndDeviation(self):

      median = self.getMedian(self.data[1][1])
      deviation = self.asd(self.data[1][1])

      return (median,deviation)

   def teste_recommending(self):
      normalize(musics)
      print ''

      recommendings = computeNearestNeighbor('Phoenix/Lisztomania', musics)

      for item in recommendings:
         print item

   def test_modifiedScore(self, s):  

      for i in s:
         asd = absoluteStandardDeviation(s)
         median = getMedian(s)
         score = (i - median)/float(asd)
         print score

   def loadData(self):
      f = open('../data_sources/ch4/athletesTrainingSet.txt','r')
      lines = f.readlines()
      f.close()
      data = []
      for i in range(len(lines)):
         if not i == 0:

            line = lines[i].strip().split('\t')

            values = [float(line[2]),float(line[3])]
            name = line[0]
            classe = line[1]

            data.append((classe,values,name))
      self.data = data

      return data

   def normalizeColumn(self,colum_Number):
      col = [v[1][colum_Number] for v in self.data]

      median = self.getMedian(col)
      asd = self.asd(col)

      for v in self.data:
         v[1][colum_Number] = (v[1][colum_Number] - median)/asd

   def normalizeVector(self, v):
      """We have stored the median and asd for each column.
      We now use them to normalize vector v"""
      vector = list(v)
      for i in range(len(vector)):
         (median, asd) = self.medianAndDeviation[i]
         vector[i] = (vector[i] - median) / asd
      return vector
        
   def manhattan(self, vector1, vector2):
      """Computes the Manhattan distance."""
      return sum(map(lambda v1, v2: abs(v1 - v2), vector1, vector2))

   def nearestNeighbor(self, itemVector):
      """return nearest neighbor to itemVector"""

      return min([(self.manhattan(itemVector, item[1]), item)
                  for item in self.data])

   def classify(self, itemVector):
      """Return class we think item Vector is in"""
      return (self.nearestNeighbor(self.normalizeVector(itemVector))[1][0])





heights = [54, 72, 78, 49, 65, 63, 75, 67, 54]

def unitTest():
   classifer = Classifier()
   m1 = classifer.getMedian(heights)
   assert(round(m1,3) == 65)

   print "getMedian and getAbsoluteStandardDeviation work correctly"

def teste3():
   unitTest()

   classifier = Classifier()

   classifier.loadData()
   classifier.normalize_data(1)

   for line in classifier.data:
      print line

def unitTest():

    classifier = Classifier('../data_sources/ch4/athletesTrainingSet.txt')
    br = ('Basketball', [72, 162], ['Brittainey Raven'])
    nl = ('Gymnastics', [61, 76], ['Viktoria Komova'])
    cl = ("Basketball", [74, 190], ['Crystal Langhorne'])
    # first check normalize function
    brNorm = classifier.normalizeVector(br[1])
    nlNorm = classifier.normalizeVector(nl[1])
    clNorm = classifier.normalizeVector(cl[1])
    assert(brNorm == classifier.data[1][1])
    assert(nlNorm == classifier.data[-1][1])
    print('normalizeVector fn OK')
    # check distance
    assert (round(classifier.manhattan(clNorm, classifier.data[1][1]), 5) == 1.16823)
    assert(classifier.manhattan(brNorm, classifier.data[1][1]) == 0)
    assert(classifier.manhattan(nlNorm, classifier.data[-1][1]) == 0)
    print('Manhattan distance fn OK')
    # Brittainey Raven's nearest neighbor should be herself
    result = classifier.nearestNeighbor(brNorm)
    assert(result[1][2]== br[2])
    # Nastia Liukin's nearest neighbor should be herself
    result = classifier.nearestNeighbor(nlNorm)
    assert(result[1][2]== nl[2])
    # Crystal Langhorne's nearest neighbor is Jennifer Lacy"
    assert(classifier.nearestNeighbor(clNorm)[1][2][0] == "Jennifer Lacy")
    print("Nearest Neighbor fn OK")
    # Check if classify correctly identifies sports
    assert(classifier.classify(br[1]) == 'Basketball')
    assert(classifier.classify(cl[1]) == 'Basketball')
    assert(classifier.classify(nl[1]) == 'Gymnastics')
    print('Classify fn OK')

unitTest()
    








