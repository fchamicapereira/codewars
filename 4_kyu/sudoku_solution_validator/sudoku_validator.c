// https://www.codewars.com/kata/529bf0e9bdf7657179000008/c

#include<stdbool.h>

bool validSolution(unsigned int board[9][9]){
   int row, col, u;
   bool used[10];
   
   // validate rows
   for (row = 0; row < 9; row++) {
     for (u = 0; u < 10; u++) used[u] = false;
     for (col = 0; col < 9; col++) {
       if (used[board[row][col]]) return false;
       used[board[row][col]] = true;
     }
   }
   
   // validate columns
   for (col = 0; col < 9; col++) {
     for (u = 0; u < 10; u++) used[u] = false;
     for (row = 0; row < 9; row++) {
       if (used[board[row][col]]) return false;
       used[board[row][col]] = true;
     }
   }
   
   // validate squares
   for (row = 0; row <= 6; row+=3) {
     for (col = 0; col <= 6; col+=3) {
       for (u = 0; u < 10; u++) used[u] = false;
       
       if (used[board[row][col]]) return false;
       used[board[row][col]] = true;
       
       if (used[board[row][col+1]]) return false;
       used[board[row][col+1]] = true;
       
       if (used[board[row][col+2]]) return false;
       used[board[row][col+2]] = true;
       
       if (used[board[row+1][col]]) return false;
       used[board[row+1][col]] = true;
       
       if (used[board[row+1][col+1]]) return false;
       used[board[row+1][col+1]] = true;
       
       if (used[board[row+1][col+2]]) return false;
       used[board[row+1][col+2]] = true;
       
       if (used[board[row+2][col]]) return false;
       used[board[row+2][col]] = true;
       
       if (used[board[row+2][col+1]]) return false;
       used[board[row+2][col+1]] = true;
       
       if (used[board[row+2][col+2]]) return false;
       used[board[row+2][col+2]] = true;
     }
   }
   
   return true;
}
