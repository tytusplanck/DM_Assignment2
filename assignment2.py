# Assignment 2 - Data Mining
# Tytus Planck and Kyle Rossman
import csv
import math
import sys
import time
start_time = time.time()


# Manages the entire posterior matrix that compares each TE row to our training set.
def createProximityTEMatrix(trData, teData, k):
    index = 1
    combinedApproximationMatrix = []
    combinedMatrix = trData[:]
    combinedMatrix += teData[:]
    printResults(combinedMatrix, "combinedwithheader.csv")
    # printResults(combinedMatrix, "combined_matrix.csv")
    while index < len(combinedMatrix):
        combinedApproximationMatrix.append(
            approximateOneInstance(combinedMatrix, index))
        index = index + 1
    resultApproximationMatrix = getFormattedCombinedResultsRow(
        combinedApproximationMatrix, k)
    printResults(resultApproximationMatrix, "formatted_rows.csv")
    return combinedApproximationMatrix


# Gets the data from income_tr
def getTRCSVData():
    data = []
    with open('income_tr.csv', 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            dataRow = []
            for item in row:
                dataRow.append(item)
            data.append(dataRow)
    return data


# Gets the data from income_te
def getTECSVData():
    teData = []
    with open('income_te.csv', 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            dataRow = []
            for item in row:
                dataRow.append(item)
            teData.append(dataRow)
    return teData


# Function Definition for generateApproximationMatrix
def generateApproximationMatrix(k, data):
    # This calls the function that will find all approximations for one instance. It loops this so it can have an array of approximations for all instances.
    index = 1
    approximationMatrix = []
    resultsMatrix = []
    while index < len(data):
        approximationMatrix.append(approximateOneInstance(data, index))
        index = index + 1
    return approximationMatrix  # returns array of approximations for each


# Takes one instance and finds all of the approximations to the other instances
def approximateOneInstance(data, index):
    instanceIndex = 1
    # Array of 520 floats containing the approximation to current instance for each object.
    approximationArray = []
    while instanceIndex < len(data):
        approximationArray.append(findRowApproximation(
            data[instanceIndex], data[index]))
        instanceIndex = instanceIndex + 1
    # Returns an array of the approximation of each instance to the current one
    return approximationArray


# Function Definition for findRowApproximation
def findRowApproximation(row1, row2):
    # Takes one row of the table and finds it's approximation to the other.
    smc = getSMCProximity(row1, row2)
    euc = getEuclidianProximation(row1, row2)
    jac = getJaccardProximation(row1, row2)
    totalApproximation = ((7 * smc) + (4 * euc) + (2 * jac)) / 13.0
    return totalApproximation


def getSMCProximity(row1, row2):
    match = 0.0
    total = 0.0
    # Finds match and total values for SMC algorithm
    if (row1[2] == row2[2]):
        match = match + 1
        total = total + 1
    else:
        total = total + 1
    if (row1[4] == row2[4]):
        match = match + 1
        total = total + 1
    else:
        total = total + 1
    if (row1[6] == row2[6]):
        match = match + 1
        total = total + 1
    else:
        total = total + 1
    if (row1[7] == row2[7]):
        match = match + 1
        total = total + 1
    else:
        total = total + 1
    if (row1[8] == row2[8]):
        match = match + 1
        total = total + 1
    else:
        total = total + 1
    if (row1[9] == row2[9]):
        match = match + 1
        total = total + 1
    else:
        total = total + 1
    if (row1[10] == row2[10]):
        match = match + 1
        total = total + 1
    else:
        total = total + 1
    if (row1[14] == row2[14]):
        match = match + 1
        total = total + 1
    else:
        total = total + 1

    return 1 - (match / total)  # Calculates the SMC Proximation


# Function Definition for getEuclidianProximation
def getEuclidianProximation(row1, row2):
    fnlwgt98 = 378460.0  # This is the 98th percentile value for the fnlwgt attribute
    weeklyHours98 = 60.0  # This is the 98th percentile value for the hours per week attribute
    # These two attributes have outliers, so dividing the data set by the maximum can make things appear closer in proximity then they actually are if we sue an outlier.

    euc = ((float(row1[1]) / 82.0) - (float(row2[1]) / 82.0))**2 + ((float(row1[3]) / fnlwgt98) - (float(row2[3]) / fnlwgt98))**2 + (
        (float(row1[5]) / 16.0) - (float(row2[5]) / 16.0))**2 + ((float(row1[13]) / weeklyHours98) - (float(row2[13]) / weeklyHours98))**2
    return math.sqrt(euc)


def getJaccardProximation(row1, row2):
    # Finds the Jaccard Proximation by adding up the matches for the 2x2 matrix.
    M01 = 0
    M10 = 0
    M11 = 0
    if(int(row1[11]) >= 1 and int(row2[11]) == 0):
        M10 += 1
    if(int(row1[12]) >= 1 and int(row2[12]) == 0):
        M10 += 1
    if(int(row1[11]) == 0 and int(row2[11]) >= 1):
        M01 += 1
    if(int(row1[12]) == 0 and int(row2[12]) >= 1):
        M01 += 1
    if(int(row1[11]) == int(row2[11]) and int(row1[11]) >= 1):
        M11 += 1
    if(int(row1[12]) == int(row2[12]) and int(row1[12]) >= 1):
        M11 += 1

    jaccard = 0
    if (M01 + M10 + M11) != 0:
        jaccard = M11 / (M01 + M10 + M11)

    return jaccard


def getFormattedCombinedResultsRow(approximationMatrix, k):
    results = []
    outerCounter = 0
    while outerCounter < len(approximationMatrix):
        sortedRow = approximationMatrix[outerCounter][:]
        sortedRow.sort()
        IDList = []
        counter = 0
        while len(IDList) < k:
            x = 0
            while x < len(sortedRow):  # has the proximities but nothing else
                # has to compare proximity to each column and returns the position in array wants it find a match
                if sortedRow[counter] == approximationMatrix[outerCounter][x] and x < 520:
                    IDList.append(x)
                x = x + 1
            counter = counter + 1
        y = 0
        singleResultsRow = [outerCounter + 1]
        while y < len(IDList):
            # adds one to take into account the header row. Is appending the ID
            singleResultsRow.append(IDList[y] + 1)
            y = y + 1
        # appends that array into the array of arrays
        results.append(singleResultsRow)
        outerCounter = outerCounter + 1
    return results


def getTEMatrix(rowIndex, formattedProximityMatrix, combinedMatrix, k):
    teMatrix = []
    x = 0
    while x < k:

    printResults(teMatrix, "teMatrix.csv")
    return teMatrix


def printResults(results, name):
    # Outputs the results calculated to a CSV file.
    with open(name, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(results)


def main():
    k = int(sys.argv[1])
    trData = getTRCSVData()
    teData = getTECSVData()
    generateApproximationMatrix(k, trData)
    createProximityTEMatrix(trData, teData[1:], k)
    print("Our program took %s seconds to complete" %
          (time.time() - start_time))


if __name__ == "__main__":
    main()
