# Uso de C en Python

Lo siguiente es un ejemplo de cómo podemos utilizar C en python para el desempeño de un código.

## Requerimientos

Para el desarrollo de este ejemplo se utilizó una máquina virtual de linux en windows, para la cual fue necesario instalar lo siguiente:

- Python:
```bash
sudo apt-get install python3
```
- Pip:
```bash
sudo apt-get install python3-pip
```
- Compilador de C:
```bash
sudo apt-get install gcc
```

Para comparar también utilizamos numpy:
```bash
pip3 install numpy
```

## Ejecución

Creamos un archivo de C, en este caso llamado **modulo.c** con el siguiente código:

```c
#include <stdlib.h>

typedef struct {
    int n;
} FastFor;

FastFor *NewFastFor(int n) {
    FastFor *ff = malloc(sizeof(FastFor));
    ff->n = n;
    return ff;
}

unsigned long long Sum(FastFor *ff) {
    unsigned long long sum = 0;
    for (unsigned long long i = 0; i < ff->n; i++) {
        sum += i;
    }
    return sum;
}

void FreeFastFor(FastFor *ff) {
    free(ff);
}
```

Luego compilamos el archivo con el siguiente comando:

```bash
gcc -shared -fPIC -o libmodulo.so modulo.c
```

Y creamos un archivo de python llamado **test.py** con el siguiente código:

```python
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
```

Finalmente ejecutamos el archivo de python con el siguiente comando:

```bash
python3 test.py
```

Y obtenemos el siguiente resultado:

```bash
C++:  0.19051146507263184
Python:  6.651530742645264
Numpy:  0.3124837875366211
4999999950000000 4999999950000000 4999999950000000
```