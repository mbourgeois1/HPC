from math import *
import time
import os
import numpy as np
import array as ar
import scipy.linalg
from mpi4py import MPI

start_time = time.time()

def main():
    #open up communications for MPI # of nodes/cores established from command line call:
    #mpiexec -n 8 -f machinefile python parallel_test1.py
    comm = MPI.COMM_WORLD
    #print(1)
    #print(comm.rank, comm.size)
    #KEEP IN MIND -- this code will execute on all pis!
    #SO, wherever you see something like: if comm.rank == x:
    #THIS IS HOW YOU EXECUTE ON ONLY ONE PI
    #NOTE: head node is referred to 0, the worker nodes (pis) are 1-7


    filebase="submatrix_"

    # modify as necessary
    n = 512
    m = 32

    #start LU decomp function to find determinant
    def lu_det(a):
        determ = 1
        log_determ = 0
        for k in range(0,int(n/m)):
            P, L, U = scipy.linalg.lu(a)
            L_inv = np.linalg.inv(L)
            U_inv = np.linalg.inv(U)
            determ = determ * np.linalg.det(L) * np.linalg.det(U)
            log_determ += log(abs((np.linalg.det(L)))) + log(abs((np.linalg.det(U))))
            for i in range((k+1), int(n/m)):
                a_mat_ik = a[i, k] * L_inv
                a_mat_ki = a[k, i] * U_inv
				for i in range((k+1), int(n/m)):
					for j in range((k+1), int(n/m)):
						a_mat_jk = a[i, j] - a[i, k] * a[k, j]
					return determ, log_determ
    #end LU decomp function to find determinant

    block_count = 1 # this will keep track of which processor / pi we are doing work on.. not using rank = 0 to do actual work

    if comm.rank == 0:  #only do this if head node
       #print(2)
        determs = []    #make a list of results arrays

        #read the large/raw matrix and divide it into smaller blocks
        largematrix = open("m0512x0512.bin", "rb")
        output = list(range(int(n/m)))
        submatrix_file = []
        for i in range(0, int(n/m)):
            for j in range(0, int(n/m)):
                str1 = "submatrix_" + str(i) + "_" + str(j)
                output[j] = open(str1, "w")
            for k in range(0,m):
                for j in range(0, int(n/m)):
                    block = largematrix.read(8 * m)
                    line = ar.array("d", block)
                    output[j].write(str(line.tolist()) + "\n")
            for j in range(0, int(n/m)):
                output[j].close()
        #end of reading large matrix

    for i in range(0,int(n/m)):
        for j in range(0,int(n/m)):
            filestr = filebase+ str(i) + "_" + str(j)
            #print(3)
            #next read in each file but only on head node
            if comm.rank == 0:  #only do this if head node
                #print(4)
                submatrix_file = open(filestr, "r")
                megastuffed = []
                for k in range(0, m):
                    doublestuffed = submatrix_file.readline()
                    singlestuffed = doublestuffed.strip('[')
                    singlestuffed = singlestuffed.replace(']', '')
                    singlestuffed = singlestuffed.split(",")
                    singlestuffed = list(map(float, singlestuffed))
                    megastuffed.append(singlestuffed)
                # Reshape the list into matrix shape
                megastuffed = np.reshape(megastuffed, (m,m))
                #now send array to a selected pi (block_count)
                comm.Send([megastuffed, MPI.DOUBLE], dest = block_count, tag = 99)
                #Ignore the tags for now

            if comm.rank == block_count:    #only executed if processor = block_count
                #make a place to receive the matrix to do work on
                my_block = np.empty(m * m, dtype=np.float64)
                my_block = np.reshape(my_block, (m, m))
                #Next line is to receive the matrix into my_block from the head node (0)
                comm.Recv([my_block , MPI.DOUBLE], source = 0, tag=99)
                #print(my_block, comm.rank)

            if comm.rank == block_count:
                # here is where work can be done on each block (i.e. LU decomp)
                #result = np.linalg.det(my_block)
                determ, log_determ = lu_det(my_block)
                #result = lu_det(my_block)
                my_determ = np.empty(1, dtype=np.float64)
                my_determ[0] = determ
                #you have to send back to the head node... but you can't send back a float/double -- so here's a 1x1 array
                comm.Send([my_determ, MPI.DOUBLE], dest=0, tag=88)

            if comm.rank == 0:
                curr_determ = np.empty(1, dtype=np.float64)
                comm.Recv([curr_determ, MPI.DOUBLE], source=block_count, tag=88)
                determs.append(curr_determ)

            if block_count < comm.size -2:
                block_count+=1
            else:
                block_count = 1
                comm.Barrier()  # wait for everybody to synchronize _here_

    if comm.rank == 0:
        print(determs)
		final_det = np.reshape(determs, (m/2, m/2))
		final_det = lu_det(final_det)
		print(final_det)

    """
    for r in range(comm.size):
        if comm.rank == r:
            print("[%d] %s" % (comm.rank, my_block))
        comm.Barrier()
    """

    #a = np.fromfile(fname)







if __name__ == '__main__':
    main()
print ("--- %s seconds ---" % (time.time() - start_time))
