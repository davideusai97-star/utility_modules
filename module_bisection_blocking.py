import numpy as np
from module_show_matrix import show_matrix # type: ignore

'''
Blocking algorithm per calcolare varianza di un array di dati con correlazione:
divide l'arrauy in blocchi, calcola la media dei blocchi (perdita di autocorrelazione)
calcola la varianza delle medie
calcola la media delle varianze ---> ritorna varianza dei blocchi scorrelati
'''

def blocking(data):
    N = len(data)                       #numero di estrazioni
    base=2                              #seleziona la base del logaritmo (chopping dei blocchi)
    k = int(np.log(N)/np.log(base))     #esponente massimo del chopping (potenze di "base") t.c. base^k <= N
    if k < 2:                           #controllo k positivo e sufficiente a fare almeno un chopping
        print(f"Data length: {N}, base: {base}, k: {k}")
        raise ValueError("Data length must be at least \"base\" (enough for 1 block).")
    variance = np.zeros(k-1)   #k-1 o k???         #array per salvare varianza ad ogni iterazione
    mu = np.mean(data)
    
    #print(f"N: {N}, k: {k}, mu: {mu}")                 PARAMETRI DELL'ALGORITMO DI BLOCKING: NUMERO DI DATI, NUMERO PASSI DI BISEZIONE, MEDIA DEI DATI
    for l in range(1,k):                #runna sulle potenze della base
        i=base**l
        cut_point = N % i               #taglio di N per avere multipli delle potenze di "base"
        n=N - cut_point                 #nuova lunghezza dei dati
        num_blocks = n // i             #numero di blocchi (colonne)
        mean_blocks = np.zeros(num_blocks)
        binned_data=np.reshape(data[cut_point:], (i, num_blocks))   #reshape dei dati in n/i blocchi di i=2^l elementi
        #print(f"iteration {l}: shape={np.shape(binned_data)}, points={n}/{len(data)}")  #control for debug
        #show_matrix(binned_data)

        mean_blocks = np.mean(binned_data, axis=0)  #calcolo della media dei blocchi (colonne)
        variance[l-1] = np.var(mean_blocks, ddof=1) #calcolo della varianza delle medie dei blocchi
        #print(f"Variance at step {l}: {variance[l-1]}, {len(variance)}")   #control for debug
        #print(f"Block {j}/{num_blocks-1} data: {binned_data[:,j]},\n mean= {mu_blocks[j]}")   #control for debug (run on j missing)

    mean_variance = np.mean(variance)

    return mean_variance

#ISSUE: LA FORMULA DELLA VARIANZA è VALIDA SOLO PER N>>K (elementi di ogni blocco)
    #POSSIBILE SOLUZIONE: NON CONSIDERARE LE POTENZE GRANDI DELLE BASI (poche colonne di tanti elementi)
    #POSSIBILE SOLUZIONE 2: CAMBIARE LA BASE CON UNA PIù ALTA (es. base=3 o 4)
#ISSUE: IL TAGLIO DEI DATI RENDE LA MEDIA DELLE MEDIE DEI BLOCCHI DIVERSA DALLA MEDIA DEI DATI
    #POSSIBILE SOLUZIONE: MEDIAMO SOMMANDO ANCHE LA MEDIA DEI DATI TAGLIATI
    #mean_cut = np.mean(data[:cut_point])        #media dei dati tagliati
    #    if (np.mean(mean_blocks)+mean_cut)/2 != mu:
    #        raise ValueError("Warning: mean of blocks {np.mean(mean_blocks)} != global mean {mu}")
    #ISSUE: NON FUNZIONA, FORSE PROBLEMA CON LUNGHEZZA DELL'ARRAY DATA[:cut_point]