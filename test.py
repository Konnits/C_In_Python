import numpy as np
import ctypes
import time

class FastFor(ctypes.Structure):
    _fields_ = [("n", ctypes.c_int)]

lib = ctypes.CDLL('./libmodulo.so')
lib.NewFastFor.argtypes = [ctypes.c_int]
lib.NewFastFor.restype = ctypes.POINTER(FastFor)

lib.Sum.argtypes = [ctypes.POINTER(FastFor)]
lib.Sum.restype = ctypes.c_int64

lib.FreeFastFor.argtypes = [ctypes.POINTER(FastFor)]
lib.FreeFastFor.restype = None

n = 100_000_000

new_for = lib.NewFastFor(n)


start_time = time.time()
a = lib.Sum(new_for)
end_time = time.time()
lib.FreeFastFor(new_for)
print("C++: ", end_time - start_time)

start_time = time.time()
b = 0
for i in range(n):
    b += i
end_time = time.time()
print("Python: ", end_time - start_time)

start_time = time.time()
c = np.sum(np.arange(n))
end_time = time.time()
print("Numpy: ", end_time - start_time)