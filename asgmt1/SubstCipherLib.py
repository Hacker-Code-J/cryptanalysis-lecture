import os, sys
import random 

Alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def subst_encrypt(key, msg):
    result = ''
    InSet = Alphabet
    OutSet = key
    
    for ch in msg:
        if ch.upper() in InSet:
            idx = InSet.find(ch.upper())
            if ch.isupper():
                result += OutSet[idx].upper()
            else:
                result += OutSet[idx].lower()
        else:
            result += ch

    return result

def subst_decrypt(key, msg):
    result = ''
    InSet = key
    OutSet = Alphabet
    
    for ch in msg:
        if ch.upper() in InSet:
            idx = InSet.find(ch.upper())
            if ch.isupper():
                result += OutSet[idx].upper()
            else:
                result += OutSet[idx].lower()
        else:
            result += ch

    return result

def ReadFile(in_file):
    
    if not os.path.exists(in_file):
        print('File %s does not exist.', in_file)
        sys.exit()
    
    InFileObj = open(in_file)    
    file_content = InFileObj.read()
    InFileObj.close()

    return file_content

def WriteFile(out_file, message):
    if os.path.exists(out_file):
        print('Overwrite the file %s ? (Y)es or (N)o' % (out_file))
        response = input('> ') 
        if not response.lower().startswith('y'): 
            sys.exit()
    
    OutFileObj = open(out_file, 'w')
    OutFileObj.write(message)
    OutFileObj.close()

    return 0

def SubstKeyGen():
    Alpha_list = list(Alphabet)
    random.shuffle(Alpha_list)
    new_key = ''.join(Alpha_list)
    
    return new_key







