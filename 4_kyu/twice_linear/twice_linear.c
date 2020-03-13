// https://www.codewars.com/kata/5672682212c8ecf83e000050/c

#include <stdbool.h>
#define CACHE_LIMIT 3000000

bool belongs(int n) {
  static bool belongs_cached[CACHE_LIMIT] = {false};
  static bool belongs_cached_set[CACHE_LIMIT] = {false};

  if (n == 1) return true;

  if (n < CACHE_LIMIT && belongs_cached_set[n]) return belongs_cached[n];

  int ry = (n - 1) % 2;
  int rz = (n - 1) % 3;
  bool b;

  if (ry != 0 && rz != 0) { return false; }

  if (ry != 0 && rz == 0) {
    b = belongs((n - 1) / 3);
    if (n < CACHE_LIMIT) {
      belongs_cached_set[n] = true;
      belongs_cached[n] = b;
    }

    return b;
  }

  if (ry == 0 && rz != 0) {
    b = belongs((n - 1) / 2);
    if (n < CACHE_LIMIT) {
      belongs_cached_set[n] = true;
      belongs_cached[n] = b;
    }
    
    return b;
  }

  b = belongs((n - 1) / 3) || belongs((n - 1) / 2);
  if (n < CACHE_LIMIT) {
    belongs_cached_set[n] = true;
    belongs_cached[n] = b;
  }
  
  return b;
}

int dblLinear(int n) {
  int u = 1;
  int counter = 1;
  
  if (n == 0) return 1;

  while (counter <= n) {
    if (belongs(++u)) counter++;
  }
  
  return u;
}
