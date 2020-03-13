// https://www.codewars.com/kata/52742f58faf5485cae000b9a/c

#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#define IYEAR 0
#define IDAY 1
#define IHOUR 2
#define IMINUTE 3
#define ISECOND 4

#define MINUTE (60)
#define HOUR (60 * MINUTE)
#define DAY (24 * HOUR)
#define YEAR (365 * DAY)

char *formatDuration (int n) {

  char *format = (char*) malloc(sizeof(char) * 500);
  char prefix[10];
  char unit[20];
  int chosen = 0;
  int parsed = 0;
  
  format[0] = '\0';
    
  if (n == 0) {
    format = (char*) realloc(format, sizeof(char) * 4);
    strcpy(format, "now\0");
    return format;
  }

  int duration[5] = { 0, 0, 0, 0, 0 };
  int components = 0;
  
  // get years
  duration[IYEAR] = n / YEAR;
  if (duration[IYEAR] > 0) components++;
  n = n % YEAR;
  
  // get days
  duration[IDAY] = n / DAY;
  if (duration[IDAY] > 0) components++;
  n = n % DAY;
  
  // get hours
  duration[IHOUR] = n / HOUR;
  if (duration[IHOUR] > 0) components++;
  n = n % HOUR;
  
  // get minutes
  duration[IMINUTE] = n / MINUTE;
  if (duration[IMINUTE] > 0) components++;
  n = n % MINUTE;
  
  // get seconds
  duration[ISECOND] = n;
  if (duration[ISECOND] > 0) components++;
  
  switch (components) {
    case 0:
      format = (char*) realloc(format, sizeof(char) * 4);
      strcpy(format, "now\0");
      return format;
    case 1:     
      for (int i = 0; i < 5; i++) {
        if (duration[i] == 0) continue;
        chosen = i;
        break;
      }
        
      switch (chosen) {
        case IYEAR:
          strcpy(unit, "year\0");
          break;
        case IDAY:
          strcpy(unit, "day\0");
          break;
        case IHOUR:
          strcpy(unit, "hour\0");
          break;
        case IMINUTE:
          strcpy(unit, "minute\0");
          break;
        case ISECOND:
          strcpy(unit, "second\0");
          break;
      }
      
      if (duration[chosen] > 1) {
        strcpy(unit + strlen(unit), "s\0");
      }
      
      sprintf(format, "%d %s\0", duration[chosen], unit);
      format = realloc(format, sizeof(char) * strlen(format));
      return format;
    
    default:
    
      for (int i = 0; i < 5; i++) {
        if (duration[i] == 0) continue;
        
        if (parsed == components - 1) {
          strcpy(prefix, " and \0");
        } else {
          strcpy(prefix, ", \0");
        }
        
        switch (i) {
          case IYEAR:
            strcpy(unit, "year\0");
            break;
          case IDAY:
            strcpy(unit, "day\0");
            break;
          case IHOUR:
            strcpy(unit, "hour\0");
            break;
          case IMINUTE:
            strcpy(unit, "minute\0");
            break;
          case ISECOND:
            strcpy(unit, "second\0");
            break;
        }
        
        if (duration[i] > 1) {
          strcpy(unit + strlen(unit), "s\0");
        }
        
        if (parsed == 0)
          sprintf(format + strlen(format), "%d %s\0", duration[i], unit);        
        else
          sprintf(format + strlen(format), "%s%d %s\0", prefix, duration[i], unit);        
        
        parsed++;
      }
  }
  
  format = realloc(format, sizeof(char) * strlen(format));
  return format;
}
