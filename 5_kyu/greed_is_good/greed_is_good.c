// https://www.codewars.com/kata/5270d0d18625160ada0000e4/c

#define SIDES 6

int score(const int dice[5]) {

    int triplet_points[SIDES] = {1000, 200, 300, 400, 500, 600};
    int single_points[SIDES] = {100, 0, 0, 0, 50, 0};
    
    int result = 0, used = -1;
    int result_tmp;
    
    int count[SIDES] = {0};
    
    int die, side;
    
    // count the occurance of each die side
    for (die = 0; die < 5; die++) {
      count[dice[die] - 1]++;
    }
    
    // look for the biggest triplet
    result_tmp = 0;
    for (side = 0; side < SIDES; side++) {
      if (count[side] >= 3 && triplet_points[side] > result_tmp) {
        result_tmp = triplet_points[side];
        used = side;
      }
    }
    
    // save
    result += result_tmp;
    
    // look for singles
    result_tmp = 0;
    for (side = 0; side < SIDES; side++) {
      if (side != used) {
        result_tmp += count[side] * single_points[side];
      } else if (count[side] > 3) {
        result_tmp += (count[side] - 3) * single_points[side];
      }
    }
    
    // save
    result += result_tmp;

    return result;
}
