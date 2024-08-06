#λと保持率の関係をプロット
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib

# matplotlib.use('Agg')

plt.close('all')

#結果が書き込んであるファイルを開く
results=[]
with open("result.txt","r") as f:
# with open("test.txt","r") as f:
    for result in f:
        results.append(result.split())
#熱対流なしの結果が書き込んであるファイルを開く
no_convection=[]
with open("no_convection.txt","r") as f:
    for no in f:
        no_convection.append(no.split())
no_lam=np.zeros(10)
no_retention=np.zeros(10)
i=0
for no in no_convection:
    no_lam[i]='{:.2f}'.format(float(no[2]))
    no_retention[i]='{:.1f}'.format(float(no[4]))
    i=i+1

# for result in results:
#     print(result)
print('input start position')
start_position=input()
start_position=int(start_position)

print('input end position')
end_position=input()
end_position=int(end_position)

for position in range(start_position,end_position+1):
    lam=np.zeros(10)
    retention=np.zeros(10)
    i=0
    for result in results:
        if (result[1]==str(position).zfill(2)):
            # print(result)
            lam[i]='{:.2f}'.format(float(result[2]))
            print("lambda = ",lam)
            retention[i]='{:.1f}'.format(float(result[4]))
            print("retention = ",retention)
            i=i+1
            # print("i = ",i)

    #plot
    fig = plt.figure(num=1,figsize=(10,8))
    plt.rcParams['font.size'] = 16
    ax1=fig.add_subplot(1,1,1)
    ax1.plot(lam,retention,linestyle='None',marker='o',color='red',label='convection')
    ax1.plot(no_lam,no_retention,linestyle='None',marker='o',color='blue',label='no convection')
    ax1.set_xlabel('λ')
    ax1.set_ylabel('retention [%]')
    # ax1.set_title('retention vs λ')
    ax1.set_xlim(-0.01,0.46)
    ax1.set_ylim(-2,102)
    for i in range(0,len(retention)):
        plt.text(lam[i],retention[i],retention[i])
        plt.text(no_lam[i],no_retention[i],no_retention[i])
    plt.legend()
    plt.savefig("../figs/analysis/"+'retention_lambda_'+str(position)+'.png')
    

    
