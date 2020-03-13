// https://www.codewars.com/kata/51b66044bce5799a7f000003/c

#include <string.h>

int from_roman(char* roman)
{
  int n = 0;
  int prev = 0;
  
  while (*roman != '\0') {
    switch (*roman) {
      case 'M':
        if (prev == 100) n += 800;
        else n += 1000;
        prev = 1000;
        break;
      case 'D':
        if (prev == 100) n += 300;
        else n += 500;
        prev = 500;
        break;
      case 'C':
        if (prev == 10) n += 80;
        else n += 100;
        prev = 100;
        break;
      case 'L':
        if (prev == 10) n += 30;
        else n += 50;
        prev = 50;
        break;
      case 'X':
        if (prev == 1) n += 8;
        else n += 10;
        prev = 10;
        break;
      case 'V':
        if (prev == 1) n += 3;
        else n += 5;
        prev = 5;
        break;
      case 'I':
        n += 1;
        prev = 1;
        break;
    }
    
    roman++;
  }
  
  return n;
}

void to_roman(int number, char* destination)
{
  int size = 1;
  int s = 0;
  char d[4];
  
  destination[size] = '\0';
  
  printf("%d => %s\n", number, destination);
  
  size += number / 1000;
  for (int i = 0; i < number / 1000; i++) destination[i] = 'M';
  number = number % 1000;

  s = 0;
  d[0] = '\0';
  switch (number / 100) {
    case 1:
      strcpy(d, "C\0");
      s = 1;
      break;
    case 2:
      strcpy(d, "CC\0");
      s = 2;
      break;
    case 3:
      strcpy(d, "CCC\0");
      s = 3;
      break;
    case 4:
      strcpy(d, "CD\0");
      s = 2;
      break;
    case 5:
      strcpy(d, "D\0");
      s = 1;
      break;
    case 6:
      strcpy(d, "DC\0");
      s = 2;
      break;
    case 7:
      strcpy(d, "DCC\0");
      s = 3;
      break;
    case 8:
      strcpy(d, "DCCC\0");
      s = 4;
      break;
    case 9:
      strcpy(d, "CM\0");
      s = 2;
      break;
  }
   
  printf("d %s %d\n", d, size);
  strcpy(destination+size-1, d);
  number = number % 100;
  size += s;
  
  s = 0;
  d[0] = '\0';
  switch (number / 10) {
    case 1:
      strcpy(d, "X\0");
      s = 1;
      break;
    case 2:
      strcpy(d, "XX\0");
      s = 2;
      break;
    case 3:
      strcpy(d, "XXX\0");
      s = 3;
      break;
    case 4:
      strcpy(d, "XL\0");
      s = 2;
      break;
    case 5:
      strcpy(d, "L\0");
      s = 1;
      break;
    case 6:
      strcpy(d, "LX\0");
      s = 2;
      break;
    case 7:
      strcpy(d, "LXX\0");
      s = 3;
      break;
    case 8:
      strcpy(d, "LXXX\0");
      s = 4;
      break;
    case 9:
      strcpy(d, "XC\0");
      s = 2;
      break;
  }
  
  printf("d %s %d\n", d, size);
  strcpy(destination+size-1, d);
  number = number % 10;
  size += s;
  
  s = 0;
  d[0] = '\0';
  switch (number) {
    case 1:
      strcpy(d, "I\0");
      s = 1;
      break;
    case 2:
      strcpy(d, "II\0");
      s = 2;
      break;
    case 3:
      strcpy(d, "III\0");
      s = 3;
      break;
    case 4:
      strcpy(d, "IV\0");
      s = 2;
      break;
    case 5:
      strcpy(d, "V\0");
      s = 1;
      break;
    case 6:
      strcpy(d, "VI\0");
      s = 2;
      break;
    case 7:
      strcpy(d, "VII\0");
      s = 3;
      break;
    case 8:
      strcpy(d, "VIII\0");
      s = 4;
      break;
    case 9:
      strcpy(d, "IX\0");
      s = 2;
      break;
  }
  
  strcpy(destination+size-1, d);
}