#!/usr/bin/python3
import itertools
import math
from McElieceKeygen import *
def get_dist(a_matrix, b_matrix):
    diff_matrix = (a_matrix + b_matrix).applyfunc(lambda x: mod(x,2))
    dist = (diff_matrix * sympy.Matrix([1] * diff_matrix.shape[1]))[0]
    return dist

def checkCode(x,H):
    x=myReadFromFile(x)
    H=myReadFromFile(H)        
    sympy.pprint((x*H.T).applyfunc(lambda x: mod(x,2)))
    
def encrypt(mfile,gen, pubkey,cipherFile):
    Gen=myReadFromFile(gen)
    G_pub, t_val = readFromFile(pubkey)
    G_pub=sympy.Matrix(G_pub)
    message = myReadFromFile(mfile)
    #Encrypt the first part of the total message
    m=message[0,:]
    print('1.Plain or 2.McEliece encryption?')
    encrypt=input()
    if int(encrypt)==1:
        x=(m * Gen).applyfunc(lambda x: mod(x,2))
    elif int(encrypt)==2:
        x=(m * G_pub).applyfunc(lambda x: mod(x,2))
    else:
        print('No correct selection, exit..')
        exit()
    errorv=sympy.zeros(1,G_pub.shape[1])
    positions=[]
    i=0
    while i<t_val:
        #Find position (>k) to create error bit
        pos = random.randrange(G_pub.shape[1])
        if pos not in positions and pos>G_pub.shape[0]:
            positions.append(pos)
            errorv[0,pos]=1
            i=i+1
    c=(x+errorv).applyfunc(lambda x: mod(x,2))
    print(sympy.pretty(m), ' *encryption',encrypt,' = \n',sympy.pretty(x), ' (x) + \n',sympy.pretty(errorv),'(error) = \n', sympy.pretty(c), ' codeword')
    writeCipher(c,cipherFile)
    errorFile='m'+str(int(math.log2(Gen.shape[1])))+'t'+str(t_val)+'.realErrorV'
    writeCipher(errorv,errorFile)
    wordFile='m'+str(int(math.log2(Gen.shape[1])))+'t'+str(t_val)+'.plainWord'
    writeCipher(x,wordFile)
def decrypt(cfile, privkey, outfile):
    S_matrix, H_matrix, P_matrix, t_val = readFromFile(privkey)
    k_val = H_matrix.shape[0]
    n_val = H_matrix.shape[1]
    S_inverse = (S_matrix**-1).applyfunc(lambda x: mod(x,2))
    P_inverse = (P_matrix**-1).applyfunc(lambda x: mod(x,2))
    cipher = readFromFile(cfile)
    errors_tbit = []
    numbers = []
    for i in range(H_matrix.shape[1]):
        numbers.append(i)
    # Generate t-bit errors and syndromes
    for bits in itertools.combinations(numbers, t_val):
        et = sympy.zeros(1, H_matrix.shape[1])
        for bit in bits:
            et[bit] = 1
        st = (et * H_matrix.T).applyfunc(lambda x: mod(x,2))
        errors_tbit.append([et, st])
    message = []
    s_zeros = sympy.zeros(1,H_matrix[0])
    for c in cipher:
        print(sympy.pretty(c), end=' -> ')
        mSG = (c * P_inverse).applyfunc(lambda x: mod(x,2))
        s_mSG = (mSG * H_matrix.T).applyfunc(lambda x: mod(x,2))
        if not args.f:
            for errors in errors_tbit:
                if errors[1] == s_mSG:
                    recover = (mSG + errors[0]).applyfunc(lambda x: mod(x,2))
                    s_recover = (recover * H_matrix.T).applyfunc(
                    								   lambda x: mod(x,2))
                    mSG = recover
        mS = mSG.extract([0], list(range(k_val, n_val)))
        m = (mS *S_inverse).applyfunc(lambda x: mod(x,2))
        if(args.v): sympy.pprint(m)
        message.append(m)
    writePlain(message, outfile)
if args.vv:
    args.v = True
if args.g and args.m and args.t and args.o:
    keygen(args.m, args.t, args.o)
elif args.e and args.gen and args.pub and args.o:
    encrypt(args.e,args.gen, args.pub, args.o)
elif args.d and args.priv and args.o:
    decrypt(args.d, args.priv, args.o)
elif args.x and args.par:
    print('x*H.T= ')
    checkCode(args.x,args.par)
else:
    print(parser.format_help())