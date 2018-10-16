#!/usr/bin/env python3
import numpy as np

def KLD(a, b):
    """ KL Divergence
    """
    a = np.asarray(a,dtype=np.float)
    b = np.asarray(b,dtype=np.float)
    return np.sum(np.where(a != 0, a * np.log(a / b), 0))


v1 = [1.346112,1.337432,1.246655]
v2 = [1.033836,1.082015,1.117323]

print(KLD(v1,v1))
print(KLD(v1,v2))

p = [0.1, 0.9]
q = [0.1, 0.9]

print(KLD(p,q))
