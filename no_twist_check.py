import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import math
import R2D2
import cv2
import pandas as pd
import time
from tqdm import tqdm
# from mpl_toolkits.axes_grid1 import make_axes_locatable

plt.close('all')
matplotlib.use('Agg')

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
    pngdir="../figs/test/"

    d=R2D2.R2D2_data(datadir)
    for key in d.p:
        exec('%s=%s%s%s' % (key, 'd.p["',key,'"]'))
    
    try:
        n0
    except NameError:
        n0=0
    if n0>d.p["nd"]:
        n0=d.p["nd"]
    
    t0=d.read_time(0,silent=True)

    dx=(xmax-xmin)/ix
    dy=(ymax-ymin)/jx
    rtube = 0.005*rsun

    #平行移動
    roll=int(((ymax+ymin)*0.5-(2*rtube+(ymax-4*rtube)/99*int(caseid[-2:])))/dy)

    #t=nの計算
    fig=plt.figure(figsize=(16,8))
    found=False
    for n in tqdm(range(n0,nd+1)):
        # print(n)
        t=d.read_time(n,silent=True)
        d.read_qq_2d(n,silent=True)
        bx=d.q2['bx']
        by=d.q2['by']
        bz=d.q2['bz']
        ro=d.q2['ro']
        Ro0,tmp=np.meshgrid(ro0,y,indexing='ij')
        Ro=ro+Ro0

        #平行移動
        if (n > 0):
            roll=roll+int((ymax+ymin)*0.5/dy-cy)
        bx=np.roll(bx,roll,axis=1)
        by=np.roll(by,roll,axis=1)
        bz=np.roll(bz,roll,axis=1)
        ro=np.roll(ro,roll,axis=1)
        Ro=np.roll(Ro,roll,axis=1)


        #t=0での磁束の計算
        if (n==0):
            initial_flux=0.0
            bz_pd=pd.DataFrame(bz)
            initial_flux=bz_pd.sum().sum()

        #アルフベン速度の計算
        alfven=bz/np.sqrt(4*np.pi*Ro)

        #2値化
        alfven_thr=np.zeros((ix,jx))
        alfven_max=np.max(alfven)
        alfven_min=0.0
        # alfven_min=np.min(alfven)
        # print('alfven max',alfven_max)
        # print('alfven min',alfven_min)
        # while True:
        threshold=(alfven_max+alfven_min)*0.5
        for j in range(0,jx):
            for i in range(0,ix):
                # if (alfven[i,j] > threshold):
                if (alfven[i,j] > alfven_max*0.05):
                    alfven_thr[i,j]=11.0
                else:
                    alfven_thr[i,j]=0.0
        ret,binary_alfven=cv2.threshold(alfven_thr,10,255,cv2.THRESH_BINARY)

        alfven_label=binary_alfven.astype('uint8')
        nlabels,labels,stats,centroids=cv2.connectedComponentsWithStats(alfven_label)
            # break
            # if (nlabels-1 >1):
            #     alfven_min=threshold
            # else:
            #     alfven_max=threshold
            
            # if (abs(alfven_max-alfven_min) < 1.e+5):
            #     print('threshold',threshold)
            #     print('nlabels',nlabels)
            #     break
        
        # 最大のものを取得
        max_flux=0
        max_label=0
        flux=np.zeros(nlabels+1)
        labels_main=np.zeros((ix,jx))
        labels_pd=pd.DataFrame(labels)
        bz_pd=pd.DataFrame(bz)
        for i in range(1,nlabels):
            flux[i]=bz[labels_pd == i].sum().sum()
            if (flux[i] > max_flux):
                max_label=i
                max_flux=flux[i]
                cy=centroids[max_label,0]
            
                labels_main=labels_pd[labels_pd == max_label]
                
        #上部に到達したか判定
        if (np.any(labels[475,:] == max_label)):
            # print('step',n)
            achirved_step=n
            retention=flux[max_label]/initial_flux*100
            # print(caseid,'reached retention',retention)
            # nd=n
            found=True

            #plot
            plt.rcParams['font.size']=16

            ax1=fig.add_subplot(2,2,1,aspect='equal')
            ax2=fig.add_subplot(2,2,2,aspect='equal')
            ax3=fig.add_subplot(2,2,3,aspect='equal')
            ax4=fig.add_subplot(2,2,4,aspect='equal')
            

            ax1.pcolormesh(y*1.e-8,(x-rsun)*1.e-8,alfven,cmap='inferno')
            ax1.set_xlabel('y [Mm]')
            ax1.set_ylabel('x [Mm]')
            ax1.set_title('alfven speed')

            ax2.pcolormesh(y*1.e-8,(x-rsun)*1.e-8,labels)
            ax2.set_xlabel('y [Mm]')
            ax2.set_ylabel('x [Mm]')
            ax2.set_title('alfven labels')

            ax3.pcolormesh(y*1.e-8,(x-rsun)*1.e-8,bz,cmap='gist_stern',vmin=0.0)
            ax3.set_xlabel('y [Mm]')
            ax3.set_ylabel('x [Mm]')
            ax3.set_title('bz')

            ax4.pcolormesh(y*1.e-8,(x-rsun)*1.e-8,labels_main)
            ax4.set_xlabel('y [Mm]')
            ax4.set_ylabel('x [Mm]')
            ax4.set_title('main tube')

            ax1.annotate("t = "+str(n*8)+" [hours]", xy=(0.04,0.90), xycoords="figure fraction",fontsize=18, color='black')

            # if(n == n0):
            #     fig.tight_layout(pad=0.5)
            fig.tight_layout(pad=0.5)

            plt.savefig(pngdir+caseid+"_alfven_main"+'{0:08d}'.format(n)+".png")
            
            if(n != nd):
                plt.clf()

        if found:
            break

        if (n == nd and not found):
            achirved_step=0
            retention=0.0
            # print('not found')
            break
    
    if (int(caseid[-3]) == 0):
        lam=0.35
    elif (int(caseid[-3]) == 1):
        lam=0.40
    elif (int(caseid[-3]) == 2):
        lam=0.45
    else:    
        lam=0.05*(int(caseid[-3])-3)
    
    # with open ('result.txt','a') as f:
    with open ('result_alfven.txt','a') as f:
        f.write("{} {} {:.2f} {} {}\n".format(caseid,caseid[-2:],lam,achirved_step,retention))
    



        