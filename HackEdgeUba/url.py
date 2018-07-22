from flask import Flask, request, jsonify
import csv
from sklearn.cluster import DBSCAN
import statistics
import math
from flask_cors import CORS
import json
from collections import namedtuple
import mysql.connector
import time
from hdbscan import HDBSCAN
import numpy as np

app = Flask(__name__)
CORS(app)


def predictPageTimeOutlier(trainData, testData, eps1, min_samples1):
    data = trainData
    data.append(testData)
    eps1 = eps1 == 0 and 1 or eps1
    model = DBSCAN(eps=int(math.ceil(eps1)), min_samples=int(min_samples1)).fit(data)
    return model.labels_[-1]


def predictScrollPatternOutlier(trainData, testData, eps, min_samples):
    data = trainData
    data.append(testData)
    eps = eps == 0 and 1 or eps
    model = DBSCAN(eps=int(math.ceil(eps)), min_samples=int(min_samples)).fit(data)
    return model.labels_[-1]


def predictClickPatternOutlier(trainData, testData, eps, min_samples):
    data = trainData
    data.append(testData)
    eps = eps == 0 and 1 or eps
    model = DBSCAN(eps=int(math.ceil(eps)), min_samples=int(min_samples)).fit(data)
    return model.labels_[-1]


def writeTrainData(file_name, time_on_page, furthest_scroll_position, click_count):
    with open(file_name, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([time_on_page, int(furthest_scroll_position), int(click_count)])


def saveKeyStrokeData(keyStrokeData, timeInSeconds):
    db = mysql.connector.connect(user='root', password='infoedge', database='keystroke_data')
    cur = db.cursor()
    x = json.loads(keyStrokeData, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    for i in range(0, len(x) - 1, 1):
        keyCombo = str(x[i].keyCode) + '-' + str(x[i + 1].keyCode)
        timeheld_1 = x[i].timeUp - x[i].timeDown
        timeheld_2 = x[i + 1].timeUp - x[i + 1].timeDown
        timeDD = x[i + 1].timeDown - x[i].timeDown
        timeUD = x[i + 1].timeDown - x[i].timeUp
        data_array = str(timeheld_1) + ',' + str(timeheld_2) + ',' + str(timeDD) + ',' + str(timeUD)
        queryString = (
            "insert into keystroke_data.keystroke (username,key_combo,data_array,created) values (%s,%s,%s,%s);")
        insertdata = ('ghan', keyCombo, data_array, timeInSeconds)
        cur.execute(queryString, insertdata)
    db.commit()
    cur.close()
    db.close()


def testKeyStrokeHistory():
    db = mysql.connector.connect(user='root', password='infoedge', database='keystroke_data')
    cur = db.cursor(buffered=True)
    min_cluster_siz = 4
    cur.execute("select key_combo from keystroke group by username, key_combo having count(*)>10;")
    listOfModelOutputs = []
    for row in cur:
        selectcur = db.cursor(buffered=True)
        selectcur.execute("select data_array from keystroke where key_combo = '{}'".format(row[0]))
        arr = []
        for resrow in selectcur:
            y = [float(i) for i in resrow[0].split(',')]
            arr.append(y)
        omodel = HDBSCAN(min_cluster_size=min_cluster_siz).fit(np.array(arr))
        print(omodel.labels_)
        listOfModelOutputs.append(omodel.labels_)
        selectcur.close()
    cur.close()
    db.close()
    totalKeyComboAnalysing = 0
    deviationCount = 0
    for le in listOfModelOutputs:
        totalKeyComboAnalysing = totalKeyComboAnalysing + 1
        clusteridtocount = {}
        currentClusterCount = 0
        for val in le.tolist():
            if val in clusteridtocount:
                clusteridtocount[val] = clusteridtocount[val] + 1
            else:
                clusteridtocount[val] = 1
        for the_key, the_value in clusteridtocount.items():
            if the_value > min_cluster_siz:
                currentClusterCount = currentClusterCount + 1
        if currentClusterCount > 1:
            deviationCount = deviationCount + 1
    return (deviationCount * 100) / totalKeyComboAnalysing


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
    timeInSeconds = int(round(time.time() * 1000 * 1000))
    requestData = request.get_data().decode('utf8')
    requestObject = json.loads(requestData, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    keyStorkDtata = requestObject.keyStrokeLog
    saveKeyStrokeData(keyStorkDtata, timeInSeconds)
    percentage = testKeyStrokeHistory()
    print(percentage)
    time_on_page = requestObject.timeOnPage
    time_on_page = int(time_on_page / 1000)
    furthest_scroll_position = requestObject.furthestScrollPosition
    click_count = requestObject.clickCount
    print('********Request Values***********')
    print(time_on_page)
    print(furthest_scroll_position)
    print(click_count)

    testDataFile = open("landingData.csv", 'rt')
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
        writeTrainData("landingData.csv", time_on_page, furthest_scroll_position, click_count)
        return jsonify({"totalScore": 100})
    pageTimeMean = statistics.mean([a for a, b in [m for m in pageTimeData]])
    scrollMean = statistics.mean([a for a, b in [m for m in scrollData]])
    clicksMean = statistics.mean([a for a, b in [m for m in clicksData]])
    pageStdDev = statistics.stdev([a for a, b in [m for m in pageTimeData]])
    scrollStdDev = statistics.stdev([a for a, b in [m for m in scrollData]])
    clicksStdDev = statistics.stdev([a for a, b in [m for m in clicksData]])
    print('********Mean***********')
    print(pageTimeMean)
    print(scrollMean)
    print(clicksMean)
    print('********Deviation***********')
    print(pageStdDev)
    print(scrollStdDev)
    print(clicksStdDev)
    pageTimePer = 0
    scrollPer = 0
    clicksPer = 0
    if pageTimeMean != 0:
        pageTimePer = (pageStdDev / pageTimeMean) * 100
    if scrollMean != 0:
        scrollPer = (scrollStdDev / scrollMean) * 100
    if clicksMean != 0:
        clicksPer = (clicksStdDev / clicksMean) * 100
    isPageTimeOutlier = predictPageTimeOutlier(pageTimeData, [int(time_on_page), 1], pageStdDev, pageTimeSamples)

    if (scrollStdDev == 0) & (scrollMean == furthest_scroll_position):
        isScrollOutlier = 1
    else:
        isScrollOutlier = predictScrollPatternOutlier(scrollData, [int(furthest_scroll_position), 1], scrollStdDev,
                                                      scrollSamples)
    isClickOutlier = predictScrollPatternOutlier(clicksData, [int(click_count), 1], clicksStdDev, clicksSamples)
    print('*******Training Data Percentage************')
    print(pageTimePer)
    print(scrollPer)
    print(clicksPer)
    print('********Outliers***********')
    print(isPageTimeOutlier)
    print(isScrollOutlier)
    print(isClickOutlier)
    total_sum = (pageTimePer + scrollPer + clicksPer)
    pageTimeWeight = ((total_sum - pageTimePer) / (total_sum * 2)) * 100
    scrollWeight = ((total_sum - scrollPer) / (total_sum * 2)) * 100
    clicksWeight = ((total_sum - clicksPer) / (total_sum * 2)) * 100
    print('*******************')
    print(pageTimeWeight)
    print(scrollWeight)
    print(clicksWeight)

    total_weight = ((pageTimeWeight * 0.4) + (scrollWeight * 0.2) + (clicksWeight * 0.4))
    pageTimeWeight = ((total_weight - (pageTimeWeight * 0.4)) / (total_weight * 2)) * 100
    scrollWeight = ((total_weight - (scrollWeight * 0.2)) / (total_weight * 2)) * 100
    clicksWeight = ((total_weight - (clicksWeight * 0.4)) / (total_weight * 2)) * 100
    print('********Final Weight Percentage***********')
    print(pageTimeWeight)
    print(scrollWeight)
    print(clicksWeight)

    pageAuthPer = (isPageTimeOutlier >= 0 and 1 or 0) * pageTimeWeight
    scrollAuthPer = (isScrollOutlier >= 0 and 1 or 0) * scrollWeight
    clickAuthPer = (isClickOutlier >= 0 and 1 or 0) * clicksWeight
    print('******Final Scores*************')
    print(pageAuthPer)
    print(scrollAuthPer)
    print(clickAuthPer)

    totalScore = (pageAuthPer + scrollAuthPer + clickAuthPer)

    if (totalScore >= thresholdScore):
        writeTrainData("landingData.csv", time_on_page, furthest_scroll_position, click_count)
    testDataFile.close()

    return jsonify({"totalScore": totalScore})


@app.route('/user/login', methods=["POST"])
def postLogin():
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
    time_on_page = int(time_on_page / 1000)
    furthest_scroll_position = request.json['furthestScrollPosition']
    click_count = request.json['clickCount']
    print('********Request Values***********')
    print(time_on_page)
    print(furthest_scroll_position)
    print(click_count)

    testDataFile = open("landingData.csv", 'rt')
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
        writeTrainData("landingData.csv", time_on_page, furthest_scroll_position, click_count)
        return jsonify({"totalScore": 100})
    pageTimeMean = statistics.mean([a for a, b in [m for m in pageTimeData]])
    scrollMean = statistics.mean([a for a, b in [m for m in scrollData]])
    clicksMean = statistics.mean([a for a, b in [m for m in clicksData]])
    pageStdDev = statistics.stdev([a for a, b in [m for m in pageTimeData]])
    scrollStdDev = statistics.stdev([a for a, b in [m for m in scrollData]])
    clicksStdDev = statistics.stdev([a for a, b in [m for m in clicksData]])
    print('********Mean***********')
    print(pageTimeMean)
    print(scrollMean)
    print(clicksMean)
    print('********Deviation***********')
    print(pageStdDev)
    print(scrollStdDev)
    print(clicksStdDev)
    pageTimePer = 0
    scrollPer = 0
    clicksPer = 0
    if pageTimeMean != 0:
        pageTimePer = (pageStdDev / pageTimeMean) * 100
    if scrollMean != 0:
        scrollPer = (scrollStdDev / scrollMean) * 100
    if clicksMean != 0:
        clicksPer = (clicksStdDev / clicksMean) * 100
    isPageTimeOutlier = predictPageTimeOutlier(pageTimeData, [int(time_on_page), 1], pageStdDev, pageTimeSamples)

    if (scrollStdDev == 0) & (scrollMean == furthest_scroll_position):
        isScrollOutlier = 1
    else:
        isScrollOutlier = predictScrollPatternOutlier(scrollData, [int(furthest_scroll_position), 1], scrollStdDev,
                                                      scrollSamples)
    isClickOutlier = predictScrollPatternOutlier(clicksData, [int(click_count), 1], clicksStdDev, clicksSamples)
    print('*******Training Data Percentage************')
    print(pageTimePer)
    print(scrollPer)
    print(clicksPer)
    print('********Outliers***********')
    print(isPageTimeOutlier)
    print(isScrollOutlier)
    print(isClickOutlier)
    total_sum = (pageTimePer + scrollPer + clicksPer)
    pageTimeWeight = ((total_sum - pageTimePer) / (total_sum * 2)) * 100
    scrollWeight = ((total_sum - scrollPer) / (total_sum * 2)) * 100
    clicksWeight = ((total_sum - clicksPer) / (total_sum * 2)) * 100
    print('*******************')
    print(pageTimeWeight)
    print(scrollWeight)
    print(clicksWeight)

    total_weight = ((pageTimeWeight * 0.4) + (scrollWeight * 0.2) + (clicksWeight * 0.4))
    pageTimeWeight = ((total_weight - (pageTimeWeight * 0.4)) / (total_weight * 2)) * 100
    scrollWeight = ((total_weight - (scrollWeight * 0.2)) / (total_weight * 2)) * 100
    clicksWeight = ((total_weight - (clicksWeight * 0.4)) / (total_weight * 2)) * 100
    print('********Final Weight Percentage***********')
    print(pageTimeWeight)
    print(scrollWeight)
    print(clicksWeight)

    pageAuthPer = (isPageTimeOutlier >= 0 and 1 or 0) * pageTimeWeight
    scrollAuthPer = (isScrollOutlier >= 0 and 1 or 0) * scrollWeight
    clickAuthPer = (isClickOutlier >= 0 and 1 or 0) * clicksWeight
    print('******Final Scores*************')
    print(pageAuthPer)
    print(scrollAuthPer)
    print(clickAuthPer)

    totalScore = (pageAuthPer + scrollAuthPer + clickAuthPer)

    if (totalScore >= thresholdScore):
        writeTrainData("landingData.csv", time_on_page, furthest_scroll_position, click_count)
    testDataFile.close()

    return jsonify({"totalScore": totalScore})


app.run(debug=True)
