#箱ひげ図を作成するプログラム

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import math

# matplotlib.use('Agg')

plt.close('all')

#結果が書き込んであるファイルを開く
results=[]
with open("result.txt","r") as f:
# with open("test.txt","r") as f:
    for result in f:
        results.append(result.split())

for i in range(0,10):
    globals()['retention{}'.format(i)]=[]
    lam=0.05*i
    lam='{:.2f}'.format(lam)
    print(lam)
    for result in results:
        if (lam == '{:.2f}'.format(float(result[2])) and float(result[4]) > 0):
           globals()['retention{}'.format(i)].append(float(result[4]))
    
#熱対流なし計算の結果
no_results=[]
with open("no_convection.txt","r") as f:
    for no_result in f:
        no_results.append(no_result.split())

for i in range(0,10):
    lam=0.05*i
    lam='{:.2f}'.format(lam)
    for no_result in no_results:
        if (lam == '{:.2f}'.format(float(no_result[2]))):
            globals()['no_retention{}'.format(i)]=float(no_result[4])

#plot
fig = plt.figure(figsize=(12,8))
plt.rcParams['font.size'] = 16
ax1=fig.add_subplot(1,1,1)
ax1.boxplot([retention0,retention1,retention2,retention3,retention4,retention5,retention6,retention7,retention8,retention9],labels=['0.00','0.05','0.10','0.15','0.20','0.25','0.30','0.35','0.40','0.45'],whis=[0, 100])
for i in range (1,9):
    plt.text(i+1.15,np.max(globals()['retention{}'.format(i)])-1,'{:.1f}'.format(np.max(globals()['retention{}'.format(i)])))
    plt.text(i+1.15,np.min(globals()['retention{}'.format(i)])-1.5,'{:.1f}'.format(np.min(globals()['retention{}'.format(i)])))
    ax1.plot(i+1,np.average(globals()['retention{}'.format(i)]),linestyle='None',marker='o',color='red')
    ax1.plot(i+1,globals()['no_retention{}'.format(i)],linestyle='None',marker='o',color='blue')
    plt.text(i+1.05,np.average(globals()['retention{}'.format(i)])-1.1,'{:.1f}'.format(np.average(globals()['retention{}'.format(i)])))
    plt.text(i+0.4,globals()['no_retention{}'.format(i)]-1.1,'{:.1f}'.format(globals()['no_retention{}'.format(i)]))
plt.text(10.15,np.max(globals()['retention{}'.format(9)])-1,'{:.1f}'.format(np.max(globals()['retention{}'.format(9)])))
plt.text(10.15,np.min(globals()['retention{}'.format(9)])-1.5,'{:.1f}'.format(np.min(globals()['retention{}'.format(9)])))
ax1.plot(10,np.average(globals()['retention{}'.format(9)]),linestyle='None',marker='o',color='red',label='average')
ax1.plot(10,globals()['no_retention{}'.format(9)],linestyle='None',marker='o',color='blue',label='no convection')
plt.text(9.4,globals()['no_retention{}'.format(9)]-1.1,'{:.1f}'.format(globals()['no_retention{}'.format(9)]))
plt.text(10.05,np.average(globals()['retention{}'.format(9)])-1.1,'{:.1f}'.format(np.average(globals()['retention{}'.format(9)])))
ax1.set_xlabel('λ')
ax1.set_ylabel('retention [%]')
ax1.set_xlim(0.5,10.7)
ax1.set_ylim(-3,100) 
plt.legend()
fig.tight_layout(pad=0.5)