#!/python
import numpy as np
import argparse
import sympy
import gzip
import pickle
import random
import itertools
from itertools import *
from InfoSetUtilities import *
from McElieceUtil import *
from sympy.combinatorics import Permutation
'''
matrix=sympy.Matrix([[1,2,3,4,5,6,7,8,9,10],[1,2,3,4,6,6,7,8,9,10],[1,2,3,4,5,6,7,88,19,110],[1,2,3,4,5,6,47,8,49,10],[1,2,3,4,5,6,7,8,96,110],[1,2,3,4,5,6,7,8,9,10]])
sympy.pprint(matrix)
l=2
n=10
k=4
t=2
up=matrix[0:l,:]
down=matrix[l:6,:]
sympy.pprint(up)
Iup=up[:,k:k+l]
Idown=down[:,k+l:n]
sympy.pprint(Iup)
print(Iup.det())
Qup=Iup**-1
Qdown=Idown**-1
sympy.pprint(Qup*up)
sympy.pprint(Qdown*down)
vec1=sympy.ones(1,2)
vec0=sympy.zeros(1,3)
vec=vec1.row_join(vec0)
'''
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
#print(getB(4,1))
#sympy.pprint(getB(4,1))

B=getB(4,1)
for i in range(0,len(B)):
    sympy.pprint(B[i]*B[i].T)

def prangeVec(t,p,l,k,n):
    errorv=sympy.zeros(1,n)
    while i<t_val:
        while ii<p:
            pos = random.randrange(int(k/2))
            if pos not in positions:
                positions.append(pos)
                    errorv[0,pos]=1
                    ii+=1
        while iii<p:
            pos = random.randrange(int(k/2),k)
            if pos not in positions:
                positions.append(pos)
                    errorv[0,pos]=1
                    iii+=1
                #Πρέπει να κατανείμω τα λάθη αναλογα όπως ψάχνει ο στερν ήηη να το πάω τελειως τυχαία;;;
        while iv<t-2*p       
            pos = random.randrange(k+l,n)
            if pos not in positions:
                positions.append(pos)
                errorv[0,pos]=1
                iv+=1
    return errorv