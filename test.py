import os
import time

timeList = []
fichiers = ['i01', 'i02', 'i03', 'i04', 'i05', 'i06', 'i07', 'i08', 'i09', 'i10']


i = 0
for elem in fichiers:
    cmd = 'python3.7 pacmen.py instances/' + fichiers[i]
    debut = time.time()
    os.system(cmd)
    fin = time.time()
    timeList.append(fin-debut)
    i+=1

i=0
for elem in timeList:
    print('Fichier : {0}, temps: {1}'.format(fichiers[i], timeList[i]))
    i+=1
