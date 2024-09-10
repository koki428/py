import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import R2D2

plt.close('all')

d=R2D2.R2D2_data("../run/d299/data/")
for key in d.p:
    exec('%s=%s%s%s' % (key, 'd.p["',key,'"]'))

#結果が書き込んであるファイルを開く
results=[]
with open("result.txt","r") as f:
# with open("test.txt","r") as f:
    for result in f:
        results.append(result.split())
lam_np=np.zeros(10)
for i in range(0,10):
    globals()['position{}'.format(i)]=[]
    # lam[i]=0.05*i
    lam='{:.2f}'.format(0.05*i)
    # print(lam)
    for result in results:
        if (lam == '{:.2f}'.format(float(result[2])) and float(result[4]) > 0):
           globals()['position{}'.format(i)].append(float(result[1]))
    lam_np[i]=lam

#plot
rtube = 0.005*rstar
t=d.read_time(400,silent=True)
d.read_qq_2d(400,silent=True)
vx=d.q2['vx']
vy=d.q2['vy']
# x=0.73*rstar*1.e-8
for i in range (0,10):
    fig = plt.figure(figsize=(14,5))
    plt.rcParams['font.size'] = 16
    ax1=fig.add_subplot(1,1,1)
    print(lam_np[i])
    position=np.zeros(len(globals()['position{}'.format(i)]))
    x_position=np.zeros(len(position))
    x_position[:]=(0.73*rstar-rstar)*1.e-8
    for j in range (0,len(globals()['position{}'.format(i)])):
        position[j]=globals()['position{}'.format(i)][j]
    p=ax1.streamplot(y*1.e-8,(x-rstar)*1.e-8,vy,vx,density=3,color=np.sqrt(vx**2+vy**2)*1.e-5,cmap='rainbow')
    ax1.plot((2*rtube+(ymax-4*rtube)/99*position)*1.e-8,x_position,marker='o',linestyle='None',color='red')
    fig.colorbar(p.lines,label='[km/s]')
    ax1.set_xlabel('y [Mm]')
    ax1.set_ylabel('x [Mm]')
    ax1.set_title('λ = {:.2f}'.format(lam_np[i]))
    ax1.set_xlim(ymin*1.e-8,ymax*1.e-8)
    ax1.set_ylim((xmin-rstar)*1.e-8,(xmax-rstar)*1.e-8)
    fig.tight_layout(pad=0.5)
    plt.savefig("../figs/analysis/"+'acherved_top_position'+str(lam_np[i])+'.png')