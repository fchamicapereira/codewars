// https://www.codewars.com/kata/51ba717bb08c1cd60f00002f/c

#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include <string.h>

int ndigits(int n) {
  int count = 0;
  
  if (n < 0) { n *= -1; count++; }

  while(n != 0)
  {
      n /= 10;
      ++count;
  }
  
  return count;
}

char* append(char* str, int n, char separator) {
  int old_size = str == NULL ? 0 : strlen(str);
  int size = old_size + 1 + ndigits(n);
  
  str = (char*) realloc(str, sizeof(char) * (size + 1));
  
  if (old_size == 0) {
    sprintf(str + old_size, "%d", n);  
  } else {
    sprintf(str + old_size, "%c%d", separator, n);
  }
  
  return str;
}

char *range_extraction(const *args, size_t n)
{
  int start, end;
  bool combo;
  int i;
  
  char * list = NULL;
  
  for (i = 0, combo = false; i < n; i++) {
  
    if (combo && args[i] == end + 1) {
      end++;
      if (i < n-1) continue;
    } 
    
    else if (!combo && i > 0 && args[i] == start + 1) {
      end = args[i];
      combo = true;
      if (i < n-1) continue;
    }
    
    // broken combo
    if (combo && (args[i] != end + 1 || i == n - 1)) {
    
      if (end - start >= 2) {
        list = append(list, end, '-');
      } else {
        list = append(list, end, ',');
      }
      
      combo = false;
    }
    
    if (args[i] == end) continue;
          
    start = args[i];
    list = append(list, start, ',');    
    combo = false;
  }
    
  return list;
}
