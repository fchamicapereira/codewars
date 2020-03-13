// https://www.codewars.com/kata/5629db57620258aa9d000014/c

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define valid_char(c) (c >= 97 && c <= 122)
#define char_to_i(c) ((int) (c - 97))
#define i_to_char(i) ((char) (i + 97))

int cmpfunc (const void * a, const void * b) {
  const char *sa = *((const char **) a);
  const char *sb = *((const char **) b);

  int la = strlen(sa);
  int lb = strlen(sb);
  
  if (la != lb) return lb - la;

  for (int i = 0; i < la; i++) {
    if (sa[i] != sb[i]) return (int) (sa[i] - sb[i]);
  }

  return (int) (sa[la - 1] - sb[lb - 1]);
}

char** append(char **substrings, int nsubstrings, char s, char c, int n) {
  int size;

  substrings = (char**) realloc(substrings, sizeof(char*) * (++nsubstrings));
  
  size = 2 + n + 1;
  substrings[nsubstrings-1] = (char*) malloc(sizeof(char) * size);
  
  sprintf(substrings[nsubstrings-1], "%c:", s);
  memset(&(substrings[nsubstrings-1][2]), c, n);
  substrings[nsubstrings-1][size - 1] = 0;

  return substrings;
}

char* mix(char* s1, char* s2) {
  char *result = NULL;
  char **substrings = NULL;
  int nsubstrings = 0;
  char *cursor;
  int s1_counter[26] = {0};
  int s2_counter[26] = {0};

  substrings = (char**) malloc(sizeof(char*));
  
  cursor = s1;
  while (*cursor != 0) {
    if (valid_char(*cursor)) s1_counter[char_to_i(*cursor)]++;
    cursor++;
  }
  
  cursor = s2;
  while (*cursor != 0) {
    if (valid_char(*cursor)) s2_counter[char_to_i(*cursor)]++;
    cursor++;
  }
  
  for (int i = 0; i < 26; i++) {
    if (s1_counter[i] <= 1 && s2_counter[i] <= 1) continue;

    if ((s1_counter[i] > 1 && s2_counter[i] <= 1) || s1_counter[i] > s2_counter[i]) {
      substrings = append(substrings, nsubstrings++, '1', i_to_char(i), s1_counter[i]);
      continue;
    }

    if ((s1_counter[i] <= 1 && s2_counter[i] > 1) || s1_counter[i] < s2_counter[i]) {
      substrings = append(substrings, nsubstrings++, '2', i_to_char(i), s2_counter[i]);
      continue;
    }

    if (s1_counter[i] == s2_counter[i]) 
      substrings = append(substrings, nsubstrings++, '=', i_to_char(i), s1_counter[i]);
  }

  qsort(substrings, nsubstrings, sizeof(char*), cmpfunc);

  int size = 1;
  result = (char*) malloc(sizeof(char));
  result[0] = 0;

  for (int i = 0; i < nsubstrings; i++) {
    size += strlen(substrings[i]) + 1;
    
    result = (char*) realloc(result, sizeof(char) * size);

    strlen(result) == 0
      ? sprintf(result, "%s", substrings[i])
      : sprintf(result, "%s/%s", result, substrings[i]);

    result[size - 1] = 0;
    free(substrings[i]);
  }
  free(substrings);

  return result;
}
