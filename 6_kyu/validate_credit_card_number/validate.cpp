#include <iostream>
#include <vector>
#include <numeric>

int continuous_digits_sum(int n) {
    if (n < 10) return n;

    int sum = 0;
    while (n > 0) {
        sum += n % 10;
        n /= 10;
    }

    return continuous_digits_sum(sum);
}

class Kata {
    public:
    static bool validate(long long int n) {
        std::vector<int> digits;

        while (n > 0) {
            digits.insert(digits.begin(), n % 10);
            n /= 10;
        }

        auto idx_match = digits.size() % 2 == 0 ? 0 : 1;
        auto i = 0;
        for (auto& digit : digits) {
            if (i == idx_match) {
                digit = continuous_digits_sum(digit * 2);
                idx_match += 2;
            }

            i++;
        }

        return std::accumulate(digits.begin(), digits.end(), 0) % 10 == 0;
    }
};

int main()
{
    int input = 2121;
    std::cout << ">" << input << std::endl;
    std::cout << Kata::validate(input) << std::endl;
}