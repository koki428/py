#縦軸保持率、横軸時間でプロット

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
    globals()['top'+str(i)]=np.zeros(count)
    globals()['time'+str(i)]=np.zeros(count)
    num=0
    for j in range(0,len(results)):
        if (lam == results[j][2] and float(results[j][4]) > 0):
            globals()['top'+str(i)][num]=results[j][4]
            globals()['time'+str(i)][num]=results[j][3]
            num=num+1
    if (count > 0):
        globals()['a'+str(i)],globals()['b'+str(i)]=np.polyfit(globals()['time'+str(i)],globals()['top'+str(i)],1)
        # globals()['a'+str(i)],globals()['b'+str(i)],globals()['c'+str(i)]=np.polyfit(globals()['time'+str(i)],globals()['top'+str(i)],2)
        globals()['yfit'+str(i)]=globals()['a'+str(i)]*globals()['time'+str(i)]+globals()['b'+str(i)]
        # globals()['yfit'+str(i)]=globals()['a'+str(i)]*globals()['time'+str(i)]**2+globals()['b'+str(i)]*globals()['time'+str(i)]+globals()['c'+str(i)]
        # print(globals()['a'+str(i)])

#plot
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
rtube = 0.005*rstar
fig = plt.figure(figsize=(15,7))   
plt.rcParams['font.size'] = 16
ax1=fig.add_subplot(1,1,1)
for i in range(1,10):
    ax1.plot(globals()['time'+str(i)]*8,globals()['top'+str(i)],linestyle='None',marker='o',label='λ='+'{:.2f}'.format(0.05*i),color=colors[i])
    ax1.plot(globals()['time'+str(i)]*8,globals()['yfit'+str(i)],color=colors[i])
    # plt.text(np.max(globals()['time'+str(i)])*8,globals()['yfit'+str(i)][len(globals()['yfit'+str(i)])-1],'{:.2f}'.format(globals()['a'+str(i)]))
    # plt.text(np.max(globals()['time'+str(i)])*8,np.min(globals()['yfit'+str(i)]),'{:.2f}'.format(globals()['a'+str(i)]))
plt.text(390,2,"{:.2f}".format(a1))
plt.text(335,13,"{:.2f}".format(a2))
plt.text(415,12,"{:.2f}".format(a3))
plt.text(320,35,"{:.2f}".format(a4))
plt.text(555,20,"{:.2f}".format(a5))
plt.text(300,52,"{:.2f}".format(a6))
plt.text(340,58,"{:.2f}".format(a7))
plt.text(690,43,"{:.2f}".format(a8))
plt.text(740,47,"{:.2f}".format(a9))
plt.text(320,1,"λ=0.05",color=colors[1])
plt.text(280,18,"λ=0.10",color=colors[2])
plt.text(380,18,"λ=0.15",color=colors[3])
plt.text(300,40,"λ=0.20",color=colors[4])
plt.text(520,25,"λ=0.25",color=colors[5])
plt.text(270,56,"λ=0.30",color=colors[6])
plt.text(300,62,"λ=0.35",color=colors[7])
plt.text(580,47,"λ=0.40",color=colors[8])
plt.text(600,55,"λ=0.45",color=colors[9])
ax1.set_xlabel('time [h]')
ax1.set_ylabel('retention [%]')
# ax1.set_xlim(ymin*1.e-8,ymax*1.e-8)
plt.legend(bbox_to_anchor=(1.01,1), borderaxespad=0)
fig.tight_layout(pad=0.5)