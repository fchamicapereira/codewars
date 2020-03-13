// https://www.codewars.com/kata/541c8630095125aba6000c00

int digital_root(int n)
{  
    int sum = 0;
    if(n <10) return n;
    while( n > 0 ) {
      sum += n%10;
      n /= 10;
    }
    return digital_root(sum);
}
