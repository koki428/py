#縦軸保持率、横軸速度でプロット

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import math
import R2D2

plt.close('all')

d=R2D2.R2D2_data("../run/d299/data/")
for key in d.p:
    exec('%s=%s%s%s' % (key, 'd.p["',key,'"]'))

t=d.read_time(400,silent=True)
d.read_qq_2d(400,silent=True)
vx=d.q2['vx']

dx=(xmax-xmin)/ix
dy=(ymax-ymin)/jx
rtube=0.005*rstar

initial_position=round((0.73*rstar-xmin)/dx)

#結果が書き込んであるファイルを開く
results=[]
with open("result.txt","r") as f:
    for result in f:
        results.append(result.split())

for i in range(0,10):
    count=0
    lam="{:.2f}".format(0.05*i)
    for j in range(0,len(results)):
        if (lam == results[j][2] and float(results[j][4]) > 0):
            count=count+1
    globals()['top'+str(i)]=np.zeros(count)
    globals()['rise'+str(i)]=np.zeros(count)
    num=0
    for j in range(0,len(results)):
        vx_sum=0
        vx_count=0
        if (lam == results[j][2] and float(results[j][4]) > 0):
            globals()['top'+str(i)][num]=results[j][4]
            # for k in range(0,ix):
            #     for l in range(0,jx):
            #         x_dis=(0.73*rstar-xmin)/dx-k
            #         y_dis=(2*rtube+(ymax-4*rtube)/99*int(results[j][1]))/dy-l
            #         rr=math.sqrt(x_dis**2+y_dis**2)
            #         if (rr < 2*rtube*1.e-8):
            #             vx_sum=vx_sum+vx[k,l]
            #             vx_count=vx_count+1
            # globals()['rise'+str(i)][num]=vx_sum/vx_count
            globals()['rise'+str(i)][num]=vx[initial_position,round((2*rtube+(ymax-4*rtube)/99*int(results[j][1]))/dy)]
            num=num+1

#plot
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
fig = plt.figure(figsize=(14,8))   
plt.rcParams['font.size'] = 16
ax1=fig.add_subplot(1,1,1)
for i in range(1,10):
    ax1.plot(globals()['rise'+str(i)],globals()['top'+str(i)],linestyle='None',marker='o',label='λ='+'{:.2f}'.format(0.05*i),color=colors[i])
    # ax1.plot(globals()['top'+str(i)],globals()['rise'+str(i)],linestyle='None',marker='o',label='λ='+'{:.2f}'.format(0.05*i))
ax1.set_xlabel('velocity [cm/s]')
ax1.set_ylabel('retention [%]')
plt.legend(bbox_to_anchor=(1.01,1), borderaxespad=0)
fig.tight_layout(pad=0.5)