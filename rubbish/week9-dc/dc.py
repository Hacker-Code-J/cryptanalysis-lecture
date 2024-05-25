#=====
# DC Table
#=====

# 3-bit S-Box Function
# S = [0, 1, 3, 2, 6, 7, 5, 4]
S = [0, 1, 7, 2, 3, 4, 5, 6]
#S = [4, 5, 6, 7, 0, 1, 2, 3]

for i in range(len(S)):
    print(f'S[{i}]={S[i]}')
    # print('S[%d]=%d', %(i,S[i]))

# DC Table [dx][dy]
# dx -> [S] -> dy
# DTable[dx][dy] = count[dx --> dy]

# Table Size = n
n = len(S) # n = 2^k for some k-bit

DTable = []
for i in range(n):
    DTable.append([0]*n) # [0,0,...,0]

# dx = x1 ^ x^2 = 0, 1, ..., n-1 = 2^k-1
# 3-bit S-Box => dx = 0, 1, ..., 7
'''
for dx in range(n):
    for x1 in range(n):
        x2 = dx ^ x1 # (dx = x1 ^ x2) => (x2 = dx ^ x1)
        y1 = S[x1]
        y2 = S[x2]
        dy = y1 ^ y2
        DTable[dx][dy] += 1
'''

for x1 in range(n):
    y1 = S[x1]
    for dx in range(n):
        x2 = dx ^ x1
        y2 = S[x2]
        dy = y1 ^ y2
        DTable[dx][dy] += 1


print('\nDC Table for S[]\n')
print('    ', end='')
for dy in range(n):
    print('%3d ' %(dy), end='')
print('\n')
for dx in range(n):
    print('%3d ' %(dx), end='')
    for dy in range(n):
        print('%3d ' %(DTable[dx][dy]), end='')
    print('\n')

# Find max P[dx -> dy]
max_cnt, max_dx, max_dy = 0, 0, 0
for dx in range(1, n): # n != 0
    for dy in range(n):
        if DTable[dx][dy] > max_cnt:
            max_cnt = DTable[dx][dy]
            max_dx = dx
            max_dy = dy

print(f'Max Count = {max_cnt} ({max_dx} -> {max_dy})')
print(f'Max Probability P[dx -> dy] = {max_cnt/n}')

# Print dx, dy s.t. P[dx -> dy] is max
# Renewal or Repeat
# -> Assignment!



