// https://www.codewars.com/kata/5544c7a5cb454edb3c000047/c

int bouncingBall(double h, double bounce, double window) {
    int seen = 0;
    
    if (h <= 0 || bounce >= 1 || bounce <= 0 || window >= h) return -1;
    
    // the ball will be seen when the ball is dropped, before bouncing
    if (h > window) seen++;
    
    // when the ball bounces, and if the bounce will make the ball reach
    // the mother, it will be 2x (when climbing and when falling)
    if (h * bounce > window)
      seen += bouncingBall(h * bounce, bounce, window) + 1;
    
    return seen;
}
