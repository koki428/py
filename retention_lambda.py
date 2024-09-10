#縦軸保持率、横軸λでプロット

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import math

plt.close('all')

#結果が書き込んであるファイルを開く
results=[]
with open("result.txt","r") as f:
    for result in f:
        results.append(result.split())

#熱対流なし計算の結果
no_results=[]
with open("no_convection.txt","r") as f:
    for no_result in f:
        no_results.append(no_result.split())

average=np.zeros(10)
llam=np.zeros(10)
no_top=np.zeros(10)
retention_max=np.zeros(10)
for i in range(0,10):
    count=0
    lam="{:.2f}".format(0.05*i)
    for j in range(0,len(results)):
        if (lam == results[j][2] and float(results[j][4]) > 0):
            count=count+1
    globals()['top'+str(i)]=np.zeros(count)
    globals()['lam'+str(i)]=np.zeros(count)
    num=0
    for j in range(0,len(results)):
        if (lam == results[j][2] and float(results[j][4]) > 0):
            globals()['top'+str(i)][num]=results[j][4]
            globals()['lam'+str(i)][num]=results[j][2]
            num=num+1
    for j in range(0,len(no_results)):
        if (lam == no_results[j][2]):
            no_top[i]=float(no_results[j][4])

    average[i]=np.mean(globals()['top{}'.format(i)])
    llam[i]=lam
    if (count > 0):
        retention_max[i]=np.max(globals()['top{}'.format(i)])

#plot
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
fig = plt.figure(figsize=(12,8))   
plt.rcParams['font.size'] = 16
ax1=fig.add_subplot(1,1,1)
for i in range(1,10):
    ax1.plot(globals()['lam'+str(i)],globals()['top'+str(i)],linestyle='None',marker='o',color='black')
    # ax1.plot(llam[i],retention_max[i],linestyle='None',marker='o',color='orange')
    plt.text(llam[i]+0.002,retention_max[i],'{:.1f}'.format(retention_max[i]),color='orange')
    # ax1.plot(0.05*i,np.mean(globals()['top'+str(i)]),linestyle='None',marker='x',color='black')
    plt.text(llam[i]+0.002,average[i],'{:.1f}'.format(average[i]),color='red')
    plt.text(llam[i]-0.03,no_top[i],'{:.1f}'.format(no_top[i]),color='blue')
ax1.plot(llam[9],globals()['top{}'.format(9)][3],linestyle='None',marker='o',color='black',label='retention')
ax1.plot(llam,retention_max,linestyle='None',marker='o',label='max',color='orange')
plt.text(-0.025,no_top[0],no_top[0],color='blue')
ax1.plot(llam,average,linestyle='None',marker='*',label='average',markersize=10,color='red')
# plt.text(llam,average,'{:.1f}'.format(float(average)))
ax1.plot(llam,no_top,linestyle='None',marker='D',label='no convection',color='blue')
ax1.set_xlabel('λ')
ax1.set_ylabel('retention [%]')
ax1.set_xlim(-0.03,0.485)
ax1.set_ylim(-3,100)
ax1.set_xticks(llam)
plt.legend(bbox_to_anchor=(0.22,0.99), borderaxespad=0)
fig.tight_layout(pad=0.5)