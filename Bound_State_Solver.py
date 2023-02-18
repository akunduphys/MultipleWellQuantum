from __future__ import division
import numpy as np
import Potential
import h5py
#import loadh5 as lh5
class BoundState():
	
	def __init__(self,a,b,v0,n,option):
		print option,'in bss'
		self.param=Potential.Parameter(a,b,v0,n,option)
		self.N= self.param.N
		self.h_cross = self.param.h_cross
		self.m = self.param.m
		self.V = self.param.V
		self.x = self.param.x
		#self.option=option

	def Hamiltonian(self,algorithm):	
	    Length_max = self.x[-1] - self.x[0]
	    delta_k = 2*np.pi/Length_max
	    N=self.N
	    n = (N/2)
	
	    if algorithm=='withoutfft':
	        KE = np.zeros((N, N))
	
	        l = np.arange(1, n+1, 1)
	        T_l = self.h_cross**2/(2*self.m) * (l*delta_k)**2
	
	        for i in xrange(N):
	            print "Row = ", i
	            for j in xrange(i, N, 1):
	                KE[i, j] = 2/N*np.sum(np.cos(l*2*np.pi*(i - j)/N)*T_l)
	
	    elif algorithm=='withfft':
	        KE = np.diag(np.ones(N) + 1j*np.zeros(N))
	
	        l = np.arange(1, n+1, 1)
#   	        l = np.arange(-n, n+1, 1)
	        T_l = self.h_cross**2/(2*self.m) * (l*delta_k)**2
	        
	
	        for row in xrange(N):
	            #print "Row = ", row
	            #KE[row, :] = np.fft.ifft(T_l*np.fft.fft(KE[row, :]))
	            KE[row, :] = np.fft.irfft(T_l*np.fft.rfft(KE[row, :]))
	
	    H = KE + np.diag(self.param.V(self.x))
	    
	    return H
	
	


