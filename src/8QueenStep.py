#!/usr/bin/python
# -*- coding: utf-8 -*-
import random as rd
import numpy as np
n = 8
s = (n, n)
x = np.zeros(s)
checkseq = 1

while checkseq == 1:
    rseq = np.random.permutation(n)  # list([3,6,2,7,1,4,0,5])
    for i in range(len(rseq)):
        x[i, rseq[i]] = 1

    rdiag = True
    for i in range(len(rseq)):
        itr = [i, rseq[i]]
        a = itr[0]
        b = itr[1]
        for j in range(rseq[i], n):
            if a < n - 1 and b < n - 1:
                a = a + 1
                b = b + 1
                if x[a, b] == 1:
                    rdiag = False
                    break

    ldiag = True
    for i in range(len(rseq)):
        itr = [i, rseq[i]]
        a = itr[0]
        b = itr[1]
        for j in range(rseq[i], 0, -1):
            if a < n - 1 and b > 0:
                a = a + 1
                b = b - 1
                if x[a, b] == 1:
                    ldiag = False
                    break

    if ldiag == True and rdiag == True:
        print ('Generated Sequence', rseq)
        print("Display of the Sequence in 8 * 8")
        print(x)
        checkseq = 0
        break
    else:
        checkseq = 1
        x = np.zeros(s)
