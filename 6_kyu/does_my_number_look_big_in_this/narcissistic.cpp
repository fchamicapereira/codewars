// https://www.codewars.com/kata/5287e858c6b5a9678200083c

#include <cmath>

int intPow(int base, int power) {
  if (power == 0) return 1;
  if (power == 1) return base;
  
  int tmp = intPow(base, power / 2);
  if (power % 2 == 0) return tmp * tmp;
  else return base * tmp * tmp;
}

bool narcissistic( int value ) {
  int sum = 0;
  int digits = value < 10 ? 1 : ceil(std::log10f((float)value));
  int digit;
  
  for (int idx = 0; idx < digits; idx++) {
    digit = (value / intPow(10, idx)) % 10;
    sum += intPow(digit, digits);
  }
  
  return sum == value;
}