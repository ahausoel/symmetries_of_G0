# imports
import numpy as np
import sys
from sys import exit, stderr as err
### here comes w2dynamics
auxdir="/Users/andi/w2dynamics___patrik_alexander_merge___likegit/"
sys.path.insert(0,auxdir)
import optparse, re
import auxiliaries.input as io
import auxiliaries.transform as tf

### here comes the ls basis
hkfile = file("wannier90_hk_t2gbasis.dat_") 
hk_ls, kpoints = io.read_hamiltonian(hkfile,spin_orbit=True)

nflav=hk_ls.shape[1]*2
Nk=kpoints.shape[0]
hk_ls=hk_ls.reshape(Nk,nflav,nflav)
hkmean_ls=hk_ls.mean(0)

#### this would set random hermitian matrix of the form
####    (  A      B  )
####    (  B^dag  A  )     with A^dag = A and arbitrary B

#def get_rand():
    #tmp = np.random.rand(nflav/2, nflav/2)*2 - np.ones((nflav/2, nflav/2))
    #return tmp

#A = get_rand() + 1.0j*get_rand()
#A += np.conjugate(np.transpose(A))
##A[...] = 0

#B = get_rand() + 1.0j*get_rand()
##B[...] = 0

#hk_ls[...] = 0
#hk_ls[0,0:nflav/2,0:nflav/2] = A
#hk_ls[0,nflav/2:,nflav/2:] = np.conjugate(A)
#hk_ls[0,0:nflav/2,nflav/2:] = B
#hk_ls[0,nflav/2:,0:nflav/2] = np.transpose(np.conjugate(B))

#####################################
#####################################
#####################################

print 'hk_ls.shape', hk_ls.shape

beta = 10.0
Niw = 50

iw = tf.matfreq(beta, 'fermi', Niw)

print 'iw.shape', iw.shape
print 'nflav', nflav

### calculate G0
G = np.zeros( shape=(nflav,nflav,Niw), dtype=complex )

for nw, w in enumerate(iw):

    denom = np.zeros( shape=(nflav,nflav), dtype=complex )
    #np.fill_diagonal( denom, 1.0j * w - 0.626832 )
    np.fill_diagonal( denom, 1.0j * w  )
    #print 'denom', denom

    for k in range(Nk):

        G[:,:,nw] += np.linalg.inv( denom - hk_ls[k,:,:] )

G /= float(Nk)

G = G.reshape(nflav/2, 2, nflav/2, 2, Niw)
print 'G.shape', G.shape

### dump it
data = np.column_stack((iw,np.real(G[0,0,2,1,:]),np.imag(G[0,0,2,1,:])))
np.savetxt("g0_0021.dat", data)
data = np.column_stack((iw,np.real(G[2,1,0,0,:]),np.imag(G[2,1,0,0,:])))
np.savetxt("g0_2100.dat", data)
data = np.column_stack((iw,np.real(G[0,1,2,0,:]),np.imag(G[0,1,2,0,:])))
np.savetxt("g0_0120.dat", data)
