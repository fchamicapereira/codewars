// https://www.codewars.com/kata/539a0e4d85e3425cb0000a88/solutions/cpp

#include <iostream>

class ChainableAdder
{
    int sum;

    public:
        ChainableAdder() { sum = 0; }
        ChainableAdder(const int n) { sum = n; }

        ChainableAdder operator()(const int n)
        {
            return ChainableAdder(sum + n);
        }

        ChainableAdder operator+(const int n){
            return ChainableAdder(sum + n);
        }

        ChainableAdder operator-(const int n){
            return ChainableAdder(sum - n);
        }

        friend bool operator==(const ChainableAdder& lhs, const ChainableAdder& rhs)
        {
            return lhs.sum == rhs.sum;
        }

        friend bool operator==(const int& lhs, const ChainableAdder& rhs)
        {
            return lhs == rhs.sum;
        }

        friend bool operator==(const ChainableAdder& lhs, const int& rhs)
        {
            return rhs == lhs;
        }

        friend std::ostream& operator<<(std::ostream& out, const ChainableAdder& ca)
        {
            out << ca.sum;
            return out;
        }
};

ChainableAdder add(int n)
{
    ChainableAdder ca;
    return ca(n);
}

int main()
{
    bool result = add(1)(2) == 2;
    std::cout << add(1)(2)(1) << std::endl;
    std::cout << add(1)(2) << std::endl;
    std::cout << result << std::endl;
}