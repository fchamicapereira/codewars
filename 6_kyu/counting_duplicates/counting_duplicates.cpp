// https://www.codewars.com/kata/54bf1c2cd5b56cc47f0007a1

#include <set>
#include <string>

size_t duplicateCount(const std::string& in); // helper for tests

size_t duplicateCount(const char* in)
{
  std::set<char> characters;
  std::set<char> counted;
  int count = 0;
  char c;
  
  for (int idx = 0; idx < strlen(in); idx++) {
    c = tolower(in[idx]);
    if (characters.find(c) == characters.end()) characters.insert(c);
    else if (counted.find(c) == counted.end()) {
      count++;
      counted.insert(c);
    }
  }
  return count;
}