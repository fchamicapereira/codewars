// https://www.codewars.com/kata/54ff3102c1bad923760001f3/c

#include <stddef.h>

size_t get_count(const char *s)
{
    size_t count = 0;
    
    // all char arrays must end on a \0 character
    while (*s != '\0') {
    
        // true = 1, false = 0
        count += (
          *s == 'a' || *s == 'e' ||
          *s == 'i' || *s == 'o' ||
          *s == 'u'
        );
        
        // step pointer
        s += 1;
    }
    
    return count;
}
