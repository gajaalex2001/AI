import csv
import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error


def loadData(fileName, inputVariabName, outputVariabName):
    data = []
    dataNames = []
    with open(fileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                dataNames = row
            else:
                if '' not in row:
                    data.append(row)
            line_count += 1
    selectedVariable = dataNames.index(inputVariabName)
    inputs = [float(data[i][selectedVariable]) for i in range(len(data))]
    selectedOutput = dataNames.index(outputVariabName)
    outputs = [float(data[i][selectedOutput]) for i in range(len(data))]

    return inputs, outputs


crtDir = os.getcwd()
filePath = os.path.join(crtDir, 'data', 'v3.csv')

x1, y = loadData(filePath, 'Economy..GDP.per.Capita.', 'Happiness.Score')
x2, _ = loadData(filePath, 'Freedom', 'Happiness.Score')

def plotData(x1, y1, x2 = None, y2 = None, x3 = None, y3 = None, title = None):
    plt.plot(x1, y1, 'ro', label = 'train data')
    if (x2):
        plt.plot(x2, y2, 'b-', label = 'learnt model')
    if (x3):
        plt.plot(x3, y3, 'g^', label = 'test data')
    plt.title(title)
    plt.legend()
    plt.show()

plotData(x1, y, [], [], [], [], 'Capita vs. Happiness')
plotData(x2, y, [], [], [], [], 'Freedom vs. Happiness')

np.random.seed(5)
indexes = [i for i in range(len(x1))]
trainSample = np.random.choice(indexes, int(0.8 * len(x1)), replace = False)
validationSample = [i for i in indexes  if not i in trainSample]
trainx1 = [x1[i] for i in trainSample]
trainx2 = [x2[i] for i in trainSample]
trainOutputs = [y[i] for i in trainSample]
validationx1 = [x1[i] for i in validationSample]
validationx2 = [x2[i] for i in validationSample]
validationOutputs = [y[i] for i in validationSample]

plotData(trainx1, trainOutputs, [], [], validationx1, validationOutputs, "train and test data gdp")
plotData(trainx2, trainOutputs, [], [], validationx2, validationOutputs, "train and test data freedom")

#training step
xx1 = [[el] for el in trainx1]
xx2 = [[el] for el in trainx2]
for i in range(len(xx1)):
    xx1[i] += xx2[i]

regressor = linear_model.LinearRegression()
regressor.fit(xx1, trainOutputs)
w0, w1, w2 = regressor.intercept_, regressor.coef_[0], regressor.coef_[1]
print(w0, w1, w2)

# plot the model
noOfPoints = 1000
xref = []
valx1 = min(trainx1)
valx2 = min(trainx2)
stepx1 = (max(trainx1) - min(trainx1)) / noOfPoints
stepx2 = (max(trainx2) - min(trainx2)) / noOfPoints
for i in range(1, noOfPoints):
    xref.append((valx1, valx2))
    valx1 += stepx1
    valx2 += stepx2
yref = [w0 + w1 * el[0] + w2 * el[1] for el in xref]

xref1 = [el[0] for el in xref]
xref2 = [el[1] for el in xref]

plotData(trainx1, trainOutputs, xref1, yref, [], [], title = "train data and model gdp")
plotData(trainx2, trainOutputs, xref2, yref, [], [], title = "train data and model freedom")

val = [[el] for el in validationx1]
val1 = [[el] for el in validationx2]
for i in range(len(val)):
    val[i] += val1[i]

computedValidationOutputs = regressor.predict(val)
xref1 = []
xref2 = []
for i in range(len(val)):
    xref1.append(val[i][0])
    xref2.append(val[i][1])

#plotData([], [], xref1, computedValidationOutputs, xref1, validationOutputs, "predictions vs real test data gdp")
#plotData([], [], xref2, computedValidationOutputs, xref2, validationOutputs, "predictions vs real test data freedom")

print(computedValidationOutputs)

#compute the differences between the predictions and real outputs
error = 0.0
for t1, t2 in zip(computedValidationOutputs, validationOutputs):
    error += (t1 - t2) ** 2
error = error / len(validationOutputs)
print("prediction error (manual): ", error)

error = mean_squared_error(validationOutputs, computedValidationOutputs)
print("prediction error (tool): ", error)