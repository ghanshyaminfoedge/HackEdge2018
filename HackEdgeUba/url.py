from flask import Flask, request
import csv
from sklearn.cluster import DBSCAN
import statistics

app = Flask(__name__)


def predictPageTimeOutlier(trainData, testData, eps1, min_samples1):
    data = trainData
    data.append(testData)
    model = DBSCAN(eps=1, min_samples=10).fit(data)
    return model.labels_[-1]


def predictScrollPatternOutlier(trainData, testData, eps, min_samples):
    data = trainData
    data.append(testData)
    model = DBSCAN(eps=eps, min_samples=min_samples).fit(data)
    return model.labels_[-1]


def predictClickPatternOutlier(trainData, testData, eps, min_samples):
    data = trainData
    data.append(testData)
    model = DBSCAN(eps=eps, min_samples=min_samples).fit(data)
    return model.labels_[-1]


def writeTrainData(time_on_page, furthest_scroll_position, click_count):
    with open("testDate.csv", 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([int(time_on_page), int(furthest_scroll_position), int(click_count)])


@app.route('/user', methods=["POST"])
def post():
    pageTimeWeight = 42
    scrollWeight = 25
    clicksWeight = 33
    thresholdScore = 62
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

    with open("testDate.csv", 'rt') as csvfile:
        trainData = csv.reader(csvfile)
        pageTimeData = []
        scrollData = []
        clicksData = []
#        if len(list(trainData)) < minimumSampleRequired:
#            writeTrainData(time_on_page, furthest_scroll_position, click_count)
#            return str(101)

        for row in trainData:
            pageTimeData.append([int(row[0]), 1])
            scrollData.append([int(row[1]), 1])
            clicksData.append([int(row[2]), 1])

    print(statistics.stdev([a for a, b in [m for m in pageTimeData]]))
    print(statistics.stdev([a for a, b in [m for m in scrollData]]))
    print(statistics.stdev([a for a, b in [m for m in clicksData]]))
    isPageTimeOutlier = predictPageTimeOutlier(pageTimeData, [int(time_on_page), 1], pageTimeEps, pageTimeSamples)
    isScrollOutlier = predictPageTimeOutlier(scrollData, [int(furthest_scroll_position), 1], scrollEps, scrollSamples)
    isClickOutlier = predictPageTimeOutlier(clicksData, [int(click_count), 1], clicksEps, clicksSamples)
    pageAuthPer = (isPageTimeOutlier == 0 and 1 or 0) * pageTimeWeight
    scrollAuthPer = (isScrollOutlier == 0 and 1 or 0) * scrollWeight
    clickAuthPer = (isClickOutlier == 0 and 1 or 0) * clicksWeight

    totalScore = pageAuthPer + scrollAuthPer + clickAuthPer

    if (totalScore >= thresholdScore):
        writeTrainData(time_on_page, furthest_scroll_position, click_count)

    return str(thresholdScore)


app.run(debug=True)
