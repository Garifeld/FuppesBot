# in this Project we will use the quadratic sieve algorithm for find factors of some large numbers

def xgcd(b, a):#return a triple (g, x, y), such that ax + by = g = gcd(a, b)
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  b, x0, y0

def modInv(a,n):
    ret= xgcd(a,n)
    if ret[0]!= 1:
        raise ArithmeticError("%i is not invertible mod %i"%(a,n))
    else:
        return ret[1]%n

def isComposite(num):#uses little Fermat to test whether this number is definitively composite
    cur=2
    res=1
    exp=num-1
    while exp>0:
        [res,cur,exp] =[res if exp%2==0 else (res*cur)%num,(cur*cur)%num,exp//2]  
    return res!=1

#computes a list of all prime numbers up to a certain bound
def computePrimes(bound):
    L=[2,3]
    i=1
    while 6*i+1<bound:
        for toadd in (6*i-1,6*i+1):
            if isComposite(toadd):
                continue
            isprime=True
            for p in L:
                if toadd%p==0:
                    isprime=False
                    break
            if isprime:
                L.append(toadd)
                if len(L)%100 ==0:
                    print("found %i primes, last prime is %i"%(len(L),L[-1]))
        i+=1
    return L

def NextPrime(bound,Primes):#returns the next Prime bigger than bound, Primes is the list of all Prime numbers less than bound**0.5 
    i=bound
    while(True):
        if isComposite(i):
            i+=1
            continue
        isprime=True
        for p in Primes:
            if i%p==0:
                isprime=False
                break
        if isprime:
            return i

        


UniBound =10**15# tries to factor numbers that are below that bound
Primes =computePrimes(1000000)

RSA=1522605027922533360535618378132637429718068114961380688657908494580122963258952897654000350692006139
toFactor=RSA#97723855957823

def tryRoot(v,n):#
    vn=v
    v2=(v*v)%n
    if v2>UniBound:
        return -1
    PF = set()
    #maybe we should already forget it if v2 seems to be prime ?
    for i in range(len(Primes)):
        if v2%Primes[i]==0:
            mul =modInv(Primes[i],n)
            if i in PF:
                vn=vn*mul%n
                v2=v2//(Primes[i]**2)
                PF.remove(i)
            else:
                v2 = v2//Primes[i]
                PF.add(i)
    if v2==1:
        return [vn,PF]
    else:
        return -1


def QuadraticSieve(n):
    VectorList={}# Hashtable of i: (v,PF) with v**2 mod n can be Factored using Primes and Primes[i] is its highest factor occuring in PF
    ind=0
    while(True):
        ind+=1
        v = round((n*ind)**0.5)
        ret=tryRoot(v,n)
        if ret==-1:
            continue
        else:
            print("found the %i-th good number"%(len(VectorList)+1))
            while len(ret[1])>0 and (max(ret[1]) in VectorList):
                (oldV,oldPF)=VectorList[max(ret[1])]
                nuv =(ret[0]*oldV)%n
                nuPF = set([])
                for p in ret[1]:
                    if p in oldPF:
                        nuv =(nuv*modInv(Primes[p],n))%n
                    else:
                        nuPF.add(p)
                for p in oldPF:
                    if not (p in ret[1]):
                        nuPF.add(p)
                ret=[nuv,nuPF]
            if (len(ret[1])==0):
                g=xgcd(ret[0]+1,n)[0]
                print("found an element that squares to 1, gave factor %i of %i"%(g,n))
                if g!=n:
                    return
            else:
                VectorList[max(ret[1])]=ret


    

QuadraticSieve(toFactor)       

