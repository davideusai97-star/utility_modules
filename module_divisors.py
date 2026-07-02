import numpy as np

'''Find divisors of N, except for very small or very large divisors
Ensures at least 'min_divisors' divisors are found
if not, decrement iteratelly N until enough divisors are found
Returns adjusted N and list of divisors'''


def find_divisors(N, min_divisors):
    #print(f"True divisors of {N}:{all_divisors(N)}")       #uncomment for debug with all divisors function
    if N<1:                 #flag for negative or zero N
        raise ValueError("N must be a positive integer.")
    divisors = []
    start=max(2,int(0.05*np.sqrt(N)))       #cuts 5% non-useful divisors (very small and very large)
    #print(f"Takes divisors > {start} for {N}...")
    for i in range(start, int(np.sqrt(N))+1):
        if N % i == 0:
            divisors.append(i)
            if i != N // i:  # Avoid duplicate divisors
                divisors.append(N // i)

    if len(divisors)<min_divisors:         #find at least min_divisors of number next to N
        #print(f"{N} has no useful divisors. First element will be removed")
        N, divisors=find_divisors(N-1, min_divisors)   #if N is prime, use N-1 and reassign N
    
    divisors.sort()
    return N, np.array(divisors)

'''
#--------------------------------SETTINGS FOR CONTROL PURPOSES
def all_divisors(num):          #find all divisors of a number except 1 and the number itself
    divisors = []
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            divisors.append(i)
            if i != num // i:  # Avoid duplicate divisors
                divisors.append(num // i)
    return sorted(divisors)


#--------------------------------SETTINGS
import random
N=random.randint(1,50000000)   #lunghezza casuale dei dati
new_N, divisors=find_divisors(N, 4)
#print("Divisor search complete.\n")
print(f"Adjusted N: {new_N}: cut of {N-new_N} required")
print(f"{new_N} has divisors: {divisors}")
'''
