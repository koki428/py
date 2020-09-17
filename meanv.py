import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import R2D2
import sys
import os

try:
    caseid
except NameError:
    print("input caseid id (3 digit)")
    caseid = 0
    caseid = input()
    caseid = "d"+caseid.zfill(3)

datadir="../run/"+caseid+"/data/"
casedir="../figs/"+caseid
os.makedirs(casedir,exist_ok=True)

d = R2D2.R2D2_data(datadir)
for key in d.p:
    exec('%s = %s%s%s' % (key, 'd.p["',key,'"]'))

try:
    n0
except NameError:
    n0 = 0
if  n0 > d.p["nd"]:
    n0 = d.p["nd"]

n0 = 0
ekm = np.zeros(nd-n0+1)

RR, TH = np.meshgrid(x,y,indexing='ij')

for n in range(n0,nd+1):
    print(n)

    d.read_vc(n,silent=True)
    ekm[n-n0] = (RR**2*sin(TH)*d.vc['vzm']**2).mean()/(RR*2*sin(TH)).mean()
