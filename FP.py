import mysql.connector
import math
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

factoryStopwordRemover = StopWordRemoverFactory()
stopword = factoryStopwordRemover.create_stop_word_remover()

factory = StemmerFactory()
stemmer = factory.create_stemmer()


class DBConnector:
    def __init__(self, user, passw, hostIp, dbname):
        self.connection = mysql.connector.connect(user=user, password=passw,
                                                  host=hostIp,
                                                  database=dbname)
        self.cursor = self.connection.cursor(dictionary=True)

    def execute(self, queryString, params=()):
        self.cursor.execute(queryString, params)
        return self.cursor.fetchall()


DB = DBConnector('root', '', '127.0.0.1', 'keluhan')
statement = "SELECT DISTINCT * FROM `keluhan` WHERE created_at BETWEEN '2017-08-01' AND '2017-08-31'"
result = DB.execute(statement)
document = []hah
totalDocumentOfTerm = {}
listKeluhan = []

idx = 0
for row in result:
    keluhan = row['keluhan'].encode('utf-8')
    listKeluhan.append(keluhan)
    stemmedKeluhan = stemmer.stem(keluhan)
    stemmedKeluhan = stopword.remove(stemmedKeluhan)
    listToken = stemmedKeluhan.split()

    dictOfTerm = {}
    for token in listToken:
        token = token.lower()
        token = token.strip(',.@?!_-"()')

        if token not in dictOfTerm:
            dictOfTerm[token] = 1
            if token not in totalDocumentOfTerm:
                totalDocumentOfTerm[token] = 1
            else:
                totalDocumentOfTerm[token] += 1
        else:
            dictOfTerm[token] += 1

    document.append(dictOfTerm)
    idx += 1
#normalisasi term dari setiap document
#menghitung TF (term frequency)
termFrequencyOfDocument = document
higherScoreTerm = ['jln', 'e-ktp', 'ektp', 'pelatihan', 'hujan','srt', 'pju', 'akte', 'gratis', 'reklame', 'rambu', 'lintas', 'surat', 'sampah', 'pdam', 'listrik', 'e-ktp', 'limbah', 'penerangan', 'lampu', 'limbah', 'banjir', 'jalan', 'hujan']

print "total = " + str(len(document))

idx=0
for terms in document:
    totalTerm = 0
    for term in terms:
        totalTerm += terms[term]
    for term in terms:
        termValue = document[idx][term]
        if (term in higherScoreTerm) :
            termValue += 10
        termFrequencyOfDocument[idx][term] = float(termValue) / float(totalTerm)
    print termFrequencyOfDocument[idx]
    idx+=1
# menghitung inverse document frequency (IDF)

inverseDocumentFrequencyOfDocument = totalDocumentOfTerm

for term in inverseDocumentFrequencyOfDocument:
    inverseDocumentFrequencyOfDocument[term] = 1 + math.log(float(len(document)) / float(totalDocumentOfTerm[term]))

print inverseDocumentFrequencyOfDocument
#menghitung TF-IDF

tfIdf = document

idx=0
for terms in document:
    totalTerm = 0
    for term in terms:
        totalTerm += terms[term]
    for term in terms:
        TF = termFrequencyOfDocument[idx][term]
        IDF = inverseDocumentFrequencyOfDocument[term]
        tfIdf[idx][term] = float(TF) * float(IDF)
    print tfIdf[idx]
    idx+=1

def generateCombinedTermList(idx1, idx2):
    combinedTerm = []
    for term in termFrequencyOfDocument[idx1]:
        if term not in combinedTerm:
            combinedTerm.append(term)
    for term in termFrequencyOfDocument[idx2]:
        if term not in combinedTerm:
            combinedTerm.append(term)
    return combinedTerm
# mencoba gabung term doc 1 dan 2

generateCombinedTermList(0,1)


def generateDotProduct(idx1, idx2):
    termList = generateCombinedTermList(idx1, idx2)
    total = 0
    for term in termList:
        document1 = 0
        document2 = 0

        if term in tfIdf[idx1]:
            document1 = tfIdf[idx1][term]
        if term in tfIdf[idx2]:
            document2 = tfIdf[idx2][term]

        total += float(document1) * float(document2)

    return total


def generateLenght(idx1, idx2):
    termList = generateCombinedTermList(idx1, idx2)
    total1 = 0
    total2 = 0

    for term in termList:
        if term in tfIdf[idx1]:
            total1 += tfIdf[idx1][term] * tfIdf[idx1][term]
        if term in tfIdf[idx2]:
            total2 += tfIdf[idx2][term] * tfIdf[idx2][term]
    return math.sqrt(total1) * math.sqrt(total2)


class SimiliarityDocument:
    value = 0.0
    idxA = -1
    idxB = -1

    def __init__(self, value, idxA, idxB):
        self.value = value
        self.idxA = idxA
        self.idxB = idxB


def findSimilarity(idx1, idx2):
    try:
        similarity = float(generateDotProduct(idx1, idx2)) / float(generateLenght(idx1, idx2))
    except:
        similarity = 0
    return similarity

findSimilarity(1, 5)
listMemberByCluster = {}
currIdx = 0
for docIdx in range(0, len(document)):
    highestAvg = 0
    highestClusterIdx = 0

    for key in listMemberByCluster:
        avg = 0
        for idxMember in listMemberByCluster[key]:
            avg = max(avg, findSimilarity(docIdx, idxMember))

        if (avg > highestAvg):
            highestAvg = avg
            highestClusterIdx = key

    if (highestAvg > 1):
        listMemberByCluster[highestClusterIdx].append(docIdx)
    else:
        listMemberByCluster[currIdx] = [docIdx]
        currIdx += 1

listMemberByCluster
totalNotListed = 0
totalListed = 0

totalAcc = 0
totalCluster = 0
for key in listMemberByCluster:
    totalListed += 1
    listMember = listMemberByCluster[key]

    countCommonTerm = {}
    for member in listMember:
        # print '>', listKeluhan[member], '\n'
        for keyTerm in termFrequencyOfDocument[member]:
            if keyTerm not in countCommonTerm:
                if (keyTerm in higherScoreTerm):
                    countCommonTerm[keyTerm] = 1
            else:
                if (keyTerm in higherScoreTerm):
                    countCommonTerm[keyTerm] += 1

    countCommonTerm = sorted(countCommonTerm.items(), key=lambda x: x[1], reverse=True)
    lenTopic = len(countCommonTerm)
    if (lenTopic > 0):
        mainTopic = countCommonTerm[0]
        sumWrongTopic = 0
        for i in range(1, lenTopic):
            sumWrongTopic += countCommonTerm[i][1]
        totalData = mainTopic[1] + sumWrongTopic
        accuracy = float(mainTopic[1]) / (totalData) * 100

        print "============================================="
        print "CLUSTER ", key

        print "ACC = " + str(accuracy) + "%"
        print "TOTAL DATA = " + str(totalData)
        print "MAIN TOPIC = " + mainTopic[0]
        totalCluster += 1
        totalAcc += accuracy
    else:
        # print "NOT LISTED IN TOPIC"
        totalNotListed += 1

print "vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv"
print "MISS TOPIC = " + str(totalNotListed)
print "TOTAL = " + str(totalListed)
print "AVG ACC = " + str(float(totalAcc) / float(totalCluster))
print "TOTAL VALID CLUSTER = " + str(totalCluster)
print "MISS RATE = " + str(float(totalNotListed) / float(totalListed) * 100) + "%"
print "PRECISION = " + str()
