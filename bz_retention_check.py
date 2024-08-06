#λ=0の時の保持率の計算
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

print("input start caseid")
start_caseid=input()
start_caseid=int(start_caseid)

print("input end caseid")
end_caseid=input()
end_caseid=int(end_caseid)

for caseid in range(start_caseid,end_caseid+1):
    caseid=str(caseid)
    caseid="d"+caseid.zfill(3)

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

    dx=(xmax-xmin)/ix
    dy=(ymax-ymin)/jx
    rtube = 0.005*rsun

    roll=int(((ymax+ymin)*0.5-(2*rtube+(ymax-4*rtube)/99*int(caseid[-2:])))/dy)

    #t=nの計算
    found=False
    for n in range(n0,nd+1):
        flux=0.0
        print(n)
        t=d.read_time(n,silent=True)
        d.read_qq_2d(n,silent=True)
        bx=d.q2['bx']
        by=d.q2['by']
        bz=d.q2['bz']

        #平行移動
        if (n != 0):
            roll=roll+int((ymax+ymin)*0.5/dy-cy)
        bx=np.roll(bx,roll,axis=1)
        by=np.roll(by,roll,axis=1)
        bz=np.roll(bz,roll,axis=1)

        #t=0での磁束の計算
        if (n == 0):
            initial_flux=0.0
            bz=pd.DataFrame(bz)
            initial_flux=bz.sum().sum()
        
        bz=d.q2['bz']
        bz=np.roll(bz,roll,axis=1)
        bz_thr=np.zeros((ix,jx))
        bz_max=np.max(bz)
        bz_min=1000

        while True:
            bz_center=(bz_max+bz_min)*0.5
            for i in range(0,ix):
                for j in range(0,jx):
                    if (bz[i,j] > bz_center):
                        bz_thr[i,j]=110.0
                    else:
                        bz_thr[i,j]=0.0
            
            ret,binary_bz=cv2.threshold(bz_thr,100,255,cv2.THRESH_BINARY)

            bz_label=binary_bz.astype('uint8')
            nlabels,labellmages,stats,centroids=cv2.connectedComponentsWithStats(bz_label)
            if (nlabels-1 > 1):
                bz_min=bz_center
            else:
                bz_max=bz_center
            
            if (abs(bz_max-bz_min) < 10 and nlabels-1 == 1):
                cy=centroids[1,0]
                cx=centroids[1,1]
                # print(cy)
                r_eff=np.sqrt(stats[1,4]/math.pi)
                rr=np.zeros((ix,jx))
                for i in range(0,ix):
                    for j in range(0,jx):
                        rr[i,j]=np.sqrt((i-cx)**2+(j-cy)**2)
                        if (rr[i,j] > 5*r_eff):
                            bz[i,j]=0.0
                
                bz_max=np.max(bz)
                bz_min=1000
                while True:
                    bz_center=(bz_max+bz_min)*0.5
                    for i in range(0,ix):
                        for j in range(0,jx):
                            if (bz[i,j] > bz_center):
                                bz_thr[i,j]=110.0
                            else:
                                bz_thr[i,j]=0.0
                    
                    ret,binary_bz=cv2.threshold(bz_thr,100,255,cv2.THRESH_BINARY)

                    bz_label=binary_bz.astype('uint8')
                    nlabels,labellmages,stats,centroids=cv2.connectedComponentsWithStats(bz_label)
                    if (nlabels-1 > 1):
                        bz_min=bz_center
                    else:
                        bz_max=bz_center
                    if (abs(bz_max-bz_min) < 10):
                        if (n != 0):
                            cy=centroids[1,0]
                        break
                break
        
        if (np.any(bz_thr[475,:]) > 0):
            print('step',n)
            achirved_step=n

            bz=pd.DataFrame(bz)
            flux=bz[bz > bz_center].sum().sum()
            retention=flux/initial_flux*100
            print('retention',caseid,retention)
            found=True
        
        if found:
            break

        if (n == nd and not found):
            print(caseid,'not found')
            achirved_step=0
            retention=0.0
    
    if (int(caseid[-3]) == 0):
        lam=0.35
    elif (int(caseid[-3]) == 1):
        lam=0.40
    elif (int(caseid[-3]) == 2):
        lam=0.45
    else:
        lam=0.05*(int(caseid[-3])-3)
    
    with open ('result_bz.txt','a') as f:
        f.write("{} {} {:.2f} {} {}\n".format(caseid,caseid[-2:],lam,achirved_step,retention))