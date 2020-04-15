def dictionary(isbin):
    fp = None
    dict1 = {}
    try:
        if isbin:
            fp = open("dictionary_bin.txt", "r")
        else:
            fp = open("dictionary_name.txt", "r")
    except:
        return None
    if fp == None:
        print("Dictionary not found!")
        return None
    else:
        line = fp.readline()
        while line != "":
            key, value = line.split("~")
            value = value.replace("\n", "")
            if isbin:
                dict1[key] = float(value)
            else:
                dict1[key] = value
            line = fp.readline()
        return dict1

def write_formula(name, data, islog, correction):
    if name == None or data == None:
        return
    else:
        fp = None
        try:
            fp = open(name, "w")
        except:
            return
        if fp == None:
            return
        else:
            if islog:
                fp.write("Logistic~")
                if correction != None:
                    for i in correction:
                        word = str(i.index) + ":" + str(i.factor) + "~"
                        fp.write(word)
                fp.write("\n")
            else:
                fp.write("Linear\n")
            
            line = None
            for i in data:
                if line == None:
                    line = str(i) + "~"
                else:
                    line += str(i) + "~"
            fp.write(line)

def dictionary_update(key, value, isbin):
    dictionary1 = dictionary(isbin)
    fp = None
    if isbin:
        fp = open("dictionary_bin.txt", "a")
    else:
        fp = open("dictionary_name.txt", "a")
    if dictionary1 == None or dictionary1.get(key) == None:
        line = str(key) + "~" + str(value) + "\n"
        fp.write(line)
    fp.close()

def append(data, name):
    if data == None or name == None:
        return
    else:
        name += ".txt"
        try:
            fp = open(name, "a")
        except:
            return
        for i in range(len(data)):
            line = str(data[i][0]) + "~"
            for j in range(1, len(data[i])):
                line += str(data[i][j]) + "~"
            line += "\n"
            fp.write(line)
        fp.close()

def bin_maker(data):
    dictionary_val = dictionary(True)
    if data == None:
        return data
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j][0] in "-0123456789":
                if len(data[i][j]) > 1 and data[i][j][1] in ".0123456789":
                    data[i][j] = float(data[i][j])
                elif len(data[i][j]) == 1 and data[i][j] != "-":
                    data[i][j] = float(data[i][j])
            else:
                val = None
                if dictionary_val != None:
                    val = dictionary_val.get(data[i][j])
                
                if val != None:
                    data[i][j] = val
                else:
                    if "Not" in data[i][j] or "not" in data[i][j] or "NOT" in data[i][j]:
                        dictionary_update(data[i][j], float(0), True)
                        data[i][j] = float(0)
                    elif "No" in data[i][j] or "no" in data[i][j] or "NO" in data[i][j]:
                        dictionary_update(data[i][j], float(0), True)
                        data[i][j] = float(0)
                    else:
                        dictionary_update(data[i][j], float(1), True)
                        data[i][j] = float(1)
    return data

def bin_data_read():
    dictionary_name = dictionary(False)
    dictionary_val = dictionary(True)
    if dictionary_name == None:
        print("Directory Error!!!")
        return None
    data = None
    name = input("Enter the name of the file: ")
    while dictionary_name.get(name) == None:
        name = input("Enter the name of the file: ")
    filename = dictionary_name.get(name)
    try:
        fp = open(filename, "r")
    except:
        return None
    data = fp.readlines()
    fp.close()
    for i in range(len(data)):
        data[i] = list(data[i].split("~"))
        data[i].pop()
        for j in range(len(data[i])):
            if data[i][j][0] in "-0123456789":
                if len(data[i][j]) > 1 and data[i][j][1] in ".0123456789":
                    data[i][j] = float(data[i][j])
                elif len(data[i][j]) == 1 and data[i][j] != "-":
                    data[i][j] = float(data[i][j])
            else:
                val = dictionary_val.get(data[i][j])
                if val != None:
                    data[i][j] = val
                else:
                    if "Not" in data[i][j] or "not" in data[i][j] or "NOT" in data[i][j]:
                        dictionary_update(data[i][j], float(0), True)
                        data[i][j] = float(0)
                    elif "No" in data[i][j] or "no" in data[i][j] or "NO" in data[i][j]:
                        dictionary_update(data[i][j], float(0), True)
                        data[i][j] = float(0)
                    else:
                        dictionary_update(data[i][j], float(1), True)
                        data[i][j] = float(1)
    return data

def bin_maker_1d(data):
    dictionary_val = dictionary(True)
    if data == None:
        return data
    for i in range(len(data)):
        if data[i][0] in "-0123456789":
            if len(data[i]) > 1 and data[i][1] in ".0123456789":
                data[i] = float(data[i])
            elif len(data[i]) == 1 and data[i] != "-":
                data[i] = float(data[i])
        else:
            val = dictionary_val.get(data[i])
            if val != None:
                data[i] = val
            else:
                if "Not" in data[i] or "not" in data[i] or "NOT" in data[i]:
                    dictionary_update(data[i], float(0), True)
                    data[i] = float(0)
                elif "No" in data[i] or "no" in data[i] or "NO" in data[i]:
                    dictionary_update(data[i], float(0), True)
                    data[i] = float(0)
                else:
                    dictionary_update(data[i], float(1), True)
                    data[i] = float(1)
    return data