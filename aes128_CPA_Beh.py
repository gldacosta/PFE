#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from pylab import *
import numpy as np
import os

#exec(open('aes128_CPA_behavioral_HD.py').read())

tmps1=time.time()

def HW(x):
	return bin(x).count("1")

def HD(a,b):
	return HW((a)^(b))

def ciphertext(y_ct, y_ct2):
	y_pt_int=np.zeros((NB_PLAINTEXT,16),dtype=int)
	print "		plaintext open"
	for i in range(NB_PLAINTEXT):
		for j in range(16):
			y_pt_int[i,j]=int(y_pt.read(2),16)
		y_pt.read(1)
		#print y_pt_int[i,:]
	print "		ciphertext creation"
	for i in range(NB_PLAINTEXT):
		cipherTextArray = AESCipher(y_pt_int[i,:], CipherKeyArray, CipherKeySize)
		tata = AESCipherR9(y_pt_int[i,:], CipherKeyArray, CipherKeySize)
		for m in range(IOBlockSize):
	    		y_ct.write(format(int(cipherTextArray[m],16),'02x'))
			y_ct2.write(format(int(tata[m],16),'02x'))     
		y_ct.write("\n")
		y_ct2.write("\n")

	y_ct.close()
	y_ct2.close()
	print "		ciphertext open"
	y_ct = open("./infiles/{0}_ciphertext.txt".format(NB_PLAINTEXT), "rb")
	y_ct2 = open("./infiles/{0}_ciphertext_h9.txt".format(NB_PLAINTEXT), "rb")
	y_ct_int=np.zeros((NB_PLAINTEXT,16),dtype=int)
	y_ct_int2=np.zeros((NB_PLAINTEXT,16),dtype=int)
	for i in range(NB_PLAINTEXT):
		for j in range(16):
			y_ct_int[i,j]=int(y_ct.read(2),16)
			y_ct_int2[i,j]=int(y_ct2.read(2),16)
		y_ct.read(1)
		y_ct2.read(1)	
		#print y_ct_int[i,:]
	
	return (y_ct_int, y_ct_int2, y_pt_int)


def popcount(x):
    return bin(x).count("1")

def generate_correlation_map(x, y):
    """Correlate each n with each m.
    Parameters
    ----------
    x : np.array
      Shape N X T.
    y : np.array
      Shape M X T.
    Returns
    -------
    np.array
      N X M array in which each element is a correlation coefficient.
    """
    mu_x = x.mean(1)
    mu_y = y.mean(1)
    n = x.shape[1]
    if n != y.shape[1]:
        raise ValueError('x and y must have the same number of timepoints')
    s_x = x.std(1, ddof=n - 1)
    s_y = y.std(1, ddof=n - 1)
    cov = np.dot(x,y.T) - n * np.dot(mu_x[:, np.newaxis],mu_y[np.newaxis, :])
    return cov / np.dot(s_x[:, np.newaxis], s_y[np.newaxis, :])

def testBit(int_type,nb): # donne la valeur du nb bit
	mask=1<<nb
	return((int_type&mask)/2**nb)

def xor(s1, s2):
    return tuple(a^b for a,b in zip(s1, s2))

