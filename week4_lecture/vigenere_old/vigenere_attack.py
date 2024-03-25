import VigenereLib, week4_lecture.vigenere_old.CaesarLib as CaesarLib
import os, sys
import EngDicLib

in_file = 'CT3.txt'
InFileObj = open(in_file)
CT = InFileObj.read()
InFileObj.close()
MAX_KEY_LENGTH = 8
keylen_candidate = 0
max_ic = 0.0
for key_len in range(1,MAX_KEY_LENGTH+1):
    sub_msg = ''
    idx = 0
    while idx < len(CT):
        sub_msg += CT[idx]
        idx += key_len
    sub_ic = EngDicLib.IC(sub_msg) 
    if max_ic < sub_ic:
        max_ic = sub_ic
        keylen_candidate = key_len
    # print('key_len =', key_len, ':', end='')
    # print('sub_msg', sub_msg[:10],"...", '( length =', len(sub_msg), ')\t', end='')
    # print('IC(sub_msg)= %6.4f' %(sub_ic))
    
key_list = [0]*keylen_candidate  

for key_pos in range(1,keylen_candidate):
    key_ch_candidate = 0
    max_ic = 0.0
    for key_ch in range(0,26):
        sub_msg = ''
        idx = 0
        while idx < len(CT):
            sub_msg += CT[idx]
            if (idx+1) < len(CT):
                sub_msg += CaesarLib.caesar_decrypt(key_ch, CT[idx+1])
            idx += keylen_candidate
            
        sub_ic = EngDicLib.IC(sub_msg)
        if max_ic < sub_ic:
            max_ic = sub_ic
            key_ch_candidate = key_ch
            
        print('key_ch =', key_ch, ':', end='')
        print('sub_msg', sub_msg[:10],"...", '( length =', len(sub_msg), ')\t', end='')
        print('IC(sub_msg)= %6.4f' %(sub_ic))
print('key[%d] : key_ch_candidate = %d' %(key_pos, key_ch_candidate))

key_0_candidate = -1

for key_ch in range(0,26):
    dec_msg = ''
    key_pos= 0
    for ch in CT:
        key_now = (key_ch + key_list[key_pos]) % 26
        dec_msg += CaesarLib.caesar_decrypt(key_now, ch)        
        key_pos = (key_pos + 1) % keylen_candidate

    eng_percent = EngDicLib.percentEnglishWords(dec_msg)
       
    print('key_ch =', key_ch, ':', end='')
    print('dec_msg', dec_msg[:10],"...", '( length =', len(dec_msg), ')\t', end='')
    print('Eng(dec_msg)= %5.2f %%' %(eng_percent*100))

    if EngDicLib.isEnglish(dec_msg):
        key_0_candidate, rightPT = key_ch, dec_msg

if key_0_candidate >= 0:
    rightkey = ''
    for idx in key_list:
        rightkey += VigenereLib.Alphabet[(key_0_candidate+idx)%26]
        
    print('right key =', rightkey)
    print('PT = ', rightPT[:20], '...', rightPT[-10:])
    out_file = 'decodedPT3.txt'
    OutFileObj = open(out_file, 'w')
    OutFileObj.write(rightPT)
    OutFileObj.close()
'''
'''