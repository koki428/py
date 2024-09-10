#同じλで上部に到達した個数をカウントし、グラフにする

import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib

# matplotlib.use('Agg')

plt.close('all')

#結果が書き込んであるファイルを開く
results=[]
with open("result.txt","r") as f:
# with open("result_back.txt","r") as f:
# with open("test.txt","r") as f:
    for result in f:
        results.append(result.split())

top=np.zeros(10)
lam=np.zeros(10)
for i in range(0,10):
    count=0
    lam[i]="{:.2f}".format(0.05*i)
    for j in range(0,len(results)):
        if (lam[i] == float(results[j][2]) and float(results[j][4]) > 0):
            print(results[j][0])
            count=count+1
    top[i]=count

#plot
fig = plt.figure(figsize=(10,8))
plt.rcParams['font.size'] = 16
ax1=fig.add_subplot(1,1,1)
ax1.bar(lam,top,width=0.04,label='count')
ax1.set_xlabel('λ')
ax1.set_ylabel('count')
ax1.set_xticks(lam)
for i in range(0,10):
    plt.text(lam[i]-0.005,top[i]+0.3,int(top[i]))
plt.legend()
fig.tight_layout(pad=0.5)
