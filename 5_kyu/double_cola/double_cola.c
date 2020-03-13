// https://www.codewars.com/kata/551dd1f424b7a4cdae0001f0/c

#include <stddef.h>
#include <stdbool.h>
#include <math.h>

const char *who_is_next(long long n, size_t length, const char *const a[length]) {
  
  long long bottom = 0;
  long long ceiling = 0;
  long long number_eq_elements = 0;
  long long group = 0;
  long long chosen = 0;
    
  while (1) {
    group += 1;
    number_eq_elements = pow(2, group - 1);
    
    bottom = ceiling + 1;
    ceiling += length * number_eq_elements;
    
    if (n >= bottom && n <= ceiling) break;
  }
  
  chosen = n - bottom;
  chosen -= chosen % number_eq_elements;
  chosen /= number_eq_elements;

  return a[chosen];
}