from flask import Flask, request
import csv
from sklearn.cluster import DBSCAN
import statistics
import math
import matplotlib.pyplot as plt

app = Flask(__name__)


def predictPageTimeOutlier(trainData, testData, eps1, min_samples1):
    data = trainData
    data.append(testData)
    model = DBSCAN(eps=int(math.ceil(eps1)), min_samples=int(min_samples1)).fit(data)
    return model.labels_[-1]


def predictScrollPatternOutlier(trainData, testData, eps, min_samples):
    data = trainData
    data.append(testData)
    model = DBSCAN(eps=math.ceil(eps), min_samples=min_samples).fit(data)
    return model.labels_[-1]


def predictClickPatternOutlier(trainData, testData, eps, min_samples):
    data = trainData
    data.append(testData)
    model = DBSCAN(eps=math.ceil(eps), min_samples=min_samples).fit(data)
    return model.labels_[-1]


def writeTrainData(time_on_page, furthest_scroll_position, click_count):
    with open("testDate.csv", 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([int(time_on_page), int(furthest_scroll_position), int(click_count)])


@app.route('/user', methods=["POST"])
def post():
    thresholdScore = 80
    minimumSampleRequired = 15

    with open("modelConfig.csv", 'rt') as csvfile:
        modelConfig = csv.reader(csvfile)
        for row in modelConfig:
            pageTimeEps = row[0]
            pageTimeSamples = row[1]
            scrollEps = row[2]
            scrollSamples = row[3]
            clicksEps = row[4]
            clicksSamples = row[5]

    time_on_page = request.json['timeOnPage']
    furthest_scroll_position = request.json['furthestScrollPosition']
    click_count = request.json['clickCount']

    testDataFile = open("testDate.csv", 'rt')
    trainData = csv.reader(testDataFile)
    pageTimeData = []
    scrollData = []
    clicksData = []
    counter = 0
    for row in trainData:
        pageTimeData.append([int(row[0]), 1])
        scrollData.append([int(row[1]), 1])
        clicksData.append([int(row[2]), 1])
        counter += 1
    if counter < minimumSampleRequired:
        writeTrainData(time_on_page, furthest_scroll_position, click_count)
        return str("100")

    pageTimeMean = statistics.mean([a for a, b in [m for m in pageTimeData]])
    scrollMean = statistics.mean([a for a, b in [m for m in scrollData]])
    clicksMean = statistics.mean([a for a, b in [m for m in clicksData]])
    pageStdDev = statistics.stdev([a for a, b in [m for m in pageTimeData]])
    scrollStdDev = statistics.stdev([a for a, b in [m for m in scrollData]])
    clicksStdDev = statistics.stdev([a for a, b in [m for m in clicksData]])

    pageTimePer = (pageStdDev / pageTimeMean) * 100
    scrollPer = (scrollStdDev / scrollMean) * 100
    clicksPer = (clicksStdDev / clicksMean) * 100

    isPageTimeOutlier = predictPageTimeOutlier(pageTimeData, [int(time_on_page), 1], pageStdDev, pageTimeSamples)
    isScrollOutlier = predictPageTimeOutlier(scrollData, [int(furthest_scroll_position), 1], scrollStdDev,
                                             scrollSamples)
    isClickOutlier = predictPageTimeOutlier(clicksData, [int(click_count), 1], clicksStdDev, clicksSamples)

    total_sum = (pageTimePer + scrollPer + clicksPer)
    pageTimeWeight = ((total_sum - pageTimePer) / (total_sum * 2)) * 100
    scrollWeight = ((total_sum - scrollPer) / (total_sum * 2)) * 100
    clicksWeight = ((total_sum - clicksPer) / (total_sum * 2)) * 100

    pageAuthPer = (isPageTimeOutlier == 0 and 1 or 0) * pageTimeWeight
    scrollAuthPer = (isScrollOutlier == 0 and 1 or 0) * scrollWeight
    clickAuthPer = (isClickOutlier == 0 and 1 or 0) * clicksWeight

    totalScore = (pageAuthPer + scrollAuthPer + clickAuthPer)

    plt.axis([0, 10, 0, max([x for x, y in pageTimeData])])
    print(pageTimeData)
    plt.scatter([x for x, y in pageTimeData], [y for x, y in pageTimeData], c="blue")
    #plt.scatter([x for x in test_data], [x for x in test_data], c="red")
    plt.show()
    if (totalScore >= thresholdScore):
        writeTrainData(time_on_page, furthest_scroll_position, click_count)
    testDataFile.close()
    return str(totalScore)


app.run(debug=True)
