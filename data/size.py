import numpy as np
import sys

with open('txt_size','a') as f:
    a = np.ones((5,10000,10000))
    size = sys.getsizeof(a)
    f.write('size : '+str(size))
    del a

    a = np.ones((10,10000,10000))
    size = sys.getsizeof(a)
    f.write('size : '+str(size))
    del a

    a = np.ones((15,10000,10000))
    size = sys.getsizeof(a)
    f.write('size : '+str(size))
    del a
