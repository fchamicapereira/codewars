// https://www.codewars.com/kata/56c04261c3fcf33f2d000534/c

#define v(k,n) ( ((double) 1) / (k * pow(n + 1, 2 * k)) )

double doubles(int maxk, int maxn) {
  double s = 0;
  for (int k = 1; k <= maxk; k++)
    for (int n = 1; n <= maxn; n++)
      s += v(k,n);
  return s;
}
