#上部に到達したかを判定し、保持率を計算し、result.txtに書き込む
import numpy as np
import math
import sympy as sym
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.axes_grid1 import make_axes_locatable
import R2D2
import cv2
import sys
import os
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN

matplotlib.use('Agg')

print("input start caseid")
caseid=input()
# caseid=int(caseid)

# print("input end caseid")
# end_caseid=input()
# end_caseid=int(end_caseid)

# for caseid in range(start_caseid,end_caseid+1):
caseid=str(caseid)
caseid="d"+caseid.zfill(3)

# datadir="../../../../../s001/c0245kikkawa/work/2dflux/run/"+caseid+"/data/"
datadir="../run/"+caseid+"/data/"

d=R2D2.R2D2_data(datadir)
for key in d.p:
    exec('%s=%s%s%s' % (key, 'd.p["',key,'"]'))

try:
    n0
except NameError:
    n0=0
if n0>d.p["nd"]:
    n0=d.p["nd"]

plt.close('all')

t0=d.read_time(0,silent=True)
initial_position=caseid[-2:]

dx=(xmax-xmin)/ix
dy=(ymax-ymin)/jx
rtube = 0.005*rsun

# roll=int(((ymax+ymin)*0.5-(2*rtube+(ymax-4*rtube)/99*int(caseid[-2:])))/dy)
print('input roll')
roll=input()
roll=int(roll)

print('input nd')
nd=input()
nd=int(nd)

#t=0での磁束の計算
t=d.read_time(0,silent=True)
d.read_qq_2d(0,silent=True)
bz=d.q2['bz']
bz=np.roll(bz,roll,axis=1)
initial_flux=0.0
bz=pd.DataFrame(bz)
initial_flux=bz.sum().sum()

#t=nの計算
# found=False
# for n in range(n0,nd+1):
flux=0.0
# print(n)
t=d.read_time(nd,silent=True)
d.read_qq_2d(nd,silent=True)
bx=d.q2['bx']
by=d.q2['by']
bz=d.q2['bz']

#平行移動
# if (n > 1):
#     roll=roll+int((ymax+ymin)*0.5/dy-cy)

bx=np.roll(bx,roll,axis=1)
by=np.roll(by,roll,axis=1)
bz=np.roll(bz,roll,axis=1)

#t=0での磁束の計算
# if n==0:
#     initial_flux=0.0
#     bz=pd.DataFrame(bz)
#     initial_flux=bz.sum().sum()

#t=nでのpsiの計算
psi=np.zeros((ix,jx))
psi[0,0]=0.0
i=0
for j in range(1,jx-1):
    psi[i,j]=psi[i,j-1]-(bx[i,j-1]*dy+4*bx[i,j]*dy+bx[i,j+1]*dy)/3
for i in range(1,ix):
    j=0
    psi[i,j]=psi[i-1,j]+by[i,j]*dx
    for j in range(1,jx-1):
        psi[i,j]=psi[i,j-1]-(bx[i,j-1]*dy+4*bx[i,j]*dy+bx[i,j+1]*dy)/3

#2値化
psi_thr=np.zeros((ix,jx))
psi_max=np.max(psi)
psi_min=100.0
while True:
    center=(psi_max+psi_min)*0.5
    for j in range(0,jx):
        for i in range(0,ix):
            if (psi[i,j] > center):
                psi_thr[i,j]=110.0
            else:
                psi_thr[i,j]=0.0

    ret,binary_psi = cv2.threshold(psi_thr, 100, 255, cv2.THRESH_BINARY)

    psi_label=binary_psi.astype('uint8')
    nlabels,labellmages,stats,centroids=cv2.connectedComponentsWithStats(psi_label)
    if (nlabels-1 > 1):
        psi_min=center
    else:
        psi_max=center
    
    # cx=centroids[1,1]
    # cy=centroids[1,0]
    # print('cy',cy)
    if (abs(psi_max-psi_min) < 1.e+3 and nlabels-1 == 1):
        # if (n != 0):
        cy=centroids[1,0]
        cx=centroids[1,1]
        r_eff=np.sqrt(stats[1,4]/math.pi)
        rr=np.zeros((ix,jx))
        for i in range(0,ix):
            for j in range(0,jx):
                rr[i,j]=np.sqrt((i-cx)**2+(j-cy)**2)
                if (rr[i,j] > 2.9*r_eff):
                    psi[i,j]=0.0
        
        psi_thr=np.zeros((ix,jx))
        psi_max=np.max(psi)
        psi_min=100.0
        while True:
            center=(psi_max+psi_min)*0.5
            for j in range(0,jx):
                for i in range(0,ix):
                    if (psi[i,j] > center):
                        psi_thr[i,j]=110.0
                    else:
                        psi_thr[i,j]=0.0

            ret,binary_psi = cv2.threshold(psi_thr, 100, 255, cv2.THRESH_BINARY)

            psi_label=binary_psi.astype('uint8')
            nlabels,labellmages,stats,centroids=cv2.connectedComponentsWithStats(psi_label)
            if (nlabels-1 > 1):
                psi_min=center
            else:
                psi_max=center
            if (abs(psi_max-psi_min) < 1.e+3):
                break
        break

#上部の到達したか判定
# if np.any(psi_thr[945,:] > 0):
# if np.any(psi_thr[475,:] > 0):
#     print('step',n)
#     achirved_step=n

#磁束の計算
bz=pd.DataFrame(bz)
psi=pd.DataFrame(psi)
flux=bz[psi > center].sum().sum()
# print('flux',flux)
retention=flux/initial_flux*100
print('retention',retention)
# found=True

# if found:
#     break

# if n == nd and not found:
#     achirved_step=0
#     retention=0.0

if (int(caseid[-3]) == 0):
    lam=0.35
elif (int(caseid[-3]) == 1):
    lam=0.40
elif (int(caseid[-3]) == 2):
    lam=0.45
else:    
    lam=0.05*(int(caseid[-3])-3)
    
    # with open ('result.txt','a') as f:
    #     f.write("{} {} {:.2f} {} {}\n".format(caseid,caseid[-2:],lam,achirved_step,retention))
    

