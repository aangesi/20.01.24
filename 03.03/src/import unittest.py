import unittest
from typing import List

def find_primes(N: int) -> List[int]:
    """Функция для поиска всех простых чисел до N (включительно)."""
    if N < 2:
        return []
    primes = []
    is_prime = [True] * (N + 1)
    is_prime[0] = is_prime[1] = False
    for num in range(2, N + 1):
        if is_prime[num]:
            primes.append(num)
            for multiple in range(num * 2, N + 1, num):
                is_prime[multiple] = False
    return primes

class TestFindPrimes(unittest.TestCase):
    def test_small_numbers(self):
        self.assertEqual(find_primes(10), [2, 3, 5, 7])
        self.assertEqual(find_primes(20), [2, 3, 5, 7, 11, 13, 17, 19])
    
    def test_large_numbers(self):
        self.assertTrue(len(find_primes(1000)) > 0)
        self.assertTrue(len(find_primes(10000)) > 0)
    
    def test_edge_cases(self):
        self.assertEqual(find_primes(1), [])
        self.assertEqual(find_primes(0), [])
    
    def test_prime_identification(self):
        primes_under_50 = find_primes(50)
        for prime in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
            self.assertIn(prime, primes_under_50)
        for composite in [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24]:
            self.assertNotIn(composite, primes_under_50)

if __name__ == "__main__":
    unittest.main()
