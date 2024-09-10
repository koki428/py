#縦軸時間、横軸初期位置でプロット

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import math
import R2D2

plt.close('all')

d=R2D2.R2D2_data("../run/d299/data/")
for key in d.p:
    exec('%s=%s%s%s' % (key, 'd.p["',key,'"]'))

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
    globals()['time'+str(i)]=np.zeros(count)
    globals()['position'+str(i)]=np.zeros(count)
    num=0
    for j in range(0,len(results)):
        if (lam == results[j][2] and float(results[j][4]) > 0):
            globals()['time'+str(i)][num]=results[j][3]
            globals()['position'+str(i)][num]=results[j][1]
            num=num+1

#plot
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
rtube = 0.005*rstar
fig = plt.figure(figsize=(15,7))   
plt.rcParams['font.size'] = 16
ax1=fig.add_subplot(1,1,1)
for i in range(1,10):
    ax1.plot((2*rtube+(ymax-4*rtube)/99*globals()['position'+str(i)])*1.e-8,globals()['time'+str(i)]*8,linestyle='None',marker='o',label='λ='+'{:.2f}'.format(0.05*i),color=colors[i])
ax1.set_xlabel('position [Mm]')
ax1.set_ylabel('time [h]')
ax1.set_xlim(ymin*1.e-8,ymax*1.e-8)
plt.legend(bbox_to_anchor=(1.01,1), borderaxespad=0)
fig.tight_layout(pad=0.5)