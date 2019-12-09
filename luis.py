#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from pylab import *
import numpy as np
import os

vcd = open("./data.vcd","r")

line=[]
for ligne in vcd:
    line.append(ligne.split())
vcd.close()
temps=[]
ligne=[]
for i in line:
    print (i)