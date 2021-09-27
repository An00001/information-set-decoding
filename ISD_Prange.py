#!/usr/bin/python3
import argparse
import sympy
import gzip
import pickle
import itertools
from InfoSetUtilities import *
from McElieceUtil import *

def prange(c, H, t, e):
    rawH=myReadFromFile(H)
    #per=permutationMatrix(rawH.shape[1])
    #rawH=(rawH*per).applyfunc(lambda x: mod(x,2))
    cword=myReadFromFile(c)
    realErrorV=myReadFromFile(e)
    syndr=(cword*rawH.T).applyfunc(lambda x: mod(x,2))
    #I=sympy.eye(rawH.shape[0])
    flag1=1
    attempts=0
    time.sleep(1)
    #Algorithm inits
    while flag1:
        attempts+=1
        restart=0
        flag2=1
        #clear()
        print("Prange attempt number", attempts )
        #Gauss Elim. starts
        while flag2:
            print("Creating P...")
            P=permutationMatrix(rawH.shape[1])
            HP=(rawH*P).applyfunc(lambda x: mod(x,2))
            print("Attempting Gaussian elimination...")
            check,primeH=Gauss_Elim(HP,HP.shape[1]-HP.shape[0],HP.shape[1])
            if check:
                print('Finding Q...')
                Q=HP[:,HP.shape[1]-HP.shape[0]:HP.shape[1]].inv_mod(2)
                #Inv=(HP*HP.T).inv_mod(2)
                #Q1=(primeH*HP.T*Inv).applyfunc(lambda x: mod(x,2) )
                #sympy.pprint(Q)
                #sympy.pprint(Q1)
                flag2=0
                break
            else:
                restart=1
                break
        if restart:
            print("Unable to perform Gaussian elimination, restarting algorithm...")
            time.sleep(1)
            continue
        primeSyndr=(syndr*Q.T).applyfunc(lambda x: mod(x,2) )
        zeroVec=sympy.zeros(1,HP.shape[1]-HP.shape[0])
        primeErrorV=zeroVec.row_join(primeSyndr)
        #primeErrorV=primeSyndr.row_join(zeroVec)
        errorV=(primeErrorV*P.T).applyfunc(lambda x: mod(x,2))
        isSyndr=(errorV*rawH.T).applyfunc(lambda x: mod(x,2))
        if int(t)==np.count_nonzero(errorV) :
            print("Success, wt(e)=w=",t, ", error vector found ",sympy.pretty(errorV), ' and the real is ',sympy.pretty(realErrorV))
            if errorV==realErrorV:
                print('Vectors are the same.')
            else:
                print('Vectors are not the same.')
            #print ('syndr=',sympy.pretty(syndr), 'primeSyndr', sympy.pretty(isSyndr))
            flag1=0
        else:
            print('Weight found = ', np.count_nonzero(primeSyndr),'. No correct  error vector found, restarting...')
            time.sleep(1)
            continue

def mod(x, modulus):
    numer, denom = x.as_numer_denom()
    if denom % modulus == 0:
        denom = int(denom/modulus)
    try:
        return numer*sympy.mod_inverse(denom,modulus) % modulus
    except:
        raise ValueError('Unable to apply modulus to matrix')
        exit()

parser = argparse.ArgumentParser()
parser.add_argument("-v", help="Enable verbose mode", action="store_true")
parser.add_argument("-c", type=str,	help="File with data in matrices to crack")
parser.add_argument("-o", type=str, help="Output file")
parser.add_argument("-pub", type=str, help="Public Key")
''' my adds'''
parser.add_argument("-cw", type=str,	help="Codeword")
parser.add_argument("-par", type=str, help="Parity matrix")
parser.add_argument("-t", type=int, help="Generate key pairs")
parser.add_argument("-er", type=str,	help="error vector")
args = parser.parse_args()

if args.cw and args.par and args.t and args.er:
    prange(args.cw, args.par,args.t,args.er)
