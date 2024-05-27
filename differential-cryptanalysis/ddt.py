# DDT = Differential Distribution Table
# S is a list of integers giving the values of the S-box
# n = number of input bits
# m = number of output bits

def ddt(S, n ,m):
    D = [[0] * (2 ** m) for _ in range(2 ** n)]
    for alpha in range(2 ** n):
        for x in range(2 ** n):
            beta = S[x] ^ S[x ^ alpha]
            D[alpha][beta] += 1
    return D

# S is a list of integers giving the values of the S-Box
# n = number of input bits
# m = number of output bits
def print_ddt(S, n, m):
    D = ddt(S, n ,m)
    for alpha in range(2 ** n):
        for beta in range(2 ** m):
            d = str(D[alpha][beta]).rjust(2)
            print(d, end='  ')
        print()
        
def print_ddt_to_file(S, n, m):
    D = ddt(S, n , m)
    ddt_txt_file = open("ddt.txt", "w")
    first_row = '|'.rjust(4)
    for i in range(2 ** m):
        first_row += str(hex(i))[2:].rjust(4)
    print(first_row, file = ddt_txt_file)
    horizontal_divider = '-' * len(first_row)
    print(horizontal_divider, file = ddt_txt_file)
    for alpha in range(2 ** n):
        row_string = ''
        row_string += str(hex(alpha))[2:].rjust(3) + '|  '
        for beta in range(2 ** m):
            d = D[alpha][beta]
            row_string += str(d).rjust(3) + ' '
        print(row_string, file = ddt_txt_file)
    ddt_txt_file.close()
    
# 3-bit S-Box function
S = [0, 1, 3, 2, 6, 7, 5, 4]
S2 = [0, 1, 7, 2, 3, 4, 5, 6]
S3 = [2, 3, 5, 6, 4, 7, 0, 1]

print_ddt(S3, 3, 3)