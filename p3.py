#!/usr/bin/env python3
"""
PART 1
"""
# S-box mapping: sbox[x] = S(x) for x = 0 to 7
sbox = [6, 5, 1, 0, 3, 2, 7, 4]

def parity(n: int) -> int:
    """Return the parity (mod-2 dot product) of the bits in n.
    Equivalent to the linear equation a·x (mod 2)."""
    return bin(n).count('1') % 2

# Compute the full 8x8 normalized LAT
print("Normalized Linear Approximation Table NL(a, b) - 4")
print("Rows = input sum a (0-7 hex), Columns = output sum b (0-7 hex)")
print("Entry formula: NL(a, b) - 4   (as specified in Project 3)")

# Header row
print("   ", end="")
for b in range(8):
    print(f" {b:1X} ", end="")
print()
print("   " + "-" * (8 * 4))  # separator

# Fill and print the table
for a in range(8):
    print(f"{a:1X} |", end="")
    for b in range(8):
        count = 0
        for x in range(8):
            # Check if a·x == b·S(x) (mod 2)
            if parity(a & x) == parity(b & sbox[x]):
                count += 1
        nl = count
        entry = nl - 4
        # Print with sign and alignment (matches style of class notes table)
        if entry >= 0:
            print(f" +{entry:1d} ", end="")
        else:
            print(f" {entry:2d} ", end="")
    print()
print("\n")

"""
PART 2
"""


"""
PART 3
"""


"""
PART 4
"""


"""
PART 5
"""


"""
PART 6
"""
