import numpy as np
import math as m

import sys
sys.path.append(r'C:\Users\david\OneDrive\Desktop\scolastiche\magistrale\moduli')

from module_divisors import find_divisors # type: ignore

'''
Calcola la media e la varianza di un array di dati attraverso l'algoritmo di blocking
Ritorna la media e l'ultimo valore trovato della varianza??
'''

def blocking_k(data):  
    d=data.copy()  # salvo in d i dati in ingresso passati come parametro (passo magnetizzazioni[L][beta] o energia[L][beta])
    N=len(d)
    d_media=np.mean(d)
    err_d_media=[]
    #k_values=[]
    Nfin,divisori=find_divisors(N,2) 
    for k in divisori:      #range(100,100000,500):
        #k_values.append(k)
        d1=d[:int(len(d)/k)*k]
        matrix=d1.reshape(-1,k)
        Fk=matrix.mean(axis=1) # vettore delle Fk_i
        M=Fk.size
        somma=0
        for j in range(M):
            somma+=np.power((Fk[j]-d_media),2)
        err_d_media.append(m.sqrt(somma/(M*(M-1))))

    return d_media,err_d_media[-1]  #ritorno la media dei dati in ingresso e l'ultimo valore stimato della sigma (ormai saturata)