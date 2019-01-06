import numpy as np
import math
import random



def getMatrixFromFile(filename):
    #print(filename)
    return np.loadtxt(filename)




#Bent Cigar Function
def basic01(x):
    result = 0
    sigma = 0
    for i in range(1,len(x)):
        sigma += x[i]*x[i]
    result = x[0]*x[0] + 1000000*sigma
    return result

def test01_D10(X):
    try:
        return basic01(np.dot(test01_D10.M, (X - test01_D10.O)))
    except AttributeError:
        path = 'utilities/M_1_D10.txt'
        test01_D10.M = getMatrixFromFile(path)
        path = 'utilities/shift_data_1.txt'
        test01_D10.O = getMatrixFromFile(path)[0:10]
        return basic01(np.dot(test01_D10.M, (X - test01_D10.O)))

def test01_D30(X):
    try:
        return basic01(np.dot(test01_D30.M, (X - test01_D30.O)))
    except AttributeError:
        path = 'utilities/M_1_D30.txt'
        test01_D30.M = getMatrixFromFile(path)
        path = 'utilities/shift_data_1.txt'
        test01_D30.O = getMatrixFromFile(path)[0:30]
        return basic01(np.dot(test01_D30.M, (X - test01_D30.O)))

#Sum of Different Power Function
def basic02(x):
    sigma = 0
    for i in range(len(x)):
        sigma += pow(abs(x[i]), i+1)
    return sigma

def test02_D10(X):
    try:
        return basic02(np.dot(test02_D10.M, (X - test02_D10.O)))
    except AttributeError:
        path = 'utilities/M_2_D10.txt'
        test02_D10.M = getMatrixFromFile(path)
        path = 'utilities/shift_data_2.txt'
        test02_D10.O = getMatrixFromFile(path)[0:10]
        return basic02(np.dot(test02_D10.M, (X - test02_D10.O)))

def test02_D30(X):
    try:
        return basic02(np.dot(test02_D30.M, (X - test02_D30.O)))
    except AttributeError:
        path = 'utilities/M_2_D30.txt'
        test02_D30.M = getMatrixFromFile(path)
        path = 'utilities/shift_data_2.txt'
        test02_D30.O = getMatrixFromFile(path)[0:30]
        return basic02(np.dot(test02_D30.M, (X - test02_D30.O)))

#Zakharov Function
def basic03(x):
    sigma1 = 0
    sigma2 = 0
    sigma3 = 0
    for i in range(len(x)):
        sigma1 += x[i]*x[i]
        sigma2 += .5 * x[i]
        sigma3 += .5 * x[i]
    return sigma1 + pow(sigma2, 2) + pow(sigma3, 4)

def test03_D10(X):
    try:
        return basic03(np.dot(test03_D10.M, (X - test03_D10.O)))
    except AttributeError:
        path = 'utilities/M_3_D10.txt'
        test03_D10.M = getMatrixFromFile(path)
        path = 'utilities/shift_data_3.txt'
        test03_D10.O = getMatrixFromFile(path)[0:10]
        return basic03(np.dot(test03_D10.M, (X - test03_D10.O)))

def test03_D30(X):
    try:
        return basic03(np.dot(test03_D30.M, (X - test03_D30.O)))
    except AttributeError:
        path = 'utilities/M_3_D30.txt'
        test03_D30.M = getMatrixFromFile(path)
        path = 'utilities/shift_data_3.txt'
        test03_D30.O = getMatrixFromFile(path)[0:30]
        return basic03(np.dot(test03_D30.M, (X - test03_D30.O)))

#Rosenbrock’s Function
def basic04(x):
    sigma = 0
    for i in range(len(x)-1):
        part1 = x[i]*x[i] - x[i+1]
        part2 = x[i] - 1
        sigma += 100 * pow(part1, 2) + pow(part2, 2)
    return sigma

def test04_D10(X):
    try:
        return basic04(np.dot(test04_D10.M, (X - test04_D10.O)))
    except AttributeError:
        path = 'utilities/M_4_D10.txt'
        test04_D10.M = getMatrixFromFile(path)
        path = 'utilities/shift_data_4.txt'
        test04_D10.O = getMatrixFromFile(path)[0:10]
        return basic04(np.dot(test04_D10.M, (X - test04_D10.O)))

def test04_D30(X):
    try:
        return basic02(np.dot(test04_D30.M, (X - test04_D30.O)))
    except AttributeError:
        path = 'utilities/M_4_D30.txt'
        test04_D30.M = getMatrixFromFile(path)
        path = 'utilities/shift_data_4.txt'
        test04_D30.O = getMatrixFromFile(path)[0:30]
        return basic04(np.dot(test04_D30.M, (X - test04_D30.O)))

#Rastrigin’s Function
def basic05(x):
    sigma = 0
    for i in range(len(x)):
        sigma +=x[i]*x[i] - 10*math.cos(2*math.pi*x) + 10
    return sigma

def test05_D10(X):
    try:
        return basic05(np.dot(test05_D10.M, (X - test05_D10.O)))
    except AttributeError:
        path = 'utilities/M_5_D10.txt'
        test05_D10.M = getMatrixFromFile(path)
        path = 'utilities/shift_data_5.txt'
        test05_D10.O = getMatrixFromFile(path)[0:10]
        return basic05(np.dot(test05_D10.M, (X - test05_D10.O)))

def test05_D30(X):
    try:
        return basic05(np.dot(test05_D30.M, (X - test05_D30.O)))
    except AttributeError:
        path = 'utilities/M_5_D30.txt'
        test05_D30.M = getMatrixFromFile(path)
        path = 'utilities/shift_data_5.txt'
        test05_D30.O = getMatrixFromFile(path)[0:30]
        return basic05(np.dot(test05_D30.M, (X - test05_D30.O)))

if __name__ == '__main__':
    #print(basic01([0,0,0,0,0]))
    #print(basic01([1,0,0,0,0]))
    x = np.zeros(10)
    x[0] = 1
    print(test01_D10(x))
    print(test01_D10(x))
    #print(getMatrixFromFile('utilities/M_1_D2.txt'))