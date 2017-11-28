# Assignment 2 - Data Mining
# Tytus Planck and Kyle Rossman
import csv
import math
import sys
import time
import random
start_time = time.time()

# Gets the data from income_tr
def getData():
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


def printResults(results, name):
    # Outputs the results calculated to a CSV file.
    with open(name, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(results)

#Can use for both
def getRandomCentroid(k, dataSet):
    centroids = []
    count = 0
    while (count < k):
        centroids.append(dataSet[random.randint(0, len(dataSet) - 1)])
        count = count + 1
    return centroids

#Need Separate call for Algorithm 2
def determineCluster(dataSet, centroids):
    clusterArray = []
    for row in dataSet: #look at each row to find which cluster it belongs too
        count = 0
        closestCentroid = 0
        shortestDistance = 10000 #initialized shortest distance high
        while (count < len(centroids)): #compare each row in dataset to each centroid
            #print((centroids[count])) #problem is centroids are empty
            lam = 0.3
            euc = findEuclideanDistanceSet1(centroids[count], row)
            modes = findKModes(centroids[count], row)
            totalClusterDist = euc + modes * lam #lam is the lambda value for our K-Prototype equation to balance out weight of categorical attributes
            if (totalClusterDist < shortestDistance):
                shortestDistance = totalClusterDist
                closestCentroid = count + 1 #marks cluster as count + 1 so it starts at 1
            count = count + 1
        clusterArray.append(closestCentroid)
    return clusterArray

#Need Separate call for algorithm 2 
def findEuclideanDistanceSet1(centroid, dataRow):
    distance = (float(centroid[1]) - float(dataRow[1]))**2 + (float(centroid[2]) - float(dataRow[2]))**2 
    distance = math.sqrt(distance) #this is the eucldean distance bewteen the data point and centroid
    return distance

def findKModes(centroid, dataRow):
    total = 0
    if (centroid[2] == dataRow[2]):
        total = total + 1
    if (centroid[4] == dataRow[4]):
        total = total + 1
    return total

#need separate call for algorithm 2 -- calls calculateAverageCentroid
def adjustCentroids(clusterArray, k, dataSet): #believe this works correctly now
    kCounter = 1
    updatedCentroids = []
    #print(clusterArray)
    while (kCounter <= k):
        dataCount = 0
        cluster = []
        while (dataCount < len(dataSet)): 
            if (kCounter == clusterArray[dataCount]):
                cluster.append(dataSet[dataCount])
            dataCount = dataCount + 1
        if (len(cluster) > 1):
            newCentroid = calculateAverageCentroid(cluster)
            #print(newCentroid)
            updatedCentroids.append(newCentroid)
        kCounter = kCounter + 1
    return updatedCentroids

#need separate function
def calculateAverageCentroid(cluster):
    count = 0
    newCentroid = []
    newCentroid.append(0) #this is so that the new centroid matches the same list size as the rows
    #while (count < len(cluster)):
    columnAverage1 = 0
    for row in cluster:
        columnAverage1 = columnAverage1 + float(row[1])
    count = count + 1
    columnAverage1 = float(columnAverage1) / float(len(cluster))
    newCentroid.append(columnAverage1)
     
    columnAverage2 = 0
    for row in cluster:
        columnAverage2 = columnAverage2 + float(row[2])
    count = count + 1
    columnAverage2 = float(columnAverage2) / float(len(cluster))
    newCentroid.append(columnAverage2)
    newCentroid.append(0) #so that averaged centroid matches row in dataset

    return newCentroid

#Can use for both
def isCentroidsCorrect(centroids, newCentroids):
    count = 0
    isSame = True
    #print(centroids)
    while (count < len(centroids)):
        if (centroids[count] != newCentroids[count]):
            isSame = False
        count = count + 1
    return isSame

#Needs separate for calls
def executeKMeans(k, dataSet):
    centroids = getRandomCentroid(k, dataSet)
    clusterArray = determineCluster(dataSet, centroids) 
    newCentroids = adjustCentroids(clusterArray, k, dataSet) 
    while (isCentroidsCorrect(centroids, newCentroids) == False):
        centroids = newCentroids
        clusterArray = determineCluster(dataSet, centroids)
        newCentroids = adjustCentroids(clusterArray, k, dataSet)
    prepData(clusterArray)

#Can use for both ---JK u suck kyle
def prepData(clusterArray):
    arr = []
    count = 0
    arr.append(["ID", "Cluster"])
    while (count < len(clusterArray)):
        row = []
        row.append(count)
        row.append(clusterArray[count])
        arr.append(row)
        count = count + 1
    if (len(clusterArray) < 500):
        printResults(arr, "Dim2HardOutput.csv")
    else:
        printResults(arr, "wineOutput.csv")

def normalizeOahu(wineData):
    count = 0
    totalNormalizedSet = []
    for row in wineData:
        normalizedSet = []
        normalizedSet.append(row[0])
        normalizedSet.append(row[1])
        normalizedSet.append(row[2])
        normalizedSet.append(row[3])
        normalizedSet.append(row[4])
        normalizedSet.append(row[5])
        normalizedSet.append(float(row[6]) / 5.0 )
        normalizedSet.append(float(row[7]) / 5.0 )
        normalizedSet.append(float(row[8]) / 4.0)
        normalizedSet.append(float(row[9]) / 688.95 )
        normalizedSet.append(float(row[10]) / 7.0 )
        normalizedSet.append(float(row[11]) / 21.7 )
        normalizedSet.append((float(row[12]) - 21.25633) / (21.703755 - 21.25633))
        normalizedSet.append((float(row[13]) + 158.260712) / (158.260712 - 157.838787))

        totalNormalizedSet.append(normalizedSet)
    return totalNormalizedSet 


#Need Separate call for Algorithm 2
# def determineClusterWine(dataSet, centroids):
#     clusterArray = []
#     for row in dataSet: #look at each row to find which cluster it belongs too
#         count = 0
#         closestCentroid = 0
#         shortestDistance = 10000 #initialized shortest distance high
#         while (count < len(centroids)): #compare each row in dataset to each centroid
#             euc = findEuclideanDistanceSet2(centroids[count], row)
#             if (euc < shortestDistance):
#                 shortestDistance = euc
#                 closestCentroid = count + 1 #marks cluster as count + 1 so it starts at 1
#             count = count + 1
#         clusterArray.append(closestCentroid)
#     return clusterArray

#Needs separate for calls
# def executeKMeansWine(k, dataSet):
#     centroids = getRandomCentroid(k, dataSet)
#     #print(centroids)
#     clusterArray = determineClusterWine(dataSet, centroids) #this first clusterArray works
#     newCentroids = adjustCentroidsWine(clusterArray, k, dataSet) #adjustCentroids is fucked ---update might not be fucked
#     #print(newCentroids)
#     #print(newCentroids)
#     while (isCentroidsCorrect(centroids, newCentroids) == False):
#         centroids = newCentroids
#         clusterArray = determineClusterWine(dataSet, centroids)
#         newCentroids = adjustCentroidsWine(clusterArray, k, dataSet)
#     prepData(clusterArray)


# def calculateAverageCentroidWine(cluster):
#     count = 1
#     newCentroid = []
#     newCentroid.append(0) #this is so that the new centroid matches the same list size as the rows
#     while (count <= 10):
#         columnAverage1 = 0
#         for row in cluster:
#             columnAverage1 = columnAverage1 + float(row[count])
#         count = count + 1
#         columnAverage1 = float(columnAverage1) / float(len(cluster))
#         newCentroid.append(columnAverage1) 

#     newCentroid.append(0) #so that averaged centroid matches row in dataset
#     newCentroid.append("string")
#     return newCentroid 

# def adjustCentroidsWine(clusterArray, k, dataSet): #believe this works correctly now
#     kCounter = 1
#     updatedCentroids = []
#     #print(clusterArray)
#     while (kCounter <= k):
#         dataCount = 0
#         cluster = []
#         while (dataCount < len(dataSet)): 
#             #print("Trying to find cluster match")
#             #print(kCounter)
#             #print(clusterArray[dataCount])
#             if (kCounter == clusterArray[dataCount]):
#                 cluster.append(dataSet[dataCount])
#                 #print("Yo we made it fam")
#             dataCount = dataCount + 1
#         #print(cluster)
#         if (len(cluster) > 1):
#             newCentroid = calculateAverageCentroidWine(cluster)
#             #print(newCentroid)
#             updatedCentroids.append(newCentroid)
#         kCounter = kCounter + 1
#     return updatedCentroids

# def findEuclideanDistanceSet2(centroid, dataRow):
#     distance = (float(centroid[1]) - float(dataRow[1]))**2 + (float(centroid[2]) - float(dataRow[2]))**2 + (float(centroid[3]) - float(dataRow[3]))**2 + (float(centroid[4]) - float(dataRow[4]))**2 + (float(centroid[5]) - float(dataRow[5]))**2 + (float(centroid[6]) - float(dataRow[6]))**2 + (float(centroid[7]) - float(dataRow[7]))**2 + (float(centroid[8]) - float(dataRow[8]))**2 + (float(centroid[9]) - float(dataRow[9]))**2 + (float(centroid[10]) - float(dataRow[10]))**2 + (float(centroid[11]) - float(dataRow[11]))**2
#     distance = math.sqrt(distance) #this is the eucldean distance bewteen the data point and centroid
#     return distance


# Gets the data from income_te
# def getWineData():
#     teData = []
#     with open('wine.csv', 'rb') as csvfile:
#         csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
#         for row in csvreader:
#             dataRow = []
#             for item in row:
#                 dataRow.append(item)
#             teData.append(dataRow)
#         del teData[0]
#     return teData

def main():
    k = int(sys.argv[1])
    data = getData()
    #data = getWineData()
    data = normalizeOahu(data)
    executeKMeans(k, data)
    #executeKMeans(k, wineData)

if __name__ == "__main__":
    main()

