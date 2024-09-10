import numpy as np
import math
import matplotlib.pyplot as plt
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
# print(initial_position)

vx2=(vx[initial_position,:])**2
vx2_avex=np.average(vx2)
vx2_rms=math.sqrt(vx2_avex)

with open("result.txt","r") as f:
    results=[]
    for result in f:
        results.append(result.split())

lam_vx=np.zeros(10)
for i in range(0,10):
    count=0
    vx_sum=0
    lam="{:.2f}".format(0.05*i)
    for j in range (0,len(results)):
        if (results[j][2] == lam and float(results[j][4]) > 0):
            vx_sum=vx_sum+vx[initial_position,round((2*rtube+(ymax-4*rtube)/99*int(results[j][1]))/dy)]
            # vx_sum=vx_sum+(vx[initial_position,round((2*rtube+(ymax-4*rtube)/99*int(results[j][1]))/dy)])**2
            # print(round((2*rtube+(ymax-4*rtube)/99*int(results[j][1]))/dy))
            count=count+1
    if (count > 0):
        lam_vx[i]=vx_sum/count
        # lam_vx[i]=math.sqrt(vx_sum/count)

##plot
fig=plt.figure(figsize=(14,7))
plt.rcParams['font.size']=16
ax1=fig.add_subplot(1,1,1)
for i in range(0,10):
    ax1.plot(0.05*i,lam_vx[i],marker='o',linestyle='None',color='red')
ax1.hlines(vx2_rms,0,0.45,linestyle='dashed',color='blue')
ax1.set_xlabel('λ')


