from numpy import log
titles = ['Week', 'Weather', 'Parents home?', 'Money', 'Activity']
mydata = [['W1', 'Sunny', 'Yes', 'Rich', 'Cinema'],
    ['W2', 'Sunny', 'No', 'Rich', 'Tennis'],
    ['W3', 'Windy', 'Yes', 'Rich', 'Cinema'],
    ['W4', 'Rainy', 'Yes', 'Poor', 'Cinema'],
    ['W5', 'Rainy', 'No', 'Rich', 'StayIn'],
    ['W6', 'Rainy', 'Yes', 'Poor', 'Cinema'],
    ['W7', 'Windy', 'No', 'Poor', 'Cinema'],
    ['W8', 'Windy', 'No', 'Rich', 'Shopping'],
    ['W9', 'Windy', 'Yes', 'Rich', 'Cinema'],
    ['W10', 'Sunny', 'No', 'Rich', 'Tennis']]

global nodescolumn
nodescolumn = 4
dontIncludeColumn = [0]


def divideset(rows,column,value):
    split_function=lambda row:row[column]==value
    set=[row for row in rows if split_function(row)]
    return set

def entropy(mydata, column, values, column2):
    entropy = 0
    for q in values:
        div = divideset(mydata, column, q)
        length = len(div)
        alist = []
        if len(values)==1:
            for i in div:
                if i[column2] not in alist:
                    alist.append(i[column2])
            log2 = lambda x:log(x)/log(2)
            for i in alist:
                div21 = divideset(div, column2, i)
                div2 = len(div21)
                entropy -= (div2/float(length))*(log2(div2/float(length)))
        else:
            prob = probability(mydata, column, q)
            entropy -= prob*(log(prob)/log(2))
    return entropy

def probability(mydata, column, value):
    return len(divideset(mydata, column, value))/float(len(mydata))

def gain(mydata, nodescolumn, column, sure):
    if sure == True:
        splitnodes = splitdata(mydata, nodescolumn)
        entropyS = entropy(mydata, nodescolumn, splitnodes, nodescolumn)
        split = splitdata(mydata, column)
        for i in split:
            entropyS -= probability(mydata, column, i)*entropy(mydata, column, [i], nodescolumn)
    else:
        entropyS = entropy(mydata, nodescolumn, sure, column)
        split2 = divideset(mydata, 1, str(sure[0]))
        for i in split2:
            entropyS -= probability(mydata, column, i)*entropy(sure, column, [i], nodescolumn)
    return float(entropyS)

def splitdata(mydata, column):
    array = []
    for i in mydata:
        if i[column] not in array:
            array.append(i[column])
    return array

def highestGain(mydata, dontIncludeColumn, nodescolumn, questions, sure):
    highest = 0
    for i in range(0, len(mydata[0])-1):
        #print(questions[len(questions)-1])
        if i not in dontIncludeColumn and i != nodescolumn and i != questions[0]:# and i not in questions[len(questions)-1]:
            infoGain = gain(mydata, nodescolumn, i, sure)
            if infoGain > highest:
                highest = i
    return highest

questions = [-1]
questions = [[highestGain(mydata, dontIncludeColumn, nodescolumn, questions, True)], []]
data = splitdata(mydata, questions[0][0])
print('\n' + str(titles[questions[0][0]]))
questions.append([])
for i in range(0, len(data)):
    questions[1].append(highestGain(mydata, dontIncludeColumn, questions[0][0], questions, [data[i]]))
    print('\t' + data[i] + ' -- ' + titles[questions[1][i]])
    sunnydata = divideset(mydata, 1, data[i])
    #print(data[i], sunnydata)
    yesnodata = splitdata(sunnydata, questions[1][i])
    #print(yesnodata)
    for q in yesnodata:
        newdata = divideset(mydata, 2, q)
        #print(newdata)
        entropyTest = entropy(newdata, 2, [q], 4)
        if entropyTest == 0:
            div = divideset(newdata, 2, q)
            activity = div[0][nodescolumn]
            print('\t\t' + str(q) + ' -- ' + str(activity))
        else:
            #print(i)
            questions[2].append(highestGain(mydata, dontIncludeColumn, questions[0][0], questions, [data[i]]))
            #print(questions)
            newsdata = splitdata(mydata, 3)
            #print(newsdata)
            #for i in newsdata:
            newdata = divideset(newsdata, 3, 'Rich')
            div = divideset(newdata, 3, q)
            #print(newdata)
            #print(div)
            #activity = div[2]
            #activity = 'Tennis'
            #activity = titles[questions[2][i]]
            print('\t\t' + str(q) + ' -- ' + str(activity))
        #print(q, entropyTest)
questions.append([])
print(questions)
print('')
