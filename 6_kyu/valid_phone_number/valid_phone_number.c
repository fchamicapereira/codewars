// https://www.codewars.com/kata/525f47c79f2f25a4db000025/c

#include <stdbool.h>
#include <regex.h>
#include <stddef.h>

bool valid_phone_number(const char* number) {

  regex_t regex;
  int status;
  
  // compile regular expression
  if (regcomp(&regex, "^\([0-9][0-9][0-9]\) [0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]$", 0)) {
    // regex expression compilation error
    // should not happen
    return false;
  }
  
  /* Execute regular expression */
  status = regexec(&regex, number, 0, NULL, 0);
  regfree(&regex);
  
  if (status == REG_NOMATCH) {
      return false;
  }
  
  return true;
}
