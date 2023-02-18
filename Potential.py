from __future__ import division
import numpy as np

'''
1.
c) Study the splitting of levels at each energy level as you go from 1 to
5 wells. For example, are the levels evenly spaced? Are the splittings
different for different values of the quantum number n (of part 1)?
d) Now run the code for algorithm=withfft. Compare both the time taken and
the answers you get with those obtained 'withoutfft'.

2. Define the following spherical symmetric potentials:

a) -V_0*exp(-r/a)                [Exponential well]
b) -V_0*exp(-r**2/a**2)          [Gaussian well]
c) -V_0*exp(-r/a)/(r/a)          [Yukawa well]
d) -V_0*exp(-r/a)(1-exp(-r/a))   [Hulthen well]
e) 1/2*k*r**2                    [Isotropic harmonic well]
f) 3-dim square well

Add the centrifugal term l*(l+1)*h_cross**2/r**2 to each of these and plot
the result for various values of l.
3.
a) Devise a scheme for converting a single finite one-dimensional harmonic
well into a delta-function. Specifically, produce a sequence, {W_n}, of
harmonic wells which become narrower and deeper in such a way that the
area of the well remains constant.
b) Include a facility to display 'p' wells starting from the mth.
c) Even better, animate the sequence.
d) Repeat the entire exercise for a square well.
'''

class Potential(object):
	def __init__(self,a=.5,b=1.5,v0=100.,n=1):
		self.a=a
		self.b=b
		self.v0=v0
		self.n=n
	
	def V_Exponential_well(self,x):
		return -self.v0*np.exp(-x/self.a)
		
	def V_Gaussian_well(self,x):
		return -self.v0*np.exp(-x**2/(self.a)**2)
		
	def V_Yukawa_well(self,x):
		return -self.v0*np.exp(-x/self.a)/(x/self.a)
	
	def V_Hulthen_well(self,x):
		return -self.v0*np.exp(-x/self.a)*(1-np.exp(-x/self.a))
		
	def V_Square_well(self,x):
		if(x < self.a and x> -self.a):
			return 0
		return self.v0
	
	
	def V_n_Square_well(self,x):
	# check if x lies anywhere in _a_|`b`|_a_|`b`|_a_|`b`|_a_|`b`|
		for i in xrange(0,self.n):
			if(x>=i*(self.a+self.b) and x<=(i+1)*self.a+i*self.b):
				return 0
		return self.v0
	
	
	def V_n_Harmonic_well(self,x):#``U``U``U``U``U``
	
		for i in xrange(0,self.n):
			#print i
			if(x>(self.a+self.b)*i and x<(2+i)*self.a+(i)*self.b):
				offset=(i+1)*self.a+i*self.b
			#print np.mod(x,((i+1)*(a+b)))
				return (self.v0/(self.a**2))*(x-offset)**2
		return self.v0
		
	
	
	def printM(self,x):
		print 'Im in mother',x

	def make_spherical(x,potential,l):
		return potential
		
	#V_n_harmonic=np.vectorize(V_n_harmonic)



class Parameter(Potential):

	def __init__(self,a=.5,b=1.,v0=1000.,n=1,option=1):
		print '__in Parameter init__'
		self.N = 1025
		self.h_cross = 1
		self.m = 1
		self.a=a
		self.b=b
		self.v0=v0
		self.n=n
		x0=-(a+b)*n
		x1=(a+b)*n
		self.x = np.linspace(x0,x1,self.N)
		self.option=option
		#self.pot=Potential.Potential(self.x,a,b,v0,n)
		self.V_n_Harmonic_well=np.vectorize(self.V_n_Harmonic_well)
		self.V_n_Square_well=np.vectorize(self.V_n_Square_well)
	
	def V2(self,x):
		print self.n,self.a,self.b
		return self.V_n_well(x)
		
	
	def V(self,x):
		#print self.n,self.a,self.b	
		print self.option
		if self.option==1:
			return self.V_n_Square_well(x)
		elif self.option==2:
			return self.V_n_Harmonic_well(x)
		elif self.option==3:
			return self.V_Yukawa_well(x)
		else:
			return self.V_Gaussian_well(x)
		
	

