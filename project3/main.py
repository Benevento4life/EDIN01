
import numpy as np
import time

st = time.time()

class LFSR:

    def __init__(self, mod: int, length: int, state: np.ndarray[int], coefficients: np.ndarray[int]):
        self.mod = mod
        self.length = length
        self.state = state
        self.coefficients = coefficients
    
    def clock(self) -> int:
        new = -np.sum(self.coefficients*self.state) % self.mod
        to_return = self.state[0]
        self.state = np.roll(self.state, -1)
        self.state[-1] = new
        return to_return

sequence = list(map(int, list("0000011101110100011000101101111000100110001101111101000100101001100010010110111110111000111101010001110110010111101111010110100101100101010000000011111110010100001000000101111011101010011011000")))
length = len(sequence)

polynomials = {13: np.array([1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1]), 
               15: np.array([1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0]), 
               17: np.array([1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0])}

def binary_list(x, size):
    x = list(map(int, bin(x)[2:]))
    x.reverse()
    while len(x) < size:
        x.append(0)
    x.reverse()
    return x

def hamming_distance(list1, list2):
    assert len(list1) == len(list2)
    ans = 0
    for i in range(len(list1)):
        ans += int(list1[i] == list2[i])
    return ans

def correlation(register_length):

    ans = -1
    maximum = 0

    for i in range(2**register_length-1):

        #print(type(initial_state), initial_state)
        
        register = LFSR(2, register_length, np.array(binary_list(i, register_length)), polynomials[register_length])
        tested_sequence = [register.clock() for _ in range(length)]
        hd = hamming_distance(tested_sequence, sequence)
        if hd/length >= 0.7: print(f"Unsually high correlation for the register with length {register_length}.")
        if maximum < hd:
            maximum = hd
            ans = i

    return ans, maximum/length

def majority(nums):
    a = list(nums)
    a.sort(); return a[len(a)//2]

def test_initial_sequence(initial_sequences):

    LFSR_13 = LFSR(2, 13, np.array(initial_sequences[0]), polynomials[13])
    LFSR_15 = LFSR(2, 15, np.array(initial_sequences[1]), polynomials[15])
    LFSR_17 = LFSR(2, 17, np.array(initial_sequences[2]), polynomials[17])

    for i in range(len(sequence)):
        num = majority((LFSR_13.clock(), LFSR_15.clock(), LFSR_17.clock()))
        if num == sequence[i]: continue
        return False
    return True


print(correlation(13))
print(correlation(15))
print(correlation(17))

print(test_initial_sequence([binary_list(199, 13), binary_list(952, 15), binary_list(84648, 17)])) # this is the correct solution

print(time.time()- st)

# An exhaustive search would take around 2^28/2 times longer. 
# This corresponds to Magnitude of 750 years on my laptop.
# Correlation attack runs in 3 minutes (thank god for numpy)
