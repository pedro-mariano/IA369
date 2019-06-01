import numpy as np
from metrics3 import hv2DContribution
from PyGMO.util import hypervolume

N = 10
hvCont = np.zeros(N)
points = np.random.random((N,2))
points = np.sort(points,axis=0)
points[:,1] = points[:,1][::-1]
ref = points.max(axis=0)*1.1
hv = hypervolume(points.tolist())
for i in np.arange(N):
    hvCont[i] = hv.exclusive(i,ref.tolist())

hvCont2 = hv2DContribution(points,ref)

diff = np.sqrt(np.sum((hvCont - hvCont2)**2)/N)

print diff
print hvCont
print hvCont2
