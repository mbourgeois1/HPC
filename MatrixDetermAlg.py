from math import *
import scipy.linalg
import numpy as np
#from array_split
import array as ar
import mpi4py as MPI


# fname = "m0016x0016.bin"
# a = np.fromfile(fname)
# a_mat = np.reshape(a,(-1, int(sqrt(len(a)))))
#
#
#
#
# print(a_mat)

n = int(16)
m = int(4)
lst = []
largematrix = open("m0016x0016.bin", "rb")
output = list(range(int(n/m)))
submatrix_file = []
for i in range(0,int(n/m)):
    for j in range(0,int(n/m)):
        str1 = "submatrix_" + str(i) + "_" + str(j)
        output[j] = open(str1, "w")
    for k in range(0,m):
        for j in range(0,int(n/m)):
            block = largematrix.read(8*m)
            #print(block)
            line = ar.array("d", block)
            #print(line)
            output[j].write(str(line.tolist())+ "\n")
    for j in range(0,int(n/m)):
        output[j].close()

#a=np.fromstring(submatrix_0-0)
#print(a)
#doublesub=list(map("d'", submatrix_0_0))
#submatrix_file = open(str1, "r")
#lst=list(submatrix_file)
#print(lst)

# doublesub = []
# with open("submatrix_0_0") as myfile:
#     array = myfile.readlines()
#     #for line in myfile:
#      #   doublesub.append(line)
# arry1 = array.astype(np.float)
# print(arry1)

#megastuffed = []

for i in range(int(n/m)):
    for j in range(int(n/m)):
        submatrix_file = open("submatrix_"+ str(i) + "_" + str(j) , "r")
        doublestuffed = submatrix_file.readline(j)
        singlestuffed = doublestuffed.strip('[')
        singlestuffed = singlestuffed.replace(']','')
        singlestuffed = singlestuffed.split(",")
        singlestuffed = list(map(float,singlestuffed))
        #put singlestuffed into megastuffed_i_j

















# #submatrix_file = open("submatrix_0_0","r")
#
# doublesub=submatrix_file.readline()
#
#
#
#
# doublesub1=doublesub.strip('[')
# doublesub1 = doublesub1.replace(']','')
#
# doublesub1=doublesub1.split(",")
# doublesub1 = list(map(float, doublesub1))
# print(doublesub1)




# def main():
#     determ = 1
#     log_determ = 0
#     a = np.arange(n).reshape(m, m)
#     for k in range(0,int(n/m)):
#         P, L, U = scipy.linalg.lu(a)
#         L_inv = np.linalg.inv(L)
#         U_inv = np.linalg.inv(U)
#         determ = determ * np.linalg.det(L)*np.linalg.det(U)
#         log_determ += log(abs((np.linalg.det(L)))) + log(abs((np.linalg.det(U))))
#         for i in range((k+1),int(n/m)):
#             a_mat_ik = a[i,k] * L_inv
#             a_mat_ki = a[k,i] * U_inv
#             for i in range((k+1),int(n/m)):
#                 for j in range((k+1),int(n/m)):
#                     a_mat_jk = a[i,j] - a[i,k] * a[k,j]
#                 return determ, log_determ
#
#
# print(main())
# a = np.arange(16).reshape(4, 4)
#print(np.linalg.det(a), log(abs(np.linalg.det(a))))