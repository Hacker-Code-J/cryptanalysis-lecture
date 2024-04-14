#------------------------------------------------
# 암호분석 : Double Encryption에 대한 MITM Attack
#------------------------------------------------
'''
 Toy Cipher DTC1 에 대한 키 전수조사 공격
 - DTC1 알고리즘: TC1을 두번 사용하는 암호
   ct = DTC1_Enc( pt, [key1, key2])
      = TC1_Enc( TC1_Enc(pt, key1), key2)  
 - 암호키: 48비트 (MITM 공격용 축소 모델)
   key1 = [ 0, k11, k12, k13]
   key2 = [ 0, k21, k22, k23]
 공격조건(기지평문공격): 주어진 (평문, 암호문)에 대한 암호키를 찾는 문제

'''

import pickle
import DTC1Lib as DTC1

#======================================================
# 함수 라이브러 - int2list(), list2int()

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

#======================================================
'''
#==[0] 공격용 (평문, 암호문) 만들기 (2쌍 필요)
#- 암호키 (공격에서 찾아야하는 키)
key1 = [0, 20, 24, 4]
key2 = [0, 24, 4, 8]

# (평문1, 암호문1) = (pt1, ct1)
pt1 = [1, 2, 3, 4]
mid1 = DTC1.TC1_Enc(pt1, key1)
ct1 =  DTC1.TC1_Enc(mid1, key2)
ct1_chk = DTC1.DTC1_Enc(pt1, [key1, key2])

print('key1 =', key1)
print('key2=', key2)

print('pt1  =', pt1)
print('mid1 =', mid1)
print('ct1  =', ct1)
print('ct1_chk  =', ct1_chk)

# (평문2, 암호문2) = (pt2, ct2)
pt2 = [4, 3, 2, 1]
mid2 = DTC1.TC1_Enc(pt2, key1)
ct2 =  DTC1.TC1_Enc(mid2, key2)
ct2_chk = DTC1.DTC1_Enc(pt2, [key1, key2])

print('pt2  =', pt2)
print('mid2 =', mid2)
print('ct2  =', ct2)
print('ct2_chk  =', ct2_chk)

'''
'''
#======================================================
# 단계 [0]에서 생성한 (평문, 암호문) 쌍

#-- (예제1)
key1 = [0, 20, 24, 4]
key2 = [0, 1, 2, 3]

pt1  = [1, 2, 3, 4]
mid1 = [48, 241, 205, 237]
ct1  = [177, 134, 205, 67]
ct1_chk  = [177, 134, 205, 67]

pt2  = [4, 3, 2, 1]
mid2 = [233, 40, 204, 238]
ct2  = [52, 254, 174, 27]
ct2_chk  = [52, 254, 174, 27]

#---------------------------------
#-- (예제2)
key1 = [0, 20, 24, 4]
key2= [0, 24, 4, 8]

pt1  = [1, 2, 3, 4]
mid1 = [48, 241, 205, 237]
ct1  = [64, 226, 255, 35]
ct1_chk  = [64, 226, 255, 35]

pt2  = [4, 3, 2, 1]
mid2 = [233, 40, 204, 238]
ct2  = [149, 202, 209, 120]
ct2_chk  = [149, 202, 209, 120]
#======================================================
'''

#=======================================================
# 주어진 평문 pt1에 대하여, 
# 모든 key1 후보로 TC1_Enc() 암호화한 결과를 사전으로 만든다.
# mid1 <-- E(pt1, key1) <-- pt1(고정)
# 사전 dic = { (mid1, [key1 리스트]) }
#  예: dic[mid1] = [key1 리스트] = [k1, k2] 
def make_enc_dic(pt):
    dic = {}
    print('Making Encryption Dictionary', end='')
    N = 1<<24 # 24비트 키 N = 2^24
    for int_key in range(0,N):
        key = int2list(int_key)
        mid = DTC1.TC1_Enc(pt, key)
        int_mid = list2int(mid)        
        
        #[실습] -- 사전 dic에 (평문, 암호키) 넣기
        if int_mid in dic:
            dic[int_mid].append(int_key)
        else:
            dic[int_mid] = [int_key]
            
        if (int_key %(1<<18)) == 0:
            print('.', end='')
    print(' Done.')
    return dic
                
#=======================================================
# 주어진 키 key1 후보 리스트 중에서 올바른 키가 있는지 찾는다.
# key1 후보들 = [k1, k2, ...] 중에서
# pt2 를 암호화하여 ct2를 만든 것을 찾는다. (주어진 key2)
# ct2 <-- E(M, key2) <-- M <-- E(pt2, k1) <-- pt2
#
def verify_key_candidate_list(key1_list, key2, pt2, ct2):
    flag = False  # 후보 없음
    for key1 in key1_list:  # 리스트에 있는 key1의 후보 각각에 대하여
        key1_state = int2list(key1)
        
        #[실습] --  (pt2, ct2)를 만족하는 key1을 찾는다
        # -- 키를 찾았으면 출력하고, flag = True로 설정한다.
        # mid1 = TC1.TC1_Enc(pt2, key1_state)
        # ct_comp = TC1.TC1_Enc(mid1, key2)
        # if ct_comp == ct2:
        #    print("\n key1 =", key1_state, ' key2 =', key2)

        ct2_chk = DTC1.DTC1_Enc(pt2, [key1_state, key2])
        if ct2_chk == ct2:
            print("Key1 = ", key1_state, "Key2 = ", key2)
            flag = True

    return flag


#=======================================================
# 공격조건: (pt1, ct1), (pt2, ct2) 로부터 key1, key2 찾기
#=======================================================
'''
#-- (예제1)
pt1  = [1, 2, 3, 4]
ct1  = [177, 134, 205, 67]
pt2  = [4, 3, 2, 1]
ct2  = [52, 254, 174, 27]
'''
#-- (예제2)
pt1  = [1, 2, 3, 4]
ct1  = [64, 226, 255, 35]
pt2  = [4, 3, 2, 1]
ct2  = [149, 202, 209, 120]
#=======================================================

#==[1] MITM 공격용 사전 만들기
#mid_dic = make_enc_dic(pt1)
#-- 사전을 파일로 저장하기
#save_var_to_file(mid_dic, 'TC1_Enc_Dic.p')

#==[2] MITM 공격으로 키 찾기
#-- 사전 만들기를 이전에 수행했으면, 사전 가져오기부터 시작해도 됨
#-- 사전을 파일에서 가져오기
mid_dic = load_var_from_file('TC1_Enc_Dic.p')
# print('Dictionary loaded')

# Replace 'your_file.pkl' with your file's path
file_path = 'TC1_Enc_Dic.p'

try:
    with open(file_path, 'rb') as f:
        # Check if the file is not empty
        if f.peek(1):  # Peek returns bytes if there's data, else it's empty
            var = pickle.load(f)
        else:
            print("The file is empty.")
except EOFError:
    print("Encountered an EOFError. The file might be corrupt or not in the expected format.")
except Exception as e:
    print(f"An error occurred: {e}")

#=======================================================

N = 1<<24 # key2의 크기 2^24
for idx_key2 in range(0, N):
    key2 = int2list(idx_key2)
    
    #[실습] -- MITM 공격 완성하기
    mid1 = DTC1.TC1_Dec(ct1, key2)
    int_mid1 = list2int(mid1)

    if int_mid1 in mid_dic:
        key1_candicate_list = mid_dic[int_mid1]
        verify_key_candidate_list(key1_candicate_list, key2, pt2, ct2)

    if (idx_key2 % (1<<18)) == 0:
        print('.', end='')

print('\n Key search completed !!!')



