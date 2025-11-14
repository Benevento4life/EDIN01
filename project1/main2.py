
import numpy as np
from math import sqrt, gcd, floor, ceil
import subprocess
from time import process_time

def first_n_primes(n: int) -> list[int]:

    primes = []
    sieve = [True for i in range(30*n)]
    for i in range(2, len(sieve)):
        if len(primes) == n: return primes
        if not sieve[i]: continue
        primes.append(i)
        for j in range(2*i, len(sieve), i):
            sieve[j] = False

def is_smooth(n: int, factorbase: list[int]) -> bool:

    for p in factorbase:
        while n % p == 0:
            n //= p
    return n == 1

def factor(n: int, factorbase: list[int], index: int) -> None:
    for i in range(len(factorbase)):
        p = factorbase[i]
        while n % p == 0:
            n //= p
            smooth_numbers[index][i] += 1

N = int(input("What number do you want to factor? "))
no_of_primes = int(input("How large of a factorbase do you want? (1024 is recommended) ")) # 2**10

st = process_time()

factorbase = first_n_primes(no_of_primes)

smooth_numbers = np.zeros((no_of_primes +5, no_of_primes), dtype=int)
x_is = np.zeros(no_of_primes+5, dtype=int)
k = 1
j = 0
index = 0
seen = set()
while index < no_of_primes+5:
    x = ceil(sqrt(k*N))+j    
    y = x*x % N
    if y == 0: 
        print(x, x)
        print("CPU time:", process_time()-st)
        exit()
    if is_smooth(y, factorbase): 
        x_is[index] = x
        factor(y, factorbase, index)
        binary_exponents = tuple((np.ones(no_of_primes, int) * smooth_numbers[index]) % 2) 
        if binary_exponents not in seen:
            seen.add(binary_exponents)
            index += 1
            print(index)
    if k > 10: 
        k = 1
        j += 1
    else: k += 1
print(x_is, [x*x % N for x in x_is])
print(smooth_numbers)

with open("project1/input.txt", "w") as file:
    file.write(f"{no_of_primes+5} {no_of_primes}")
    for i in range(no_of_primes+5):
        file.write("\n")
        file.write(" ".join(str(x) for x in smooth_numbers[i]))


result = subprocess.run(["./project1/gauss.out", "project1/input.txt", "project1/output.txt"], capture_output=True)
print(result.stdout)
print(result.stderr)

with open("project1/output.txt", "r") as file:
    no_of_solutions = int(file.readline())
    solutions = np.zeros((no_of_solutions, no_of_primes+5), dtype=int)

    i = 0
    for line in file.readlines():
        solutions[i] = np.array(list(map(int, line.split())))
        i += 1
print(len(solutions[0]))
print(solutions)

x_solutions = [1 for _ in range(no_of_solutions)]
for i in range(no_of_solutions):
    for j in range(no_of_primes+5):
        x_solutions[i] = (x_solutions[i] * int(pow(x_is[j], int(solutions[i][j])))) % N
    print(i)

y_solutions = [1 for _ in range(no_of_solutions)]
for i in range(no_of_solutions):
    total_exponents = np.sum(smooth_numbers*solutions[i][:, np.newaxis], axis=0)
    print(total_exponents)
    for j in range(no_of_primes):
        y_solutions[i] = y_solutions[i] * int(pow(factorbase[j], int(total_exponents[j])//2, N)) % N
    print(i)
print(x_is)
print(x_solutions)
print("\n\n\n")
print(y_solutions)

for i in range(no_of_solutions):
    a = gcd(N, x_solutions[i]+y_solutions[i])
    if a in [1, N]:
        continue
    print(a, N//a)
    print("CPU time:", process_time()-st)
    exit()
print("Prime number?")
print("CPU time:", process_time()-st)
