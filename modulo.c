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