INVSBOX = [
0x52,0x09,0x6a,0xd5,0x30,0x36,0xa5,0x38,0xbf,0x40,0xa3,0x9e,0x81,0xf3,0xd7,0xfb,
0x7c,0xe3,0x39,0x82,0x9b,0x2f,0xff,0x87,0x34,0x8e,0x43,0x44,0xc4,0xde,0xe9,0xcb,
0x54,0x7b,0x94,0x32,0xa6,0xc2,0x23,0x3d,0xee,0x4c,0x95,0x0b,0x42,0xfa,0xc3,0x4e,
0x08,0x2e,0xa1,0x66,0x28,0xd9,0x24,0xb2,0x76,0x5b,0xa2,0x49,0x6d,0x8b,0xd1,0x25,
0x72,0xf8,0xf6,0x64,0x86,0x68,0x98,0x16,0xd4,0xa4,0x5c,0xcc,0x5d,0x65,0xb6,0x92,
0x6c,0x70,0x48,0x50,0xfd,0xed,0xb9,0xda,0x5e,0x15,0x46,0x57,0xa7,0x8d,0x9d,0x84,
0x90,0xd8,0xab,0x00,0x8c,0xbc,0xd3,0x0a,0xf7,0xe4,0x58,0x05,0xb8,0xb3,0x45,0x06,
0xd0,0x2c,0x1e,0x8f,0xca,0x3f,0x0f,0x02,0xc1,0xaf,0xbd,0x03,0x01,0x13,0x8a,0x6b,
0x3a,0x91,0x11,0x41,0x4f,0x67,0xdc,0xea,0x97,0xf2,0xcf,0xce,0xf0,0xb4,0xe6,0x73,
0x96,0xac,0x74,0x22,0xe7,0xad,0x35,0x85,0xe2,0xf9,0x37,0xe8,0x1c,0x75,0xdf,0x6e,
0x47,0xf1,0x1a,0x71,0x1d,0x29,0xc5,0x89,0x6f,0xb7,0x62,0x0e,0xaa,0x18,0xbe,0x1b,
0xfc,0x56,0x3e,0x4b,0xc6,0xd2,0x79,0x20,0x9a,0xdb,0xc0,0xfe,0x78,0xcd,0x5a,0xf4,
0x1f,0xdd,0xa8,0x33,0x88,0x07,0xc7,0x31,0xb1,0x12,0x10,0x59,0x27,0x80,0xec,0x5f,
0x60,0x51,0x7f,0xa9,0x19,0xb5,0x4a,0x0d,0x2d,0xe5,0x7a,0x9f,0x93,0xc9,0x9c,0xef,
0xa0,0xe0,0x3b,0x4d,0xae,0x2a,0xf5,0xb0,0xc8,0xeb,0xbb,0x3c,0x83,0x53,0x99,0x61,
0x17,0x2b,0x04,0x7e,0xba,0x77,0xd6,0x26,0xe1,0x69,0x14,0x63,0x55,0x21,0x0c,0x7d ]

Sbox = [
0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16 ]

def SubBytes(state):
    for i in range(IOBlockSize): state[i] = Sbox[state[i]]
    return state

def InvSubBytes(state):
    for i in range(IOBlockSize): state[i] = InvSbox[state[i]]
    return state

def SubWord(word): return Sbox[word]

# state before:    0  1  2 3 4 5  6  7 8 9 10 11 12 13 14 15
# state after:     0 13 10 7 4 1 14 11 8 5  2 15 12  9  6 3

def ShiftRows(state):
	tmp13 = state[13]
	state[13] = state[1]
	state[1] = state[5]
	state[5] = state[9]
	state[9] = tmp13
	tmp15 = state[15]
	state[15] = state[11]
	state[11] = state[7]
	state[7] = state[3]
	state[3] = tmp15
	tmp2 = state[2]
	state[2] = state[10]
	state[10] = tmp2
	tmp6 = state[6]
	state[6] = state[14]
	state[14] = tmp6
	return state

def key_shift(nb):
	switcher = {
		0: 0,
		1: 13,
		2: 10,
		3: 7,
		4: 4,
		5: 1,
		6: 14,
		7: 11,
		8: 8,
		9: 5,
		10: 2,
		11: 15,
		12: 12,
		13: 9,
		14: 6,
		15: 3
		}
	return switcher.get(nb)

def InvShiftRows(state):
    tmp = state[13]
    state[13] = state[9]
    state[9] = state[5]
    state[5] = state[1]
    state[1] = tmp
    tmp = state[10]
    tmp2 = state[14]
    state[10] = state[2]
    state[14] = state[6]
    state[2] = tmp
    state[6] = tmp2
    tmp = state[11]
    state[11] = state[15]
    state[15] = state[3]
    state[3] = state[7]
    state[7] = tmp
    return state

def inv_key_shift(nb):
	switcher = {
		0: 0,
		1: 5,
		2: 10,
		3: 15,
		4: 4,
		5: 9,
		6: 14,
		7: 3,
		8: 8,
		9: 13,
		10: 2,
		11: 7,
		12: 12,
		13: 1,
		14: 6,
		15: 11
		}
	return switcher.get(nb)

def MixColumns(state):
    block = []
    while len(block) < IOBlockSize: block.append(0)
    k = 0
    while k <= IOBlockSize-4:
        block[k] = GF(2,state[k])^GF(3,state[k+1])^GF(1,state[k+2])^GF(1,state[k+3])
        block[k+1] = GF(1,state[k])^GF(2,state[k+1])^GF(3,state[k+2])^GF(1,state[k+3])
        block[k+2] = GF(1,state[k])^GF(1,state[k+1])^GF(2,state[k+2])^GF(3,state[k+3])
        block[k+3] = GF(3,state[k])^GF(1,state[k+1])^GF(1,state[k+2])^GF(2,state[k+3])
        k += 4
    return block

