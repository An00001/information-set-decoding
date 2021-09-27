#!/usr/bin/python3
import argparse
import sympy
import gzip
import pickle
import itertools
from InfoSetUtilities import *
from McElieceUtil import *


def stern(c,H,t,p,l,e):
    realErrorV=myReadFromFile(e)    
    rawH=myReadFromFile(H) 
    n=rawH.shape[1] 
    k= rawH.shape[1]  - rawH.shape[0] 
    halfK=int(k/2)   
    #print('k,k/2=', k, int(k/2))
    cword=myReadFromFile(c)   
    syndr=(cword*rawH.T).applyfunc(lambda x: mod(x,2))
    #I=sympy.eye(rawH.shape[0])
    flag1=1
    attempts=0
    time.sleep(1)
    #Algorithm inits
    while flag1 :
        attempts+=1
        restart=0
        flag2=1
        #clear()
        print("Stern attempt number", attempts )
        #Gauss Elim. starts
        while flag2:
            print("Creating P...")
            P=permutationMatrix(n)
            HP=(rawH*P).applyfunc(lambda x: mod(x,2))
            print("Attempting Gaussian elimination...")
            check,primeH=Gauss_Elim(HP,k,n)
            #Q=HP[:,k:n].inv_mod(2)            
            if check:
                print('Finding Q...')
                Q=HP[:,k:n].inv_mod(2)                
                A=primeH[0:l,0:halfK]                
                B=primeH[0:l,halfK:k]
                C=primeH[l:n-k,0:halfK]
                D=primeH[l:n-k,halfK:k]
                #Inv=(HP*HP.T).inv_mod(2)
                #Q1=(primeH*HP.T*Inv).applyfunc(lambda x: mod(x,2) )                
                flag2=0
                break
            else:
                restart=1
                break
        if restart:
            print("Unable to perform Gaussian elimination, restarting algorithm...")
            time.sleep(1)
            continue   
        #c̃ = c̃L1 c̃L2 c̃M c̃R 
        '''        
        primeCwd=(cword*P).applyfunc(lambda x: mod(x,2))    
        pCwdL1=primeCwd[:,0:halfK]
        pCwdL2=primeCwd[:,halfK:k]
        pCwdM=primeCwd[:,k:l]
        pCwdR=primeCwd[:,l:n]
        '''
        #s̃ = s̃ℓ s̃R
        primeSyndr=(syndr*Q.T).applyfunc(lambda x: mod(x,2))
        pSyndrl=primeSyndr[:,0:l]
        pSyndrR=primeSyndr[:,l:n-k]
        #vecB=B^k/2(p)
        vecB=getB(halfK,p)
        #sympy.pprint(B)
        #errorV=sympy.zeros(n)
        for eL1 in range(0,len(vecB)-1):            
            for eL2 in range(eL1+1,len(vecB)):                
                if pSyndrl==((vecB[eL1]*A.T).applyfunc(lambda x: mod(x,2))+(vecB[eL2]*B.T).applyfunc(lambda x: mod(x,2))).applyfunc(lambda x: mod(x,2))  :
                    p1=(vecB[eL1]*C.T).applyfunc(lambda x: mod(x,2))+(vecB[eL2]*D.T).applyfunc(lambda x: mod(x,2))
                    prErrR=(pSyndrR+p1).applyfunc(lambda x: mod(x,2))
                    lzero=sympy.zeros(1,l)
                    primeErrorV=vecB[eL1].row_join(vecB[eL2]).row_join(lzero).row_join(prErrR)  
                                
                    toBrake=1
                    break
                else:
                    toBrake=0
               
            if toBrake:        
                errorV=(primeErrorV*P.T).applyfunc(lambda x: mod(x,2))
                break
            else:
                errorV=sympy.zeros(1,1)
            

        if t==np.count_nonzero(errorV) :
            print("Success, wt(e)=w=",t, ", error vector found ",sympy.pretty(errorV), ' and the real is ',sympy.pretty(realErrorV))
            #print ('syndr=',sympy.pretty(syndr), 'primeSyndr', sympy.pretty(isSyndr))
            flag1=0
        else:
            print('Weight found = ', np.count_nonzero(errorV),'. No correct  error vector found, restarting...')
            time.sleep(1)
            continue
        


parser = argparse.ArgumentParser()
#parser.add_argument("-v", help="Enable verbose mode", action="store_true")
parser.add_argument("-c", type=str,	help="File with data in matrices to crack")
parser.add_argument("-o", type=str, help="Output file")
parser.add_argument("-pub", type=str, help="Public Key")
''' my adds'''
parser.add_argument("-cw", type=str,	help="Codeword")
parser.add_argument("-par", type=str, help="Parity matrix")
parser.add_argument("-t", type=int, help="Generate key pairs")
parser.add_argument("-er", type=str,	help="error vector")
parser.add_argument("-pErr", type=int,	help="errors in section A(stern)")
parser.add_argument("-l", type=int,	help="size of dimension l(stern)")
args = parser.parse_args()

if args.cw and args.par and args.t and args.pErr and args.l and args.er:
    stern(args.cw, args.par,args.t,args.pErr, args.l, args.er)