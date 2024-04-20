#-------------------------
# 암호분석 : TC1 - 평문, 암호문 만들기
#-------------------------
'''
 Toy Cipher TC1의 평문, 암호문 만들기
 - 암호키: 24비트 key = [ 0, k1, k2, k3]
 - TMTO 테이블에 나타나는 암호키로 선택한다.
 
 - (pt1, ct1), (pt2, ct2) 두 쌍을 만든다.
   pt1은 TMTO 테이블 만들때 고정한 것
   pt2, ct2는 암호키가 맞는지 검증하기 위한 것

'''
#==================================================

#==================================================

import TC1Lib as TC1


#==================================================
    
pt1 = [1, 2, 3, 4]  # TMTO 테이블 만들 때 사용한 평문

key = [0, 23, 36, 6]  # TMTO 테이블에 나오는 암호키 (TMTO-chain-188-255)

ct1 = TC1.TC1_Enc(pt1, key)

pt2 = [5, 6, 7, 8]
ct2 = TC1.TC1_Enc(pt2, key)


print('PTCT for TMTO attack')

print('pt1 =', pt1)
print('ct1 =', ct1)

print('pt2 =', pt2)
print('ct2 =', ct2)

print('key =', key)

'''
실행 결과
PTCT for TMTO attack
pt1 = [1, 2, 3, 4]
ct1 = [224, 255, 196, 177]
pt2 = [5, 6, 7, 8]
ct2 = [71, 69, 245, 137]
key = [0, 23, 36, 6]
'''