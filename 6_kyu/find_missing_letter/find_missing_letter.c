// https://www.codewars.com/kata/5839edaa6754d6fec10000a2/c

char findMissingLetter(char array[], int arrayLength)
{
  int i;
  for (i = 1; i < arrayLength; i++) {
    if (array[i] != (char)((int)array[i - 1] + 1)) {
      return (char)((int)array[i - 1] + 1);
    }
  }
  return '\0';
}
