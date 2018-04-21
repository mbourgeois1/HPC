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
    b = b * U_inv
    writesubmatrix(i,k, b)

def leftmulti(k,j,L_inv):
    b= readSunMatrix(k,j)
    b = b * L_inv
    writesubmatrix(k,j,b)

def schur(i,j,k):
    b = readSunMatrix(i,j)
    c = readSunMatrix(i,k)
    d = readSunMatrix(k,j)
    b = b - c*d
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
    # print(L)
    # print(U)
    L_inv = np.linalg.inv(L)
    U_inv = np.linalg.inv(U)
    determ = determ * (np.linalg.det(L) * np.linalg.det(U))
    log_determ += log(abs((np.linalg.det(L)))) + log(abs((np.linalg.det(U))))
    return L_inv, U_inv, determ, log_determ

def readSunMatrix(i,j):
    str1 = "submatrix_" + str(i) + "_" + str(j) + ".npy"
    megastuffed = np.load(str1)
    return megastuffed

# end
# Read the large/raw matrix and divide it into smaller block
n = int(16)
m = int(8)
lst = []
largematrix = open("m0016x0016.bin", "rb")
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

# end of reading large matrix


# # Read the submatrix files and convert the submatrix into lists
# determinant_megastuffed=[]
# for i in range(0, int(n / m)):
#     for j in range(0, int(n / m)):
#
#         # Reshape the list into matrix shape
#         #megastuffed = np.reshape(megastuffed, (m,m))
#
#         # Calculate the determinant and log determinant of submatrix by using LU factorization
#         determinant_megastuffed.append(lu_det())
#         print(determinant_megastuffed)
#         #print('The determinant and log determinant are' + str(determinant_megastuffed))

#print(len(determinant_megastuffed))
#determinant_megastuffed=np.reshape(determinant_megastuffed,(-1, int(sqrt(len(determinant_megastuffed)))))
final_determinant=lu_det()
print (final_determinant)







        # submatrix_file = open("submatrix_0_0")
        # blockmatrix=[]
        # for i in range (0,(n/m)):
        #     doublesub=submatrix_file.readline()
        #     doublesub1=doublesub.strip('[')
        #     doublesub1 = doublesub1.replace(']','')
        #     doublesub1=doublesub1.split(",")
        #     doublesub1 = list(map(float, doublesub1))
        #     blockmatrix.append(doublesub1)

        # blockmatrix=np.reshape(blockmatrix,(-1, int(len(blockmatrix))))
        # #print(blockmatrix)

        # b=lu_det(blockmatrix)
        # print b






        # print(main())
        # a = np.arange(16).reshape(4, 4)
        # print(np.linalg.det(a), log(abs(np.linalg.det(a))))
