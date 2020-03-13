// https://www.codewars.com/kata/526a569ca578d7e6e300034e/c

#include <math.h>
#include <string.h>

// from string.h (another implementation)
char *strrev(char *str) {
      char *p1, *p2;

      if (! str || ! *str)
            return str;
      for (p1 = str, p2 = str + strlen(str) - 1; p2 > p1; ++p1, --p2)
      {
            *p1 ^= *p2;
            *p2 ^= *p1;
            *p1 ^= *p2;
      }
      return str;
}

int index_of(const char value, const char * arr, size_t size) {
  int i;
  
  for (i = 0; i < size; i++) {
    if (value == arr[i]) return i;
  }
  
  return -1;
}

long long base_10(const char * input, const char * source, size_t size) {
  long long i;
  int input_size = strlen(input);
  long long result, p = 1;
  
  for (i = input_size - 1, result = 0; i >= 0; i--) {
    result += index_of(input[i], source, size) * p;
    p *= size;
  }
  
  return result;
}

// Translate the input string from the source alphabet to the target alphabet
char * convert(const char * input, const char * source, const char * target) {
  int source_base = strlen(source);
  int target_base = strlen(target);
  long long input_base_10 = base_10(input, source, source_base);
        
  char digit;
  int rem;
  long long div = 1;
  
  char* result;
  int result_size;
  
  result = (char*)malloc(sizeof(char) * 1);
  result_size = 1;
  result[result_size - 1] = '\0';
  
  while (div) {
    div = input_base_10 / target_base;
    rem = input_base_10 % target_base;
    digit = target[rem];
    
    result = (char*) realloc(result, sizeof(char) * (result_size + 1));
    result[result_size - 1] = digit;
    result[result_size] = '\0';
    result_size++;
    
    input_base_10 = div;
  }
  
  strrev(result);  
  return result;
}
