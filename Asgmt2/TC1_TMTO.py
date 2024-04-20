#----------------------------------
# 암호분석 
#
# TC1에 대한 TMTO 공격
# - 평문/암호문: 32비트, 암호키:24비트
# - 파라미터 설정: m=t=l=2^8 (mtl = 2^24)
# - 메모리(M) = m*l = 2^16
# - 계산량(T) = t*l = 2^16
#----------------------------------

import TC1Lib as TC1
import pickle # 변수저장
import random # 난수생성
import copy   # deep copy 


#============================================================
# 이전에 만든 함수들
#============================================================
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

#- 변수를 파일에 저장하기
def save_var_to_file(var, filename):
    f = open(filename, 'w+b')
    pickle.dump(var, f)
    f.close()
    
#- 파일에서 변수를 가져오기
def load_var_from_file(filename):
    f = open(filename, 'rb')
    var = pickle.load(f)
    f.close()
    return var
#============================================================
    
#--------------------------------
# 평문-암호문(32비트): PT = [*,*,*,*] --> CT = [*,*,*,*]
# 키 크기 - 공격시간을 고려하여 24비트 키로 한정함: key = [0,*,*,*]
key_bit = 24 # 키공간 24비트 key = [0,*,*,*]

#---------------------------------
# TMTO Table: { (SP:EP) }
#   #SP = #EP = 2^8,   #chains: m = 2^8, #tables: l = 2^8

#============================================================
# P0 : 선택평문 (공격자가 획득 가능한 암호문에 대응되는 평문)
# X_{j+1} = E(P0, X_{j})  # key bit = block size 인 경우
# X_{j+1} = R( E(P0, X_{j}) )  # R: 32비트 [*,*,*,*] -> 24비트 [0,*,*,*]
# SP = X0(Key) -> X1 -> X2 -> ... -> Xt = EP  (encryption key chain)
#============================================================

#------------
# 암호문(32비트)을 다음 단계 암호키(24비트)로 만드는 함수
# R: 32비트 -> 24비트 
# R: [a,b,c,d] -> [0,b,c,d]
def R(ct):
    #next_key = ct
    next_key = copy.deepcopy(ct)
    next_key[0] = 0
    return next_key

#-------------
# Encryption key chain 만들기
#   SP = (24비트 랜덤키)
#   P0 = (선택평문, 고정값)    
#    t = 체인의 길이
def chain_EP(SP, P0, t):
    Xj = SP
    for j in range(0,t):
        ct = TC1.TC1_Enc(P0, Xj)
        Xj = R(ct)   # next Xj (출력 암호문 32비트를 암호키 24비트로)
    return Xj

#===========
# chain 만들기 - 확인용 화면출력 함수 (공격에는 불필요)    
def chain_EP_debug_print(SP, P0, t):
    Xj = SP
    print('SP =', SP)
    for j in range(0,t):
        ct = TC1.TC1_Enc(P0, Xj)
        Xj = R(ct)   # next Xj 
        print(' -> ', ct, ' -> ', Xj)
    return Xj



# 선택평문 (TMTO 테이블 전체에서 고정된 값으로 사용)
P0 = [1,2,3,4]
# 공격 파라미터 설정
m = 256             # m: 한 테이블에 들어가는 체인의 개수
t = 256             # t: 체인의 길이
num_of_tables = 256 # 테이블 개수


#=====================
# (단계2) 온라인 공격(획득 암호문에 대한 암호키 찾기)
# (단계1에서 만든 사전파일을 이용하여 공격하는 과정)
#=====================


#=====
# random.seed(2024)으로 만든 TMTO 테이블용 샘플
#=====
'''
PTCT for TMTO attack
pt1 = [1, 2, 3, 4]
ct1 = [224, 255, 196, 177]
pt2 = [5, 6, 7, 8]
ct2 = [71, 69, 245, 137]
key = [0, 23, 36, 6]
'''

#--------------
# 한개의 테이블에 대한 키 탐색 함수
def one_tmto_table_search(ct, P0, m, t, ell):
    key_candid_list = []
    file_name = 'tmto_table/TMTO-' + str(ell) + '.dic'
    tmto_dic = load_var_from_file(file_name)

    Xj = R(ct)
    current_j = t
    for idx in range(0,t):
        Xj_int = list2int(Xj)
        
        if Xj_int in tmto_dic: # Xj가 EP에 있는가?
            SP = int2list(tmto_dic[Xj_int]) # dic = { EP:SP }
            key_guess = chain_EP(SP, P0, current_j - 1)
            key_candid_list.append(key_guess)
        
        new_ct = TC1.TC1_Enc(P0,Xj)
        Xj = R(new_ct)
        current_j = current_j - 1

    return key_candid_list


#================

ct1 = [224, 255, 196, 177] # (random.seed(2024))
key_pool = []
print("TMTO Attack", end='')
for ell in range(0, num_of_tables):
    key_list = one_tmto_table_search(ct1, P0, m, t, ell)
    key_pool += key_list
    print('.', end='')
    
print('\n Attack complete!\n')
print('key_pool =', key_pool)

# 다른 (평문, 암호문)을 이용하여, 후보키 중 최종 암호키를 선택함
pt2 = [5,6,7,8]
ct2 = [71, 69, 245, 137] # (random.seed(2024))
final_key = []

for key in key_pool:
    ct_result = TC1.TC1_Enc(pt2, key)
    if ct_result == ct2:
        final_key.append(key)

print('Final key =', final_key)   





