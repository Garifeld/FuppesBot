def xgcd(b, a):#return a triple (g, x, y), such that ax + by = g = gcd(a, b)
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  b, x0, y0

class Fp:

    def __init__(self,m,p):
        self.m = m%p
        self.p=p

    def __add__(self,x):
        if type(x)==Fp:
            if x.p!=self.p:
                raise ValueError("Cannot add elements of different fields F%i and F%i"%(self.p,x.p))
            return Fp((x.m+self.m)%self.p,self.p)
        if type(x)==int:
            return Fp((x+self.m)%self.p,self.p)
        raise ValueError("Uncastable argument in Fp-addition %s"%type(x))

    def __radd__(self,x):
        return self+x

    def __neg__(self):
        return Fp(-self.m%self.p,self.p)

    def __sub__(self,x):
        if type(x)==Fp:
            if x.p!=self.p:
                raise ValueError("Cannot subtract elements of different fields F%i and F%i"%(self.p,x.p))
            return Fp((self.m-x.m)%self.p,self.p)
        if type(x)==int:
            return Fp((self.m-x)%self.p,self.p)
        raise ValueError("Uncastable argument in Fp-subtraction %s"%type(x))

    def __rsub__(self,x):
        return -(self-x)

    def __mul__(self,x):
        if type(x)==Fp:
            if x.p!=self.p:
                raise ValueError("Cannot multiply elements of different fields F%i and F%i"%(self.p,x.p))
            return Fp((self.m*x.m)%self.p,self.p)
        if type(x)==int:
            return Fp((self.m*x)%self.p,self.p)
        if type(x)==Vector:
            return x*self 
        raise ValueError("Uncastable argument in Fp-multiplication %s"%type(x))

    def __rmul__(self,x):
        return self*x

    def modinv(self):
        [g,a,b]=xgcd(self.m,self.p)
        if g!=1:
            raise ValueError("%i is not invertible mod %i"%(self.m,self.p))
        return Fp(a,self.p)

    def __truediv__(self,x):
        if type(x)==Fp:
            if x.p!=self.p:
                raise ValueError("Cannot divide elements of different fields F%i and F%i"%(self.p,x.p))
            return self*x.modinv()
        if type(x)==int:
            return self*Fp(x%self.p,self.p).modinv()
        raise ValueError("Uncastable argument in Fp-division. %s"%type(x))

    def __rtruediv__(self,x):
        return (self/x).modinv()       
    
    def __repr__(self):
        return ("%i (mod %i)"%(self.m,self.p))

    def __str__(self):
        return ("%i (mod %i)"%(self.m,self.p))

    def __pow__(self,exp):
        x=self
        if exp<0:
            x=self.modinv()
            exp=-exp
        ret=Fp(1,self.p)
        while exp>0:
            [ret,x,exp]=[ret*x if exp%2!=0 else ret,x*x,exp//2]
        return ret

    def __eq__(self,x):
        if type(x)==Fp:
            return (x.p==self.p) and (self.m==x.m)
        if type(x)==int:
            return x%self.p==self.m
        raise ValueError("Uncastable argument in Fp-division. %s"%type(x))

    def __req__(self,x):
        return self==x

    def zero(self):
        return Fp(0,self.p)

    def one(self):
        return Fp(1,self.p)

#class ChainComplexGenerator():
    
class SimplicialSet():

    #inc stores all simplices in the following form
    # inc[n] is a hashtable with entries i:(d_0(i),..,d_n+1(i))
    # storing the boundaries of the i-th nondegenerate n-simplex
    # each d_i is a pair (deg,int,int)
    #deg is a degeneracy map, stored as a sequence of nondecreasing ints
    #meaning that we apply s_* for * in that tuple
    #first int is  the index of the nondegenerate n-|deg|-dim simplex
    # second int is the dimension of our simplex
    
    def __init__(self,inc):
        self.inc=inc

    def addSimplex(self,x):
        dim = max(0,len(x)-1)
        self.inc[dim][len(self.inc[dim])]=x
        
    def removeSimplex(self,x):#OMFG ADD THAT RELABELING
        raise NotImplementedError("This method has not yet been implemented")

    def dim(self,simplex):
        return simplex[2]

    def isDegenerate(self,simplex):
        return len(simplex[0])>0
    
    def d(self,simplex,i):
        print("Calling d %i on %s "%(i,str(simplex)))
        li=list(simplex[0])
        for j in range(len(li)):
            if li[j]+1<i:
                i-=1
            elif i==li[j] or i==li[j]+1:
                ret= (tuple(li[:j]+li[j+1:]),simplex[1],simplex[2]-1)
                print("case1")
                return ret
            else:
                #print("case2")
                li[j]-=1
        print("case2")
        cur =self.inc[simplex[2]-len(li)][simplex[1]][i]
        for k in range(len(li)-1,-1,-1):
            cur =self.s(cur,li[k])
        return cur#asdf now we need the dimension

    def s(self,simplex,i):
        #raise NotImplementedError("This method has not yet been implemented")
        j=0
        while j <len(simplex[0]):
            if simplex[0][j]<i:
                i-=1
            else:
                break
            j+=1
        ret=(tuple(simplex[0][:j]+(i,)+simplex[0][j:]),simplex[1],simplex[2]+1)
        return ret
            
    def applyMorphismFromSimplexCategory(self,simplex,f):# f:m->n is a tuple (f(0),..,f(m))
        #raise NotImplementedError("This method has not yet been implemented")
        cur=simplex
        find = len(f)-1
        for j in range(simplex[2],-1,-1):
            if (find==-1) or (j>f[find]):
                cur=self.d(cur,j)
                print("Applied d%i cur:%s"%(j,str(cur)))
            elif j==f[find]:
                find-=1
                if find==-1:
                    continue
                while f[find]==f[find+1]:
                    cur=self.s(cur,f[find])
                    print("Applied s%i cur%s"%(f[find],str(cur)))
                    find-=1
        return cur#TODO TEST THIS

class Vector():
    #stores vectors as dicts of the form {i:coeff of e_i}
    # stored only the nonzero entries

    def __init__(self,dic):
        self.v=dic
        self.shorten()

    def __add__(self,w):
        #print("adding vectors %s and %s"%(str(self),str(w)))
        nud = self.v.copy()
        for key in w.v:
            if key in nud:
                nud[key]=nud[key]+w.v[key]
            else:
                nud[key]=w.v[key]
        return Vector(nud)

    def shorten(self):
        for key in list(self.v.keys()):
            if self.v[key]==0:
                del self.v[key]

    
    def __rmul__(self,lamb):
        for key in self.v:
            self.v[key]=lamb*self.v[key]

    def __mul__(self,lamb):
        ret =Vector({})
        for key in self.v:
            ret.v[key]=lamb*self.v[key]
        return ret


    def __repr__(self):
        return str(self.v)

    def __str__(self):
        return str(self.v)

    def __eq__(self,w):
        if type(w)==int and w==0:
            return len(self.v)==0
        return self.v==w.v
    
        
class ChainComplex():

    #self.TB is a dict of dicts. such that
    #self.TB[dim][i] is a tuple (j,vect) such that d(vect) is the j-1 th basis vector TB in dimension dim-1
    #j=0 means it represents a cohomology class, j=-k means it is boundary of the (k-1)-th vector in TB[dim+1]

    #self.gen has two methods dim(n), which returns the dimension of C_n
    # and d(dim,i) which returns the image of the i-th standart basis vector as a vector
    
    # ring could also be lambda x:Fp(x,p) or sth.
    def __init__(self, gen, ring=lambda x:x):
        self.gen=gen
        self.ring=ring

    # Computing the Cohomology means four things
    # 1) compute it as abstract groups
    # 2) find a map that picks for each cohomology class a representative
    # 3) find a map that sends a cycle to its cohomology class
    # 4) For a boundary, find a preimage under the differential
    def computeHomology(self,mindim ,maxdim):
         #raise NotImplementedError("This method has not yet been implemented")
        self.TB ={}
        self.cohomGen={}
        for dim in range(maxdim+1, mindim-2,-1):
            self.TB[dim]={}
            self.cohomGen[dim]=set([])
        for dim in range(maxdim+1, mindim-2,-1):
            for i in range(self.gen.dim(dim)):
                if(i in self.TB[dim]):#meaning that there has been a dim+1 dim vector whose bdry has pivot at i
                    print("TB[%i] already contains %i"%(dim,i))
                    continue
                st=Vector({i:self.ring(1)})#standart-basis vector
                bdry = self.gen.d(dim,i)#boundary of that vector
                print("%i-th std basis vector in dim %i send to %s"%(i,dim,str(bdry)))
                print("current TB in dim %i: %s"%(dim,str(self.TB[dim])))
                print("current TB in dim %i: %s"%(dim-1,str(self.TB[dim-1])))
                print("looking at simplex %s of dim %i and its bdry %s"%(str(st),dim,str(bdry)) )
                pivot=-1
                if bdry !=0:
                    pivot=max(bdry.v)
                    print("pivot:%i"%pivot)
                    while bdry !=0 and pivot in self.TB[dim-1]:
                        toadd =self.TB[dim][-(self.TB[dim-1][pivot][0]+1)][1]
                        print("toadd: %s"%str(toadd))
                        lamb=(-bdry.v[pivot]
                              /self.TB[dim-1][pivot][1].v[pivot])
                        st =st+lamb*toadd#asdf
                        bdry = bdry+lamb*self.TB[dim-1][pivot][1]
                        if bdry !=0:
                            pivot=max(bdry.v)
                if bdry ==0:# we found a cycle which isnt bdry
                    self.TB[dim][i]=[0,st]
                    self.cohomGen[dim].add(i)
                else:
                    self.TB[dim-1][pivot]=[-(i+1),bdry]#asdf -0=0 so my encoding doesnt work !!!!
                    self.TB[dim][i]=[pivot+1,st]

    def TBcoefficients(self,dim,v):
        coeff = {}
        if self.TB==None:
            raise ArithmeticError("Cohomology has not been computed in dimension %i"%dim)
        for i in range(len(self.TB[dim])-1,-1,-1):#counting backwards
            if i not in v.v:
                continue
            coi =-v.v[i]/self.TB[dim][i][1].v[i]
            coeff[i]=coi
            v=v+coi*self.TB[dim][i][1]
        return Vector(coeff)

    def TBcoefftoVector(self,dim,coeff):
        cur=Vector({})
        for i in v.v:
            cur=cur+coeff.v[i]*self.TB[dim][i][1]
        return cur
    
    #returns a representative of a given cohomology class
    # the class is given as a linear combination of the triangular bases TB's
    def getRepresentative(self,dim,v):
        cur=Vector({})
        for i in v.v:
            cur=cur+v.v[i]*self.TB[dim][i][1]
        return cur

    
    #finds for a vector v which is a boundary a preimage under the differential
    def preimage(self,dim,v):
        coeff = self.TBcoefficients(self,dim,v)
        v=Vector({})
        for i in coeff.v:
            ind = self.TB[dim][i][0]
            if ind>=0:
                raise ArithmeticError("Given class is not a boundary, coefficents: %s"%str(coeff))
            v=v+coeff.v[i]*self.TB[dim+1][-(ind+1)][1]
        return v
    
    # finds sends a cycle to the homology class it represents
    def homClass(self,dim,v):
        coeff =self.TBcoefficients(dim,v)
        v=Vector({})
        for i in coeff.v:
            ind = self.TB[dim][i][0]
            if ind>0:
                raise ArithmeticError("Given class is not a cycle, coefficents: %s"%str(coeff))
            if ind==0:
                v.v[i]=coeff.v[i]
        return v

    def printHomology(self,mindim,maxdim):
        print("k:dim(H_k(C_k)) for k=%i,..,%i: %s"%(mindim,maxdim,' , '.join(["%i:%i"%(j,len(self.cohomGen[j])) for j in range(mindim,maxdim+1)])))

class SurjOperadAlgebra(ChainComplex):
    def applySurjection():
        raise NotImplementedError("This method has not yet been implemented")
        
    
    
class FilteredComplex(ChainComplex):
    #for  our purpose, we can look only at vector spaces. The filtration
    # is given by additionally giving each basis vector a filtration degree.

    # gen should now contain a method filtrdegree with arguments (self,dim,i) which tells you the filtrationd degree of the i-th basis vector in dimension dim. 
    def __init__(self, gen, ring=lambda x:x):
        super(B, self).__init__(gen,ring)
    
    def startSpectralSequence():
        raise NotImplementedError("This method has not yet been implemented")
    
    
        
        
    
    

class Group():

    def __init__(self,mul,neu,inv):
        self.__mul__=mul
        self.neu==neu
        self.inv =inv

class Permutation(Group):
    def __mul__(self,x):
        if type(x)!=Permutation:
            raise ValueError("Cannot compose permutation with %s"%str(type(x)))
        if len(self.tup)!=len(x.tup):
            raise ValueError("Cannot compose permutations of size %i and %i"%(len(self.tup),len(x.tup)))          
        ret =Permutation(tuple([self.tup[j] for j in x.tup]))
        return ret

    def invert(self):
        tup = [-1 for i in range(len(self.tup))]
        for i in range(len(tup)):
            tup[self.tup[i]]=i
        return Permutation(tuple(tup))

    def neu(n):
        size=-1
        if type(n)==int:
            size=n
        if type(n)==Permutation:
            size=len(n.tup)
        if size==-1:
            raise ValueError("Cannot understand argument of neu: type %s"%str(type(n)))
        return Permutation(tuple([i for i in range(size)]))

    def __eq__(self,x):
        if type(x)!=Permutation:
            return False
        return self.tup==x.tup

    def __str__(self):
        return str(self.tup)

    def __repr__(self):
        return str(self.tup)
          
    def __init__(self,tup):
        self.tup=tup

    def eletoindex(self):
        return
    
    def indextoele(self,n):
        return
    
def getTorus():
    inc = [{0:()},
           {0:(((),0,0),((),0,0)),1:(((),0,0),((),0,0)),2:(((),0,0),((),0,0))},
           {0:(((),1,1),((),2,1),((),0,1)),1:(((),0,1),((),2,1),((),1,1))}]
    X=SimplicialSet(inc)
    return X
    
class SampleGen:
    #self.gen has two methods dim(n), which returns the dimension of C_n
    # and d(dim,i) which returns the image of the i-th standart basis vector as a vector
    
    def __init__(self):
        self.dims={0:1,1:2,2:1}
        pass

    def dim(self,n):
        if n not in self.dims:
            return 0
        else:
            return self.dims[n]

    
    def d(self,dim,i):
        if dim==2:
            return Vector({})
        if dim==1:
            return Vector({0:Fp(1,2)})
        return Vector({})


SG=SampleGen()
CC=ChainComplex(gen=SG,ring =lambda x:Fp(x,2))
CC.computeHomology(0,2)
CC.printHomology(0,2)
#v=CC.TB[1][1][1]
v=Vector({})
print(v)
ch = CC.homClass(1,v)
print(ch)

#X=getTorus()
#A=((),1,2)
#f=(1,2,2)
#print(A)
#print(f)
#ret=X.applyMorphismFromSimplexCategory(A,f)
#print(ret)

#one=Fp(1,5)
#v=Vector({0:one,2:one})
#w=Vector({0:Fp(4,5),1:one})
#print(v)
#print(w)
#print(v+w)
