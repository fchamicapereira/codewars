// https://www.codewars.com/kata/56269eb78ad2e4ced1000013

#include <cmath>

long int findNextSquare(long int sq) {
  long int base = (long int) std::sqrt((double) sq);
  if (base * base != sq) return -1;
  return (base+1)*(base+1);
}