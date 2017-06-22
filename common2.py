__author__ = 'Jac'
#Developer = fengjiang

import random

def generateRandomString(ran, length):
    result = ""
    ranUnic = ran.decode("utf8")
    while len(result) < length:
        value = ranUnic[random.randint(0, len(ranUnic)-1)]
        if result.find(value) is -1:
            result += value
        elif len(result) >= len(ranUnic):
            result += value
    return result.encode("utf8")

def generateRandomChannel(range):
    '''
    random choise channel from [channel avilable]
    '''
    index = random.randint(0, len(range)-1)
    return range[index]






if __name__ == "__main__":
    CHANNEL_2_ALL = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
    CHANNEL_5_ALL = ['36', '40', '44', '48', '52', '56', '60', '64', '149', '153', '157', '161', '165']
    fjtest = generateRandomChannel(CHANNEL_2_ALL)
    fjtest1 = generateRandomChannel(CHANNEL_5_ALL)
    print fjtest, fjtest1