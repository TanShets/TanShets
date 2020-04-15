import numpy as np
import filereadwrite as frw

def Linear_Regression(data, fromfile, dataexists):
    X = None
    Y = None
    l = True
    dictionary_name = frw.dictionary(False)
    '''
    if isfile:
        for i in data:
            x = []
            gen = list(i.split("~"))
            y = gen[0]
            for j in range(1, len(gen)):
                x.append(gen[j])
            X.append(x)
            Y.append(y)
    else:
        for i in data:
            y = i[0]
            x = i[1:]
            X.append(x)
            Y.append(y)
    '''
    if fromfile:
        for i in range(len(data)):
            data[i] = list(data[i].split("~"))
    data = frw.bin_maker(data)
    data_og = None
    name = input("Enter the file to store data: ")
    frw.append(data, name)
    if dataexists:
        data_og = frw.bin_data_read()
    else:
        namex = name + ".txt"
        frw.dictionary_update(name, namex, False)

    if dataexists:
        for i in data:
            data_og.append(i)
    else:
        data_og = data
    for i in data_og:
        y = i[0]
        x = i[1:]
        x.insert(0, 1.0)
        x1 = np.array([x])
        y1 = np.array([[y]])
        if l:
            X = x1
            Y = y1
            l = False
        else:
            X = np.append(X, x1, axis = 0)
            Y = np.append(Y, y1, axis = 0)
    XT = X.T
    R = np.dot(XT, Y)
    L = np.dot(XT, X)
    LA = np.linalg.inv(L)
    B = np.dot(LA, R)
    #Essentially: B = (XtX)^(-1)XtY
    b = np.append(B, B)
    b = b.tolist()
    n = len(b)
    b = b[:int(n/2)]
    name1 = name + "1"
    new_name = dictionary_name.get(name1)
    if dataexists:
        if new_name == None:
            print("ERROR in saving into file, creating a new file with the same name.")
            new_name = name + "_linearformula.txt"
            frw.dictionary_update(name1, new_name, False)
    else:
        new_name = name + "_linearformula.txt"
        frw.dictionary_update(name1, new_name, False)
    frw.write_formula(new_name, b, False, None)
    return b