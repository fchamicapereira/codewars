// https://www.codewars.com/kata/550f22f4d758534c1100025a/c

#include <stdbool.h>

// arr: directions to reduce, sz: size of arr, lg size of returned array
// function result will be freed
char** dirReduc(char** arr, int sz, int* lg) {
  
  int i, ii;
  bool found;
  int adjacent;
  char ** result;
  
  // setup
  bool * keep = (bool*) malloc(sizeof(bool) * sz);
  *lg = sz;
  for (i = 0; i < sz; i++) {
    keep[i] = true; 
  }
  
  found = true;
  while (found) {
    found = false;
    
    for (i = 0; i < sz - 1; i++) {
      if (!keep[i]) continue;
      
      // find the next direction to keep
      adjacent = -1;
      for (ii = i + 1; ii < sz; ii++) {
        if (!keep[ii]) continue;
        adjacent = ii;
        break;
      }
      
      // no adjacent direction
      if (adjacent == -1) break;
      
      if (
        (!strcmp(arr[i], "NORTH") && !strcmp(arr[adjacent], "SOUTH")) ||
        (!strcmp(arr[i], "SOUTH") && !strcmp(arr[adjacent], "NORTH")) ||
        (!strcmp(arr[i], "EAST") && !strcmp(arr[adjacent], "WEST")) ||
        (!strcmp(arr[i], "WEST") && !strcmp(arr[adjacent], "EAST"))
      ) {
        keep[i] = false;
        keep[adjacent] = false;
        found = true;
        *lg -= 2;
      }
    }
  }
  
  result = (char**) malloc(sizeof(char*) * (*lg));
  for (i = 0, ii = 0; i < sz; i++) {
    if (!keep[i]) continue;
    result[ii++] = arr[i];
  }
  
  free(keep);
  
  return result;  
}
