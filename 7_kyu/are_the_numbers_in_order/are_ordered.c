// https://www.codewars.com/kata/56b7f2f3f18876033f000307/c

#include <stddef.h>
#include <stdbool.h>

bool in_asc_order(const int *arr, size_t arr_size) {
  int i;
  
  if (!arr_size) return false;
  
  for (i = 0; i < arr_size - 1; i++) {
    if (arr[i] > arr[i + 1]) return false;
  }

  return true;
}
