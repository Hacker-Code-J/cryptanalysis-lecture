#-------------------------
# 암호분석 : TC1 - 전수조사 공격
#-------------------------
'''
 Toy Cipher TC1에 대한 키 전수조사 공격
 - 암호키: 24비트 key = [ 0, k1, k2, k3]
 
 공격조건(기지평문공격): 주어진 (평문, 암호문)에 대한 암호키를 찾는 문제

'''
#==================================================
# 주어진 조건: (평문, 암호문) = (given_pt, given_ct)
# 찾을 것: 암호키(key)
'''
(정답)
given_pt = [0, 1, 2, 3]
key = [0, 20, 20, 4]
given_ct = [192, 126, 66, 83]
'''
#==================================================

import TC1Lib as TC1


#----------------------------------------
# 함수 라이브러
#----------------------------------------
#--- int(4bytes) to list 0x12345678 -> [ 0x12, 0x34, 0x56, 0x78 ]
def int2list(n):
    out_list = []
    out_list.append( (n >> 24) & 0xff )
    out_list.append( (n >> 16) & 0xff )
    out_list.append( (n >>  8) & 0xff )
    out_list.append( (n      ) & 0xff )

    return out_list

#--- list to int [ 0x12, 0x34, 0x56, 0x78 ] -> 0x12345678
def list2int(l):
    n = 0
    num_byte = len(l)
    for i in range(len(l)):
        n += l[i] << 8*(num_byte - i -1)
        
    return n
#----------------------------------------



#==================================================
    
given_pt = [65, 82, 73, 65]
given_ct = [202, 134, 119, 230]

Flag = False    # If we found key, then Flag = True
KeySize = 1<<24 # 24-bit key

print('TC1 Exhaustive key search ...')
print('PT =', given_pt)
print('CT =', given_ct)

print('Key Searching ...', end=' ')

#[실습] -- 키 전수조사 공격 완성하기

for key_idx in range (0, KeySize): # 0, 1, ...,  2^24 - 1
    key_guess = int2list(key_idx)
    pt = TC1.TC1_Dec(given_ct, key_guess)
    if pt == given_pt:
        print("Key Found!")
        print("Key = ", key_guess)
        Flag = True
        # break
    if ((key_idx) % (1 << 16) == 0):
        print(' . ', end = ' ')


if Flag:
    print("Key Found!")
else:
    print("Key Not Found!")





















