#!/usr/bin/python3
import argparse
import gzip
import pickle

def writeCipher(output, filename):
    with gzip.open(filename , 'wb') as f:
        f.write(pickle.dumps(output))
def writePlain(output, filename):
    with gzip.open(filename , 'wb') as f:
        f.write(pickle.dumps(output))
def readFromFile(filename):
    with gzip.open(filename, 'rb') as f:
        contents = pickle.loads(f.read())
    return contents
def writeToFile(filename):
    with gzip.open(filename, 'rb') as f:
        contents = pickle.loads(f.read())
    return contents
def writeKeys(Gen_matrix,G_matrix, t_val, S_matrix, H_matrix, P_matrix, filename):
    with gzip.open(filename + '.pub', 'wb') as f:
        f.write(pickle.dumps([G_matrix, t_val]))
    with gzip.open(filename + '.priv', 'wb') as f:
        f.write(pickle.dumps([S_matrix, H_matrix, P_matrix, t_val]))
    with gzip.open(filename + '.parity', 'wb') as f:
        f.write(pickle.dumps([H_matrix]))
    with gzip.open(filename + '.gen', 'wb') as f:
        f.write(pickle.dumps([Gen_matrix]))
parser = argparse.ArgumentParser()
parser.add_argument("-v", help="Enable verbose mode", action="store_true")
parser.add_argument("-vv", help="Enable very verbose mode",
					action="store_true")
parser.add_argument("-g", help="Generate key pairs", action="store_true")
parser.add_argument("-m", type=int, help="Generate key pairs")
parser.add_argument("-t", type=int, help="Generate key pairs")
parser.add_argument("-o", type=str, help="Output file (always needed)")
parser.add_argument("-e", type=str,
					help="File with data in matrices to encrypt")
parser.add_argument("-d", type=str,
					help="File with data in matrices to decrypt")
parser.add_argument("-pub", type=str, help="Key to encrypt with")
parser.add_argument("-priv", type=str, help="Key to decrypt with")
parser.add_argument("-f",help="Encrypt without errors in ciphertext", action="store_true")
''' my adds'''
parser.add_argument("-x", type=str, help="Encoded msg without errors")
parser.add_argument("-par", type=str, help="Parity matrix")
parser.add_argument("-cw", type=str,	help="Codeword")
parser.add_argument("-er", type=str,	help="error vector")
parser.add_argument("-gen", type=str,	help="Gen matrix")
args = parser.parse_args()
