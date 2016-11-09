import sys
import io
import os
import math

def distance(p1, p2):
    i = 0
    dist = []
    while i < len(p1):
        d = math.sqrt(
            math.pow(float(p1[i]) - float(p2[i]), 2) +
            math.pow(float(p1[i+1]) - float(p2[i+1]), 2) +
            math.pow(float(p1[i+2]) - float(p2[i+2]), 2)
        )
        dist.append(str("{0:.5f}".format(d)))
        i += 3
    # dist.append(d)
    return dist

def delta(featVectList):
    deltaFeat = []
    for i in range(len(featVectList[-1])):
        d = float(featVectList[-1][i]) - float(featVectList[-2][i])
        deltaFeat.append(str("{0:.5f}".format(d)))
    return deltaFeat


def calVector(p1, p2):
    v = []
    for i in range(len(p1)):
        p = float(p2[i]) - float(p1[i])
        v.append(str("{0:.5f}".format(p)))
    return v


# var yaw = atan2(2.0*(q.y*q.z + q.w*q.x), q.w*q.w - q.x*q.x - q.y*q.y + q.z*q.z);
# var pitch = asin(-2.0*(q.x*q.z - q.w*q.y));
# var roll = atan2(2.0*(q.x*q.y + q.w*q.z), q.w*q.w + q.x*q.x - q.y*q.y - q.z*q.z);
def rollFromQuant(quant):
    w = float(quant[0])
    x = float(quant[1])
    y = float(quant[2])
    z = float(quant[3])
    roll = math.atan2(2.0 * (x * y + w * z), w * w + x * x - y * y - z * z)
    return str("{0:.5f}".format(roll))




if len(sys.argv) != 3:
    print "Usage: featExtraction.py inputFile outFolderName featureIndex"
    print "Please input the feature set that you want to generated and seperated the index by comma: \n" +\
          "0:     hand position\n" +\
          "1:     hand position delta\n" +\
          "2:     tip & hand distance\n" +\
          "3:     tip & hand distance delta\n" +\
          "4:     thumb & hand distance\n" +\
          "5:     thumb & hand distance delta\n" +\
          "6:     thumb & hand distance delta & hand orientation\n" +\
          "7:     Roll of hand quanternion\n" +\
          "8:     shoulder & elbow vector \n" +\
          "9:     elbow & hand vector \n" +\
          "10:    left & right hand vector \n\n" +\
          "Example input:  python featExtraction.py handPosition 1,2"
    exit

featureNameSets = [
    "handPosition",
    "handPositionDelta",
    "tipHandDistance",
    "tipHandDistanceDelta",
    "thumbHandDistance",
    "thumbHandDistanceDelta",
    "handOrientation",
    "handRoll",
    "shoulderElbowVector",
    "elbowHandVector",
    "leftRightHandVector"
];


# feature list
handPosition = []
handPositionDelta = []
tipPosition = []
tipHandDistance = []
tipHandDistanceDelta = []
thumbPosition = []
thumbHandDistance = []
thumbHandDistanceDelta = []
handOrientation = []
handRoll = []
shoulderPosition = []
elbowPosition = []
shoulderElbowVector = []
elbowHandVector = []
leftRightHandVector = []


# featureName = sys.argv[2]
# arkFolder = featureName + "/ark"
# htkFolder = featureName + "/htk"

featureIndex = [int(i) for i in sys.argv[2].split(",")]

inputFile = io.open(sys.argv[1], "r")

# inputFile = io.open(sys.argv[1], "r", encoding="utf-16-le")

name = sys.argv[1].replace(".txt", ".txt.ark")

outFile = open(name, 'w')

# read original feature files

line = inputFile.readline()
line = line.strip("\r\n")

# feature before " |||" are orientation features
orientationFeats = line.split("  ||| ")[0].split(" ")
handOrientation.append(orientationFeats[36:44])

# roll feature
# handRoll.append(
#     [rollFromQuant(orientationFeats[36:40]),
#      rollFromQuant(orientationFeats[40:44])])


# feature after "  ||| " are position features
line = line.split("  ||| ")[1]

# 27 -33: x, y, z of left & right hand position
features = line.split(" ")

handFeatures = features[27:33]
handPosition.append(handFeatures)
handPositionDelta.append(handFeatures)

thumbFeatures = features[33:39]
# thumb position
thumbPosition.append(thumbFeatures)
# thumb & hand distance
thumbHandD = distance(thumbPosition[-1], handPosition[-1])
thumbHandDistance.append(thumbHandD)
thumbHandDistanceDelta.append(thumbHandD)
# print "thumb features distance:"
# print thumbHandD

