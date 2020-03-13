// https://www.codewars.com/kata/587731fda577b3d1b0001196/c

#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

char *camel_case(const char *s)
{
    char *cc = (char*) malloc(sizeof(char) * (strlen(s) + 1));
    int i = 0;
    bool ws = false;
    
    while (*s != '\0') {
      if (isspace(*s)) {
        ws = true;
        s++;
        continue;
      }
      
      if ((ws || i == 0) && isalpha(*s)) {
        cc[i] = (char) toupper(*s);
        ws = false;
      } else {
        cc[i] = *s;
      }
    
      s++; i++;
    }
    
    cc[i] = '\0';
    cc = (char*) realloc(cc, sizeof(char) * (strlen(cc) + 1));
    
    return cc;
}
