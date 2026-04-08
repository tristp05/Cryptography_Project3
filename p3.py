#!/usr/bin/env python3
print("By: Tristan Price, Nathan Byun, Ahran Dymond, Barrett Larson")
"""
PART 1
"""
print("--- PART 1: Linear Approximation Table ---")
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
print("\n\n")

"""
PART 2
"""
print("--- PART 2: Linear Approximation Trail ---")
print("Trace connecting plaintext bits P1, P2, P4, P5 to bit H1:")
print("1. Round 1, S11: Input mask a=6 (P1, P2). Output mask b=4 (B1).")
print("2. Round 1, S12: Input mask a=6 (P4, P5). Output mask b=4 (B4).")
print("3. Permutation: B1 connects to E1, and B4 connects to E2.")
print("4. Round 2, S21: Input mask a=6 (E1, E2). Output mask b=4 (F1).")
print("5. Permutation: F1 connects directly to H1.")
print("Conclusion: The trail uses three active S-boxes (S11, S12, S21), all with input sum 6 and output sum 4.\n")

# ASCII Art Sketch of the Trail
sketch = """
   --- ACTIVE LINEAR TRAIL SKETCH ---
   
   Plaintext Bits:   P1  P2      P4  P5
                      |   |       |   |
                      v   v       v   v
                    +-------------------+
                    |  Subkey K1 Mixing |
                    +-------------------+
                      |   |       |   |
                      v   v       v   v
                    +-------+   +-------+
                    |  S11  |   |  S12  |
                    +-------+   +-------+
                      |           |      
                     B1          B4      
                       \           \     
                        \           \    (Permutation layer)
                         \          /    (B1 -> E1, B4 -> E2)
                          \        /     
                           v      v      
                    +-------------------+
                    |  Subkey K2 Mixing |
                    +-------------------+
                           |      |      
                           v      v      
                         +----------+    
                         |   S21    |    
                         +----------+    
                           |             
                          F1             
                           |             
                           v             
                    +-------------------+
                    |  Subkey K3 Mixing |
                    +-------------------+
                           |             
                           v             
                          H1             
   
   ----------------------------------
"""
print(sketch)

"""
PART 3
"""
print("\n--- PART 3: Total Bias of the Trail ---")
# S-boxes all use a = 6 and b = 4
a, b = 6, 4

# Recalculate NL(6,4) to find the bias
count = 0
for x in range(8):
    if parity(a & x) == parity(b & sbox[x]):
        count += 1

nl_minus_4 = count - 4
epsilon = nl_minus_4 / 8.0

print(f"Bias for each active S-box (input sum {a}, output sum {b}) is: {nl_minus_4} / 8 = {epsilon}")

# Applying the Piling-Up Lemma for l=3 active S-boxes
# Formula: Total Bias = 2^(l-1) * (epsilon_1 * epsilon_2 * ... * epsilon_l)
l = 3
total_bias = (2**(l - 1)) * (epsilon**l)

print(f"Total bias of the linear approximation trail using Piling-Up Lemma: {total_bias}\n")

"""
PART 4
"""
print("\n--- PART 4: Counter Values of Each Key ---")
S_box = {0:6, 1:5, 2:1, 3:0, 4:3, 5:2, 6:7, 7:4}

# Inverse S-box
S_box_inv = {}
for i in range(len(S_box)):
    S_box_inv[S_box[i]] = i

pairs = [
    (0b100111, 0b100100),
    (0b000111, 0b110010),
    (0b001100, 0b111001),
    (0b011000, 0b011101),
    (0b001000, 0b001101),
    (0b011010, 0b101001),
]

for key in range(8):
    count = 0
    for pair in range(len(pairs)):
        p = pairs[pair][0]
        c = pairs[pair][1] >> 3
        P1 = (p >> 5) & 1
        P2 = (p >> 4) & 1
        P4 = (p >> 2) & 1
        P5 = (p >> 1) & 1
        v = key ^ c
        u = S_box_inv[v]
        H1 = (u >> 2) & 1
        z = P1 ^ P2 ^ P4 ^ P5 ^ H1
        if z == 0: 
            count += 1
        
    print("Counter for", (bin(key)), "=", count)

"""
PART 5
"""
print("\n\n--- PART 5: First and Third bits of Subkey ---")
print("Key has 6 pairs -> expected random behavior ~3")
print("Find counter with largest bias from 3")
print("Counter for 0b000=6 and counter for 0b010=0 are furthest from 3, 0b000=6 is preffered due to sign")
print("\tCounter for 0b000=6\n\t\tbit1:0 bit2:0 bit3:0")
print("\tCounter for 0b010=0\n\t\tbit1:0 bit2:1 bit3:0")
print("bit1=0, bit3=0")


"""
PART 6
"""
print("\n\n--- PART 6: Second bit Insufficiency ---")
print("Bit2 of K4 can not be determined because it does not show consistent bias.\n" \
"For the strongest candidates bit1 and bit3 are consistent but bit2 varies.\n" \
"Therefore it is not possible to determine the second bit from this approximation.\n")
