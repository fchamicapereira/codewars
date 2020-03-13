// https://www.codewars.com/kata/550498447451fbbd7600041c/c

#include <stdbool.h>
#include <stdlib.h>

int cmpfunc (const void *a, const void *b) {
   return ( *(int*)a - *(int*)b );
}

bool comp(const int *a, const int *b, size_t n)
{   
    if (a == NULL || b == NULL) return false;
    
    // empty arrays are the "same"
    if (!n) return true;
    
    // sorting the arrays
    qsort(a, n, sizeof(int), cmpfunc);
    qsort(b, n, sizeof(int), cmpfunc);
    
    while (n > 0) {
      if (*b != (*a) * (*a)) return false;
      
      // updating
      n -= 1; a++; b++;
    }
    
    return true;
}