tipFeatures = features[39:45]
tipPosition.append(tipFeatures)
#tip & hand distance
tipHandD = distance(tipPosition[-1], handPosition[-1])
tipHandDistance.append(tipHandD)
tipHandDistanceDelta.append(tipHandD)
# print "tip features distance:"
# print tipHandD


# Shoulder -> elbow vector feature
shoulderFeatures = features[6:12]
shoulderPosition.append(shoulderFeatures)
elbowFeatures = features[15:21]
elbowPosition.append(elbowFeatures)

# Calculate vectors
shoulderElbowVector.append(calVector(shoulderFeatures, elbowFeatures))
elbowHandVector.append(calVector(elbowFeatures, handFeatures))
leftRightHandVector.append(calVector(handFeatures[0:3], handFeatures[3:]))


while True:
    line = inputFile.readline()
    line = line.strip("\r\n")
    if line == "":
        break
    
    # hand orientation quaternion features
    orientationFeats = line.split("  ||| ")[0].split(" ")
    handOrientation.append(orientationFeats[36:44])

    # roll feature
    # handRoll.append(
    #     [rollFromQuant(orientationFeats[36:40]),
    #      rollFromQuant(orientationFeats[40:44])])

    line = line.split("  ||| ")[1]
    features = line.split(" ")

    # hand features
    handFeatures = features[27:33]
    handPosition.append(handFeatures)
    handPositionDelta.append(delta(handPosition))


    # thumb features
    thumbFeatures = features[33:39]
    thumbPosition.append(thumbFeatures)
    
    thumbHandD = distance(thumbPosition[-1], handPosition[-1])
    thumbHandDistance.append(thumbHandD)

    thumbHandDistanceDelta.append(delta(thumbHandDistance))


    # tip features
    tipFeatures = features[39:45]
    tipPosition.append(tipFeatures)
    
    tipHandD = distance(tipPosition[-1], handPosition[-1])
    tipHandDistance.append(tipHandD)
    tipHandDistanceDelta.append(delta(tipHandDistance))

    # shoulder & elbow features
    shoulderFeatures = features[6:12]
    shoulderPosition.append(shoulderFeatures)
    elbowFeatures = features[15:21]
    elbowPosition.append(elbowFeatures)

    # Calculate vectors
    shoulderElbowVector.append(calVector(shoulderFeatures, elbowFeatures))
    elbowHandVector.append(calVector(elbowFeatures, handFeatures))
    leftRightHandVector.append(calVector(handFeatures[0:3], handFeatures[3:]))



for i in range(len(handPosition)):
    featureLine = ""
    if i == 0:
        name = name.replace(".ark", "")
        featureLine =  name.replace("testsets/", "") +" [ "

    if 0 in featureIndex:
        # print "handPosition:\t" + " ".join(handPosition[i])
        featureLine += " ".join(handPosition[i]) + ' '
    if 1 in featureIndex:
        # print "handPositionDelta:\t" + " ".join(handPositionDelta[i])
        featureLine += " ".join(handPositionDelta[i]) + ' '
    if 2 in featureIndex:
        featureLine += " ".join(tipHandDistance[i]) + ' '
    if 3 in featureIndex:
        featureLine += " ".join(tipHandDistanceDelta[i]) + ' '
    if 4 in featureIndex:
        featureLine += " ".join(thumbHandDistance[i]) + ' '
    if 5 in featureIndex:
        featureLine += " ".join(thumbHandDistanceDelta[i]) + ' '
    if 6 in featureIndex:
        featureLine += " ".join(handOrientation[i]) + ' '
    if 7 in featureIndex:
        featureLine += " ".join(handRoll[i]) + ' '
    if 8 in featureIndex:
        featureLine += " ".join(shoulderElbowVector[i]) + ' '
    if 9 in featureIndex:
        featureLine += " ".join(elbowHandVector[i]) + ' '
    if 10 in featureIndex:
        featureLine += " ".join(leftRightHandVector[i]) + ' '


    featureLine = featureLine.strip(" ")
    # print featureLine
    # raw_input()

    print >>outFile, featureLine

print >> outFile, ']'
# cmd = "copy-feats-to-htk --output-dir=" + htkFolder + " --output-ext=htk --sample-period=40000 ark:" + outputFileName
# print cmd
# os.system(cmd)

