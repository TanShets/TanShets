import filereadwrite as frw
import Linear_Regr as Lr
import Logistic_Regr as lr
import math

def adjust_1d(dataline, filename):
    if dataline == None or filename == None:
        return dataline
    else:
        fp = open(filename, "r")
        line = fp.readline()
        fp.close()
        line = line.split("~")
        line.pop()
        corrections =[]
        for i in range(1, len(line)):
            y = list(line[i].split(":"))
            correction = lr.Correction(int(y[0]), float(y[1]))
            corrections.append(correction)
        if len(corrections) == 0:
            return dataline
        else:
            for i in corrections:
                dataline[i.index - 1] /= i.factor
        return dataline

def sigmoid(z):
    return 1 / (1 + math.exp(-z))

def result(W, isbin, filename):
    l = len(W)
    new_input = []
    while len(new_input) != l - 1:
        new_input = list(input("Enter values separated by space: ").split())
    z = 0.0
    new_input = frw.bin_maker_1d(new_input)
    if isbin:
        if filename != None:
            new_input = adjust_1d(new_input, filename)
    new_input.insert(0, 1.0)
    for i in range(l):
        z += W[i] * new_input[i]
    y = None
    if isbin:
        y = sigmoid(z)
        if y >= 0.5:
            print("The event will occur. (Yes)")
        else:
            print("The event will not occur. (No)")
    else:
        y = z
        print("Predicted value:", y)

def isbinary(data, fromfile):
    #dictionary_val = frw.dictionary(True)
    a = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm"
    a = set(a)
    if fromfile:
        if data[0][0] not in "-0123456789":
            return True
        else:
            i = 1
            while data[0][i] != "~":
                i += 1
            if a.intersection(set(data[0][:i])) != {}:
                return True
            else:
                for i in range(1, len(data)):
                    x = data[i].find('~')
                    if data[i][:x] != "0.0" and data[i][:x] != "1.0":
                        return False
                return True
    else:
        if a.intersection(set(data[0][0])) != set():
            return True
        else:
            for i in range(len(data)):
                if data[i][0] != "0.0" and data[i][0] != "1.0":
                    return False
            print("1")
            return True
        
choice1 = input("Would you like to enter new data? Y/N ")
if choice1 in "Yy":
    choice2 = input("Is it in the form of a file? Y/N ")
    fromfile = None
    data = None
    if choice2 in "Yy":
        name = input("Enter the name of the file without the txt extension: ")
        name += ".txt"
        fp = open(name, "r")
        data = fp.readlines()
        fp.close()
        fromfile = True
    else:
        m = int(input("Enter the number of lines of data: "))
        n = int(input("Enter the number of parameters excluding the outcome: "))
        data = []
        for i in range(m):
            line = list(input("Enter the line (output first) separated by space for each value: ").split())
            data.append(line)
        fromfile = False
    dataexists = None
    choice3 = input("Is this data, an addition to data already in a file? Y/N ")
    if choice3 in "Yy":
        dataexists = True
    else:
        dataexists = False
    W = None
    if isbinary(data, fromfile):
        W = lr.Logistic_Regression(data, fromfile, dataexists)
        result(W[0], True, W[1])
    else:
        W = Lr.Linear_Regression(data, fromfile, dataexists)
        print(W)
        result(W, False, None)

choice4 = input("Do you wish to predict an outcome from data? Y/N ")
if choice4 in "Yy":
    name = input("Enter the name of the file or database: ")
    name1 = input("Press 0 for Logistic Prediction, Press 1 for Linear Prediction: ")
    while name1 != "1" and name1 != "0":
        name1 = input("Incorrect!! Enter 0 for Logistic, 1 for Linear: ")
    name += name1
    dictionary_name = frw.dictionary(False)
    filename = dictionary_name.get(name)
    if filename == None:
        print("ERROR! File Not Found")
    else:
        fp = open(filename, "r")
        line = fp.readline()
        if "Linear" not in line and "Logistic" not in line:
            print("ERROR")
        else:
            isbin = None
            if "Linear" in line:
                isbin = False
            else:
                isbin = True
            line = fp.readline()
            line = line.replace("\n", "")
            line = list(line.split("~"))
            line.pop()
            line = list(map(float, line))
            l = len(line)
            new_input = []
            while len(new_input) != l - 1:
                new_input = list(input("Enter values separated by space: ").split())
            z = 0.0
            new_input = frw.bin_maker_1d(new_input)
            new_input = adjust_1d(new_input, filename)
            new_input.insert(0, 1.0)
            for i in range(l):
                z += line[i] * new_input[i]
            y = None
            if isbin:
                y = sigmoid(z)
                if y >= 0.5:
                    print("The event will occur. (Yes)")
                else:
                    print("The event will not occur. (No)")
            else:
                y = z
                print("Predicted value:", y)