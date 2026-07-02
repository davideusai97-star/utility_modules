import numpy as np
from module_show_matrix import show_matrix # type: ignore

'''
IN: DATA ARRAY; OUT: MEAN VARIANCE
Blocking algorithm used to calculate variance of an array with correlated values:
splits the arrays into blocks, calculates the mean f each block (autocorrelation loss)
calculates the variance of the means
gets the mean variance of the means ---> return variance of uncorrelated blocks
'''

def blocking(data):
    N = len(data)                       #number of values
    base=2                              #selects the logarithm base (number of chopping points each step)
    k = int(np.log(N)/np.log(base))     #max exponent for selected chopping method, so that base^k <= N
    if k < 2:                           #check positivity of k and sufficient to make at least 1 chopping
        print(f"Data length: {N}, base: {base}, k: {k}")
        raise ValueError("Data length must be at least \"base\" (enough for 1 block).")
    variance = np.zeros(k-1)   #k-1 o k???         # variance is saved in this array at every step
    mu = np.mean(data)
    
    #print(f"N: {N}, k: {k}, mu: {mu}")                BLOCKING PARAMETERS: NUMBER OF DATA, NUMBER  OF CHOPPING STEPS, MEAN OF THE DATA
    for l in range(1,k):                #runna sulle potenze della base
        i=base**l
        cut_point = N % i               #removes the excess data to have regular bins (multiple of base)
        n=N - cut_point                 #new data lenght
        num_blocks = n // i             #number of blocks (coloumns)
        mean_blocks = np.zeros(num_blocks)
        binned_data=np.reshape(data[cut_point:], (i, num_blocks))   #reshapes data in n/i blocks of i=2^l elements
        #print(f"iteration {l}: shape={np.shape(binned_data)}, points={n}/{len(data)}")  #control for debug
        #show_matrix(binned_data)

        mean_blocks = np.mean(binned_data, axis=0)  #makes mean of each block (coloumns)
        variance[l-1] = np.var(mean_blocks, ddof=1) #makes variance of the block means
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
