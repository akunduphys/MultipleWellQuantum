import h5py
import matplotlib.pyplot as plt
import numpy as np
import Bound_State_Solver as bss

class Loader():

	def __init__(self,option):
		self.BSobj=bss.BoundState(a=.5,b=1,v0=100.,n=1,option=option)	
#H=P	(parameters,'withoutfft')

	def _calculate_(self):
		self.H =self.BSobj.Hamiltonian('withfft')
		
		self.eigenvalues, self.eigenvectors = np.linalg.eigh(self.H, UPLO='U')


	def store(self):
# Store in hdf5 format:
		datafile = h5py.File('data.h5', 'w')
		datafile['x'] = self.BSobj.x
		datafile['V'] = self.BSobj.V(self.BSobj.x)
		datafile['H'] = self.H
		datafile['eigenvalues'] = self.eigenvalues
		datafile['eigenvectors'] = np.abs(self.eigenvectors)
		#datafile.close()


	def loader(self):
		datafile = h5py.File('data.h5', 'r')
		self.x = datafile['x'][:]
		self.V = datafile['V'][:]
		self.eigenvalues = datafile['eigenvalues'][:]
		self.eigenvectors = datafile['eigenvectors'][:]
		datafile.close()

	fig=plt.figure()

	def plot_all(self,name):
		self.fig.clf()
		ax_left=self.fig.add_subplot(111)
		ax_right=ax_left.twinx()
		ax_left.set_ylabel('$V$')
		ax_right.set_ylabel('$\psi$')
		ax_left.set_ylim(-self.BSobj.param.a,self.BSobj.param.v0)
		ax_right.set_ylim(0,1)
		ax_left.set_xlabel('$x$')
		plt.title(name)
		scaley=(ax_right.axis()[3]-ax_right.axis()[2])/(ax_left.axis()[3]-ax_left.axis()[2])
		lineleft,=ax_left.plot(self.x,self.V,'--',lw=2)
		i=0
		while (self.eigenvalues[i]<self.BSobj.param.v0):
			#print 'im here',scaley
			ax_right.plot(self.x,scaley*self.eigenvalues[i]+ax_right.axis()[2]+self.eigenvectors[:,i])
			i=i+1
	
		#plot_all()
		plt.show()
		

names=["n Square well","n Harmonic well","Yukawa Potential","Gaussian potential"]
print ("Enter option\n 1.n Square well\n2.n Harmonic well \n Yukawa Potential\n 4.Gaussian potential")		
option=input()
loadobj=Loader(option=option)
loadobj._calculate_()
loadobj.store()
loadobj.loader()
loadobj.plot_all(names[option-1])
plt.show()
