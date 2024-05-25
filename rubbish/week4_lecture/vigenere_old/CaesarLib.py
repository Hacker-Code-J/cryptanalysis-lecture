# -*- coding: utf-8 -*-
"""
암호분석 2024 : Caesar 암호 라이브러리 (CaesarLib.py)
"""

UpAlphabet  = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LowAlphabet = "abcdefghijklmnopqrstuvwxyz"

#암호화 함수
def caesar_encrypt(key, plain_msg):
    cipher_msg = ""
    for ch in plain_msg:  #문자열에서 한글자씩 추출
        if ch in UpAlphabet:  # ch가 대문자이면,
            idx = ( UpAlphabet.find(ch) + key ) % len(UpAlphabet)
            cipher_msg = cipher_msg + UpAlphabet[idx]
        elif ch in LowAlphabet: # ch가 소문자이면,
            idx = ( LowAlphabet.find(ch) + key ) % len(LowAlphabet)
            cipher_msg = cipher_msg + LowAlphabet[idx]
        else:  #숫자, 특수문자 처리
            cipher_msg = cipher_msg + ch     
    return cipher_msg

#복호화 함수
def caesar_decrypt(key, cipher_msg):
    recovered_msg = ""
    for ch in cipher_msg:  #문자열에서 한글자씩 추출
        if ch in UpAlphabet:  # ch가 대문자이면,
            idx = ( UpAlphabet.find(ch) - key ) % len(UpAlphabet)
            recovered_msg = recovered_msg + UpAlphabet[idx]
        elif ch in LowAlphabet: # ch가 소문자이면,
            idx = ( LowAlphabet.find(ch) - key ) % len(LowAlphabet)
            recovered_msg = recovered_msg + LowAlphabet[idx]
        else:  #숫자, 특수문자 처리
            recovered_msg = recovered_msg + ch 
    return recovered_msg


#테스트 코드...
def main():
    PT_msg = "This is a sample text 2024." #평문 메시지
    key = 3 #암호키  (a->d, b->e, ..., z->c)  (find()함수 사용)
        
    print("PT=", PT_msg)    
    CT = caesar_encrypt(key, PT_msg)
    print("CT =", CT)
    PT_recovered = caesar_decrypt(key, CT)
    print("PT_recovered =", PT_recovered)


#==========
# 라이브러리를 단독으로 실행할때만 main()을 호출함
#==========
if __name__ == '__main__':
    main()







