import numpy as np
import filereadwrite as frw

class Correction:
    def __init__(self, index, factor):
        self.index = index
        self.factor = factor

class Total_Data:
    def __init__(self, data, correction):
        self.data = data
        self.correction = correction
#correction is for a new file, adjust is if the file already exists
def adjust(data, name, dictionary):
    if dictionary == None or name == None or data == None:
        tot_data = Total_Data(data, None)
        return tot_data
    else:
        name += "0"
        name1 = dictionary.get(name)
        if name1 == None:
            tot_data = Total_Data(data, None)
            return tot_data
        else:
            fp = open(name1, "r")
            line = fp.readline()
            x = list(line.split("~"))
            x.pop()
            if "Logistic" not in x[0]:
                tot_data = Total_Data(data, None)
                return tot_data
            corrections = []
            for i in range(1, len(x)):
                y = list(x[i].split(":"))
                correction = Correction(int(y[0]), float(y[1]))
                corrections.append(correction)
            if len(corrections) == 0:
                corrections = None
            else:
                for i in corrections:
                    for j in range(len(data)):
                        data[j][i.index] /= i.factor
            tot_data = Total_Data(data, corrections)
            return tot_data

def find_max(data, position):
    maximum = data[0][position]
    for i in range(len(data)):
        if maximum < data[i][position]:
            maximum = data[i][position]
    return maximum

def find_min(data, position):
    minimum = data[0][position]
    for i in range(len(data)):
        if minimum > data[i][position]:
            minimum = data[i][position]
    return minimum

def correct(data):
    correction = []
    #tot_data = None
    for i in range(len(data[0])):
        maxi = find_max(data, i)
        if maxi > 1:
            j = 0
            while 10**j < maxi:
                j += 1
            for k in range(len(data)):
                data[k][i] /= 10**j #gets all the values between 0 and 1
            corr = Correction(i, 10**j)
            correction.append(corr)
    if len(correction) == 0:
        correction = None
    tot_data = Total_Data(data, correction)
    return tot_data
            

def Probability(x):
    return 1 / (1 + np.exp(-x))

def effective_balance(x):
    return x * (1 - x)

def Logistic_Regression(data, fromfile, dataexists):
    #Anything with Yes/No will be considered binary given by 0 and 1
    dictionary1 = frw.dictionary(False)
    tot_data = None
    X = None
    Y = None
    x = None
    y = None
    l = 0
    data_og = None
    if fromfile:
        for i in range(len(data)):
            data[i] = list(data[i].split("~"))
    data = frw.bin_maker(data)
    name = input("Enter the name of the file to store the data: ")
    if dataexists:
        data_og = frw.bin_data_read()
        tot_data = adjust(data, name, dictionary1)
        data = tot_data.data
        frw.append(data, name)
    name1 = None
    if dataexists:
        for i in data:
            data_og.append(i)
    else:
        data_og = data
        tot_data = correct(data_og)
        data_og = tot_data.data
    
    for i in data_og:
        y = i[0]
        x = i[1:]
        x.insert(0, 1.0)
        x1 = np.array([x])
        y1 = np.array([[y]])
        if l == 0:
            X = x1
            Y = y1
            l += 1
        else:
            X = np.append(X, x1, axis = 0)
            Y = np.append(Y, y1, axis = 0)
    W = None
    if dataexists:
        name += "0" #zero is the indicating key for Logistic Regression formula
        fp = None
        name1 = None
        while fp == None:
            if dictionary1 != None:
                name1 = dictionary1.get(name)
            while name1 == None and dictionary1 != None:
                name = input("Please enter the correct name: ")
                name += "0"
                name1 = dictionary1.get(name)
            fp = open(name1, "r")
        line = fp.readline()
        if "Logistic" not in line:
            print("ERROR")
            fp.close()
            return None
        line = fp.readline() #moves to second line
        fp.close()
        w = list(line.split("~"))
        w.pop()
        l = 0
        for i in range(len(w)):
            w[i] = float(w[i])
            wn = np.array([[w[i]]])
            if l == 0:
                W = wn
                l += 1
            else:
                W = np.append(W, wn, axis = 0)
            #W.append(i)
        for i in range(1000): #Since we already have a formula, we need a fewer number of steps to make it accurate
            #Even if incoming data is large we are technically handling Overfitting by doing this.
            Y1 = Probability(np.dot(X, W))
            error = Y - Y1
            adjust1 = error * effective_balance(Y1)
            adjustment = np.dot(X.T, adjust1)
            W += adjustment
    else:
        W = np.array([[0.1]])
        wx = np.array([[0.1]])
        for i in range(len(x) - 1):
            W = np.append(W, wx, axis = 0)
        for i in range(10000):
            Y1 = Probability(np.dot(X, W))
            error = Y - Y1
            adjust1 = error * effective_balance(Y1)
            adjustment = np.dot(X.T, adjust1)
            W += adjustment
    neW = np.append(W, W)
    neW = neW.tolist()
    l = len(neW)/2
    neW = neW[:int(l)]
    neW2 = None
    if dataexists:
        frw.write_formula(name1, neW, True, tot_data.correction)
        neW2 = [neW, name1]
    else:
        frw.append(data_og, name)
        val1 = name + ".txt"
        frw.dictionary_update(name, val1, False)
        key2 = name + "0"
        val2 = name + "_logisticformula.txt"
        frw.write_formula(val2, neW, True, tot_data.correction)
        frw.dictionary_update(key2, val2, False)
        neW2 = [neW, val2]
    return neW2