def GF(a, b):
    r = 0
    for times in range(8):
        if (b & 1) == 1: r = r ^ a
        if r > 0x100: r = r ^ 0x100
        # keep r 8 bit
        hi_bit_set = (a & 0x80)
        a = a << 1
        if a > 0x100:
            # keep a 8 bit
            a = a ^ 0x100
        if hi_bit_set == 0x80:
            a = a ^ 0x1b
        if a > 0x100:
            # keep a 8 bit
            a = a ^ 0x100
        b = b >> 1
        if b > 0x100:
            # keep b 8 bit
            b = b ^ 0x100
    return r

############################## AddRoundKey ##############################
def AddRoundKey(state, RoundKey):
    for i in range(IOBlockSize):
        if i < len(RoundKey): state[i] = state[i] ^ RoundKey[i]
    return state

def NextRoundKey(RoundKeyArray, NextRoundKeyPointer):
    NextRoundKey = []
    k = 0

    while len(NextRoundKey) < IOBlockSize: NextRoundKey.append(0)
    for i in range(4):
        NextRoundKey[i*4] = RoundKeyArray[NextRoundKeyPointer + k]
        NextRoundKey[i*4+1] = RoundKeyArray[NextRoundKeyPointer + k+1]
        NextRoundKey[i*4+2] = RoundKeyArray[NextRoundKeyPointer + k+2]
        NextRoundKey[i*4+3] = RoundKeyArray[NextRoundKeyPointer + k+3]
        k += 4        # next column
    return NextRoundKey


############################## KEY SCHEDULE ##############################
Rcon = [
    0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8,
    0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3,
    0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f,
    0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d,
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab,
    0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d,
    0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25,
    0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01,
    0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d,
    0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa,
    0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a,
    0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02,
    0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a,
    0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef,
    0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94,
    0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04,
    0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f,
    0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5,
    0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33,
    0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb ]

def getRconValue(num): return Rcon[num]

def RotWord(word):
    temp = word[0]
    for i in range(3): word[i] = word[i+1]
    word[3] = temp
    return word

def KeyExpansion(CipherKeyArray, CipherKeySize, expandedKeySize):
    i = 0
    rconIteration = 1
    w = [0,0,0,0]

    expandedKey = []
    while len(expandedKey) < expandedKeySize: expandedKey.append(0)

    for j in range(CipherKeySize): expandedKey[j] = CipherKeyArray[j]

    i += CipherKeySize
    while i < expandedKeySize:
        for k in range(4): w[k] = expandedKey[(i - 4) + k]

        # Every 16,24,32 bytes
        if i % CipherKeySize == 0:
            w = RotWord(w)
            for r in range(4): w[r] = SubWord(w[r])
            w[0] = w[0] ^ getRconValue(rconIteration)
            rconIteration += 1

        # For 256-bit keys, we add an extra Sbox to the calculation
        if CipherKeySize == 256/8 and (i % CipherKeySize) == IOBlockSize:
            for e in range(4): w[e] = SubWord(w[e])

        for m in range(4):
            expandedKey[i] = expandedKey[i - CipherKeySize] ^ w[m]
            i += 1

    return expandedKey

def AESCipher(PlaintextArray, CipherKeyArray, CipherKeySize):
    if CipherKeySize == 128/8: nbrRounds = 10
    elif CipherKeySize == 192/8: nbrRounds = 12
    elif CipherKeySize == 256/8: nbrRounds = 14

    state = []
    while len(state) < CipherKeySize: state.append(0)
    for i in range(CipherKeySize):
        if i < len(PlaintextArray): state[i] = PlaintextArray[i]

    RoundKeyArraySize = IOBlockSize*(nbrRounds+1)
    RoundKeyArray = KeyExpansion(CipherKeyArray, CipherKeySize, RoundKeyArraySize)

    state = AddRoundKey(state, CipherKeyArray)

    i=0
    while i < nbrRounds:
        i += 1
        state = SubBytes(state)
        state = ShiftRows(state)
        if i < nbrRounds: 
        		state = MixColumns(state) # Do not MixColumns in the last Round	
        state = AddRoundKey(state, NextRoundKey(RoundKeyArray, IOBlockSize*i))

    for j in range(IOBlockSize): 
    			state[j] = hex(state[j])
    return state

