// https://www.codewars.com/kata/57f609022f4d534f05000024/c

#include <stddef.h>

int stray(size_t n, int arr[n]) {
    int constant, i;
    
    int first = arr[0];
    int second = arr[1];
    int third = arr[2];
        
    if (first == second || first == third) constant = first;
    else constant = second;
    
    for (i = 0; i < n; i++) {
      if (arr[i] != constant) return arr[i];
    }

    // something went wrong...
    return -1;
}
