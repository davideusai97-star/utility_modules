import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import pickle

import sys
sys.path.append(r'C:\Users\david\OneDrive\Desktop\scolastiche\magistrale\metodi_numerici\mod1\File_PY')

from blocking import blocking_k
from jackknife_chi import jackknife # type: ignore


# INIZIALIZZAZIONE
dim=[20,40,60,80,100,120,140,160]
betas={
    20:np.arange(0.454,0.460, 0.002),     #inclusivo dell'estremo finale
    40:np.arange(0.4373,0.4375+1e-10,0.0001),
    60:np.arange(0.4364,0.4365+1e-10,0.0001),
    80:np.arange(0.439,0.439+1e-10,0.0001),
    100:np.arange(0.439,0.439+1e-10,0.0001),
    120:np.arange(0.439,0.439+1e-10,0.0001),
    140:np.arange(0.440,0.440+1e-10,0.0001),
    160:np.arange(0.440,0.440+1e-10,0.0001)
}
#CREAZIONE DI UN DIZIONARIO PER LA GESTIONE DATI
magnetizzazioni={}
magnetizzazioni_abs={}
magnetizzazioni_media={}
magnetizzazioni_abs_media={}
err_magnetizzazioni_media={}
err_magnetizzazioni_abs_media={}
energie={}
chi={} # suscettibilità
c={} # calore specifico
err_chi={}

# LETTURA Q.TA' FISICHE PER LE COPPIE (L,beta)
for L in dim:
    magnetizzazioni[L]={}                       # m
    magnetizzazioni_abs[L]={}                   # |m|
    magnetizzazioni_media[L]={}                 # <m>
    magnetizzazioni_abs_media[L]={}             # <|m|>
    err_magnetizzazioni_media[L]={}
    err_magnetizzazioni_abs_media[L]={}
    energie[L]={}
    chi[L]={}                                   # (L**2)*(<m**2> - <|m|>**2) ossia chi'
    c[L]={}                                     # (L**2)*(<E**2> - <E>**2)
    err_chi[L]={}
    for beta in betas[L]:
        filename=f"b{beta:.6f}_L{L}_opt.dat"  # nome del file da leggere
        percorso_file=f".\datafolder_ising\datafolder{L}_n5\{filename}"  # costruzione del percorso completo del file da leggere
        mag=np.loadtxt(percorso_file,usecols=0) # mag è il vettore delle magnetizzazioni del singolo file
        en=np.loadtxt(percorso_file,usecols=1) # en è il vettore delle energie del singolo file
        magnetizzazioni[L][beta]=mag
        magnetizzazioni_abs[L][beta]=np.abs(mag)
        energie[L][beta]=en
        magnetizzazioni_media[L][beta],err_magnetizzazioni_media[L][beta]=blocking_k(magnetizzazioni[L][beta])  # calcolo magnetizzazione media e relativo errore per ogni coppia (L,beta)
        magnetizzazioni_abs_media[L][beta],err_magnetizzazioni_abs_media[L][beta]=blocking_k(magnetizzazioni_abs[L][beta])  # calcolo magnetizzazione assoluta media e relativo errore per ogni coppia (L,beta)

        chi[L][beta],err_chi[L][beta]=jackknife(magnetizzazioni[L][beta], L)  #calcolo di chi e relativo errore per la coppia (L,beta)
        c[L][beta]=(L**2)*(np.mean(energie[L][beta]**2)-(np.mean(energie[L][beta]))**2)
        #print(f"{beta} for L{L} done!")


# SALVATAGGIO DIZIONARI SU FILE osservabili.pkl
with open("dict2_prova.pkl", "wb") as f:
    pickle.dump({
        "chi": chi,
        "err_chi": err_chi,
        "c": c,
        "magnetizzazioni_media": magnetizzazioni_media,
        "magnetizzazioni_abs_media": magnetizzazioni_abs_media,
        "err_magnetizzazioni_media": err_magnetizzazioni_media,
        "err_magnetizzazioni_abs_media": err_magnetizzazioni_abs_media,
    }, f)