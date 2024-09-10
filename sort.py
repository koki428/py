import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib

results=[]
with open("result.txt","r") as f:
    for result in f:
        results.append(result.split())

for i in range(0,len(results)):
    for j in range(0,len(results)-1):
        if (len(results[j][0]) == 4):
            caseid1=results[j][0][-3:]
        elif (len(results[j][0]) == 5):
            caseid1=results[j][0][-4:]

        if (len(results[j+1][0]) == 4):
            caseid2=results[j+1][0][-3:]
        elif (len(results[j+1][0]) == 5):
            caseid2=results[j+1][0][-4:]
        
        if (int(caseid1) > int(caseid2)):
            results[j],results[j+1]=results[j+1],results[j]

with open("result.txt","w") as f:
    for i in range(0,len(results)):
        f.write("{} {} {} {} {}\n".format(results[i][0],results[i][1],results[i][2],results[i][3],results[i][4]))

    

