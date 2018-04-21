from math import *
import scipy.linalg
import numpy as np
import array as ar
import re


# LU Decomposition and Calculate Determinant
def lu_det():
    determ = 1
    log_determ = 0

    for k in range(0, int(n / m)):
        L_inv, U_inv, sub_determ, sub_log_determ = part2(k,k)

        for i in range((k + 1), int(n / m)):
            rightmulti(i,k,U_inv)

        for j in range((k+1), int(n/m)):
            leftmulti(k,j,L_inv)
        for i in range((k + 1), int(n / m)):
            for j in range((k + 1), int(n / m)):
                schur(i,j,k)
        determ = determ* sub_determ
        log_determ = sub_log_determ + log_determ
    return determ, log_determ





def rightmulti(i,k,U_inv):
    b = readSunMatrix(i,k)
    #print(b, U_inv)
    b = np.dot(b, U_inv)
    #print(b)
    writesubmatrix(i,k, b)

def leftmulti(k,j,L_inv):
    b= readSunMatrix(k,j)
    b = np.dot(L_inv, b)
    writesubmatrix(k,j,b)

def schur(i,j,k):
    b = readSunMatrix(i,j)
    c = readSunMatrix(i,k)
    d = readSunMatrix(k,j)
    b = b - np.dot(c,d)
    writesubmatrix(i,j,b)

def writesubmatrix(i,k,a):
    submatrix_file = "submatrix_" + str(i) + "_" + str(k)
    np.save(submatrix_file, a)



def part2(i,j):
    a = readSunMatrix(i,j)
    determ = 1
    log_determ = 0
    L, U = scipy.linalg.lu(a, permute_l = True)
    # print(P)
    #print(L)
    #print(U)
    L_inv = np.linalg.inv(L)
    U_inv = np.linalg.inv(U)
    determ = determ * (np.linalg.det(L) * np.linalg.det(U))
    log_determ += log(abs((np.linalg.det(L)))) + log(abs((np.linalg.det(U))))
    #print(np.linalg.det(L),np.linalg.det(U))
    #print(L_inv, U_inv, determ, log_determ)
    return L_inv, U_inv, determ, log_determ


def readSunMatrix(i,j):
    str1 = "submatrix_" + str(i) + "_" + str(j) + ".npy"
    megastuffed = np.load(str1)
    return megastuffed

# end
# Read the large/raw matrix and divide it into smaller block
n = int(512)
m = int(32)
lst = []
largematrix = open("m0512x0512.bin", "rb")
output = list(range(int(n / m)))
submatrix_file = []
for i in range(0, int(n / m)):
    A =[]
    for j in range(0, int(n/m)):
        A.append(np.empty([m,m]))
    for k in range(0, m):
        for j in range(0, int(n / m)):
            block = largematrix.read(8 * m)
            line = ar.array("d", block)
            for p in range(0,m):
                A[j][k,p] = line[p]

    for j in range(0, int(n / m)):
        str1 = "submatrix_" + str(i) + "_" + str(j)
        #submatrix = open(str1, "w")
        np.save(str1, A[j])
        #submatrix.close()
largematrix.close()


print (lu_det())

