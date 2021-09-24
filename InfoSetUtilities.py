#!/python
import sys
import time
import numpy as np
import os
import sympy
import gzip
import pickle
import random
import itertools

'''General utility functions'''
def myWriteFile(output, filename):
    with gzip.open(filename, 'wb') as f:
        f.write(pickle.dumps(output))

def mod(x, modulus):
    numer, denom = x.as_numer_denom()
    try:
        return numer*sympy.mod_inverse(denom,modulus) % modulus

    except:
        print('Error: Unable to apply modulus to matrix')

        exit()
def clear():
    os.system('clear')

def myReadFromFile(filename):
    with gzip.open(filename, 'rb') as f:
        matrix= sympy.Matrix(pickle.loads(f.read()))
    return matrix

def permutationMatrix(size):
    P=sympy.zeros(size,size)
    position=[]
    flag=False
    i=0
    while i< size:
        pos=np.random.randint(size)
        if pos not in position:
            position.append(pos)
            i+=1
    #print (position)
    for i in range(size):
        P[i,position[i]]=1
    return P

def doLowZeros(matrix,currentRow, currentCol):
    for row in range(currentRow+1,matrix.shape[0]):
        if  matrix[row,currentCol] :
            matrix=matrix.elementary_row_op(op='n->n+km',k=1,row1=row,row2=currentRow)
            matrix=matrix%2
    return matrix
def doUpperZeros(matrix,currentRow, currentCol):
    for row in range(currentRow-1,-1,-1):
        if  matrix[row,currentCol] :
            matrix=matrix.elementary_row_op(op='n->n+km',k=1,row1=row,row2=currentRow)
            matrix=matrix%2
    return matrix
def swapRows(matrix,currentRow, currentCol):
    for row in range(currentRow,matrix.shape[0]):
        if matrix[row,currentCol]:
            matrix=matrix.elementary_row_op(op='n<->m',row1=currentRow,row2=row)
    return matrix
def isLower0(m,colStart,colStop):
    falseList=[]
    #sympy.pprint(m)
    for r in range(m.shape[0]):
        for c in range(m.shape[0]):
            if c<r and m[r,c]!=0:
                falseList.append(999)
    if 999 in falseList:
        #matrix has 1 in lower triangl
        return False
    else:
        #matrix has 0 in lower triangl,Bingo....
        return True
def getZeroXY(matrix):
    #matrix=M[:,colStart:colStop]
    xList=[]
    yList=[]
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[0]):
            if i==j and matrix[i,j]==0:
                #print('i,j',i,j)
                xList.append(i)
                yList.append(j)
    return xList,yList
#fix the matrix size into the functions
def fixDiagonal(M,colStart,colStop):
    matrix=M[:,colStart:colStop]
    sampleDiag=sympy.ones(1,colStop-colStart)
    #while
    xL,yL=getZeroXY(matrix)
    #print(xL,yL)
    while xL:
        x=xL.pop()
        y=yL.pop()
        #for r in range(matrix.shape[0]):
        r=np.random.randint(matrix.shape[0])
        #print(matrix[r,y])
        if matrix[r,y]:
            M=M.elementary_row_op(op='n->n+km',k=1,row1=x,row2=r)
            M=M%2

    if sampleDiag!=matrix.diagonal():
        return False, M
    else:
        return True,M
'''Gauss elimination with row operations'''
def Gauss_Elim(matrix,colStart, colStop):
    flag1=0
    flag2=0
    while not flag1 and not flag2:
        #sympy.pprint(matrix)
        row=-1
        for col in range(colStart,colStop):
            row+=1
            if matrix[row,col]:
                matrix=doLowZeros(matrix,row,col)
            else:
                matrix=swapRows(matrix,row,col)
        flag2,matrix=fixDiagonal(matrix,colStart,colStop)
        flag1=isLower0(matrix[:,colStart:colStop],colStart,colStop)
    row=matrix.shape[0]
    for col in range(colStop-1,colStart, -1):
        row-=1
        #print('row,col', row,col)
        matrix=doUpperZeros(matrix,row,col)

    if matrix[:,colStart:colStop]==sympy.eye(colStop-colStart):
        return 1,matrix
    else:
        return 0,matrix
        
def getB(k,p):
    lst = list(itertools.product([int(0), int(1)], repeat=k))    
    lst2=[]
    for i in lst:
         if np.count_nonzero(i)==p:                        
            mat=sympy.Matrix(i)
            matMut=mat.as_mutable()
            matMutT=matMut.T
            lst2.append(matMutT)
    return lst2