def AESCipherR9(PlaintextArray, CipherKeyArray, CipherKeySize):
    if CipherKeySize == 128/8: nbrRounds = 9
    elif CipherKeySize == 192/8: nbrRounds = 11
    elif CipherKeySize == 256/8: nbrRounds = 13

    state = []
    while len(state) < CipherKeySize: state.append(0)
    for i in range(CipherKeySize):
        if i < len(PlaintextArray): state[i] = PlaintextArray[i]

    RoundKeyArraySize = IOBlockSize*(nbrRounds+1)
    RoundKeyArray = KeyExpansion(CipherKeyArray, CipherKeySize, RoundKeyArraySize)

    state = AddRoundKey(state, CipherKeyArray)
    i=0
    while i < nbrRounds:
	i += 1
        state = SubBytes(state)
        state = ShiftRows(state)
	
	a = NextRoundKey(RoundKeyArray, IOBlockSize*i)
	

        if i < nbrRounds: 
        		state = MixColumns(state)                # Do not MixColumns in the last Round	
	
	
        state = AddRoundKey(state, a)
	
    for j in range(IOBlockSize): 
    			state[j] = hex(state[j])
			
    return state

##########################################
# key : A1D9AE128BBF2F73F68EC42B25525475 # 
##########################################
# k10 : 92E75918275353F8D3ABF156A925AF56 #
##########################################


NB_PLAINTEXT=5000 #int(input("plaintext numbers :"))
start=13000 #int(input("start :"))
delta=4500 #int(input("delta :"))
modulo=18270 #int(input("modulo :"))

IOBlockSize = 16 
CipherKeySize = int(128/8)
CipherKeyArray = [0xa1,0xd9,0xae,0x12,0x8b,0xbf,0x2f,0x73,0xf6,0x8e,0xc4,0x2b,0x25,0x52,0x54,0x75]

print 'step 1/4 : Plaintext and Ciphertext processing'

y_ct=open("./infiles/{0}_ciphertext.txt".format(NB_PLAINTEXT), "a")
y_pt=open("./infiles/{0}_plaintext.txt".format(NB_PLAINTEXT),"rb")
y_ct2=open("./infiles/{0}_ciphertext_h9.txt".format(NB_PLAINTEXT), "a")

y_ct_int, y_ct_int2 , y_pt_int = ciphertext(y_ct, y_ct2)

print 'step 2/4 : VCD file processing'

changes_parser_output = open("output_parser","r")

temps = []
changes = []
for line in changes_parser_output:
    elements = line.split(",")
    temps.append(int(elements[0]))
    changes.append(int(elements[1]))

debut=start
fin=start+delta
ts=0

for i in range(fin):
	if temps[i]>=debut and temps[i]<=fin:
		ts+=1

print ("	%d Time stamps from %dps to %dps" % (ts,debut,fin))

NB_POINT=4 #ts

print 'step 3/4 : Toggle processing'

toggle=np.zeros((NB_PLAINTEXT,NB_POINT),dtype=float)

for i in range(NB_PLAINTEXT):
	debut=i*modulo+start
	fin=i*modulo+start+delta
	a=0
	b=0
	for j in range(len(temps)-1):
		if temps[j]>=debut and temps[j]<=fin:
			if a%2==0:
				toggle[i,b]=float(chages[j])
				b+=1
			a+=1
 
print 'step 4/4 : CPA HD Processing'
      		
####CPA
for key_byte_number in range(16):
	power_hypothesis=np.zeros((NB_PLAINTEXT,256,256),dtype=int)
	CC=np.zeros((256,NB_POINT,256),dtype=float)
	for key10 in range(256):
		for key9 in range(256):
			for i in range(NB_PLAINTEXT):
				power_hypothesis[i,key10,key9]=HD(INVSBOX[y_ct_int[i,key_byte_number]^key10], INVSBOX[y_ct_int2[i,key_byte_number]^key9])
	for i in range(256):
		CC[:,:,i] = generate_correlation_map(np.transpose(power_hypothesis[:,:,i]), np.transpose(toggle))

	b=0
	for j in range(256):
		for i in range(256):
			a=max(abs(CC[i,:,j]))
			if a > b:
				index=i
				b=a
			
	print("clef %2d : 0x%2x" % (key_byte_number,index))
###CPA
tmps2=(time.time()-tmps1)
print "Execution time = %d minutes" % int(tmps2/60)
y_pt.close()
y_ct.close()
y_ct2.close()
os.remove("./infiles/{0}_ciphertext.txt".format(NB_PLAINTEXT))
os.remove("./infiles/{0}_ciphertext_h9.txt".format(NB_PLAINTEXT))