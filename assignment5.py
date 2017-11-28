# Assignment 2 - Data Mining
# Tytus Planck and Kyle Rossman
import csv
import math
import sys
import time
import random
start_time = time.time()

# Gets the data from income_tr
def get2DimHardData():
    data = []
    with open('TwoDimHard.csv', 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            dataRow = []
            for item in row:
                dataRow.append(item)
            data.append(dataRow)
        del data[0]
    return data


# Gets the data from income_te
def getWineData():
    teData = []
    with open('wine.csv', 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            dataRow = []
            for item in row:
                dataRow.append(item)
            teData.append(dataRow)
        del teData[0]
    return teData

def printResults(results, name):
    # Outputs the results calculated to a CSV file.
    with open(name, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(results)

def getRandomCentroid(k, dataSet):
    centroids = []
    count = 0
    while (count < k):
        centroids.append(dataSet[random.randint(0, len(dataSet) - 1)])
        count = count + 1
    return centroids

def determineCluster(dataSet, centroids):
    clusterArray = []
    for row in dataSet: #look at each row to find which cluster it belongs too
        count = 0
        closestCentroid = 0
        shortestDistance = 10000 #initialized shortest distance high
        while (count < len(centroids)): #compare each row in dataset to each centroid
            euc = findEuclideanDistanceSet1(centroids[count], row)
            if (euc < shortestDistance):
                shortestDistance = euc
                closestCentroid = count + 1 #marks cluster as count + 1 so it starts at 1
            count = count + 1
        clusterArray.append(closestCentroid)
    return clusterArray

#Believe problem is centroid array only holds a certain
#centroid might not be getting passed correctly
def findEuclideanDistanceSet1(centroid, dataRow):
    count = 0
    print(len(centroid))
    print(len(dataRow))
    if (len(centroid) == 4 and len(dataRow) == 4):
        distance = (float(centroid[1]) - float(dataRow[1]))**2 + (float(centroid[2]) - float(dataRow[2]))**2 
    else:
        distance = 0
        print("Bad length")
    #while (count < len(dataRow) - ):
        # #print(len(dataRow)) #tracker
        # print((dataRow[count]))
        # #print(dataRow[0])
        # distance = distance + (float(centroid[count]) - float(dataRow[count]))**2 # count + 1 to skip header row
        # count = count + 1
    distance = math.sqrt(distance) #this is the eucldean distance bewteen the data point and centroid
    return distance

def adjustCentroids(clusterArray, k, dataSet):
    kCounter = 0
    updatedCentroids = []
    while (kCounter <= k):
        dataCount = 0
        cluster = []
        while (dataCount < len(dataSet)):
            if (kCounter == dataSet[dataCount]):
                cluster.append(dataSet[dataCount])
            dataCount = dataCount + 1
        newCentroid = calculateAverageCentroid(cluster)
        updatedCentroids.append(newCentroid)
        kCounter = kCounter + 1
    return updatedCentroids


def calculateAverageCentroid(cluster):
    count = 0
    newCentroid = []
    while (count < len(cluster)):
        columnAverage = 0
        for row in cluster:
            columnAverage = columnAverage + row[count]
        count = count + 1
        columnAverage = float(columnAverage) / len(cluster)
        newCentroid.append(columnAverage)
    return newCentroid
        
def isCentroidsCorrect(centroids, newCentroids):
    count = 0
    isSame = True
    while (count < len(centroids)):
        if (centroids[count] != newCentroids[count]):
            isSame = False
        count = count + 1
    return isSame


def executeKMeans(k, dataSet):
    centroids = getRandomCentroid(k, dataSet)
    clusterArray = determineCluster(dataSet, centroids)
    newCentroids = adjustCentroids(clusterArray, k, dataSet)
    while (isCentroidsCorrect(centroids, newCentroids) == False):
        centroids = newCentroids
        clusterArray = determineCluster(dataSet, centroids)
        newCentroids = adjustCentroids(clusterArray, k, dataSet)
    
    #need function taht compares new Centroids to old and returns true if they're the same




def main():
    k = int(sys.argv[1])
    twoDimHardData = get2DimHardData()
    wineData = getWineData()
    executeKMeans(k, twoDimHardData)
    #executeKMeans(k, wineData)

    # printResults(combinedMatrix, "combinedwithheader.csv")
    # print("Our program took %s seconds to complete" %
    #       (time.time() - start_time))


if __name__ == "__main__":
    main()
#don't leave your computer open or kenton will text me and  tell me I should write something in your code.