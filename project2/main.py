
import numpy as np

class LFSR:

    def __init__(self, mod: int, length: int, state: np.ndarray[int], coefficients: np.ndarray[int]):
        self.mod = mod
        self.length = length
        self.state = state
        self.coefficients = coefficients
    
    def clock(self) -> int:
        new = (-np.sum(self.coefficients*self.state) + 
               (self.state[0]+1)*int(not (self.state[3] >= 1 or self.state[2] >= 1 or self.state[1] >= 1))) % self.mod
        to_return = self.state[0]
        self.state = np.roll(self.state, -1)
        self.state[-1] = new
        return to_return

def de_bruijn(base: int, exp: int):

    nums = []

    if base == 2 and exp == 4:
        LFSR_2 = LFSR(base, exp, np.array([0, 0, 0, 1]), np.array([1, 0, 0, 1])) # x^4 + x + 1
        for _ in range(10**4+3):
            nums.append(LFSR_2.clock())
    

    elif base == 5 and exp == 4:
        LFSR_5 = LFSR(base, exp, np.array([0, 0, 0, 1]), np.array([2, 0, 2, 1])) # 2x^4 + 2x^2 + x + 1
        for _ in range(10**4+3):
            nums.append(LFSR_5.clock())
        
    return nums
    
if __name__ == "__main__":

    seq_2 = de_bruijn(2, 4)
    seq_5 = de_bruijn(5, 4)

    codes = set()
    nums = []

    for i in range(10**4+3):
        nums.append(5*seq_2[i%(2**4)]+seq_5[i%(5**4)] % 10)  
        if i >= 3:
            codes.add(str(nums[i]) + str(nums[i-1]) + str(nums[i-2]) + str(nums[i-3]))  

    print("\n".join(map(str, nums)))
    print(len(codes))
