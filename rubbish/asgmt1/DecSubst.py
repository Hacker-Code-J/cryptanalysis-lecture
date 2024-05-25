import SubstCipherLib
import os, sys

key = 'YTCUOKBDIGVWQXLFNSHJMZREAP'

in_file = 'CT2.txt'

if not os.path.exists(in_file):
    print("Working directory:", os.getcwd())
    print('File %s does not exist.' %(in_file))
    sys.exit() 
    

InFileObj = open(in_file)    
CT = InFileObj.read()
InFileObj.close()

print('input file (%s) : ' %(in_file), end = '')
print(CT[:10],"...", CT[-10:])

recPT = SubstCipherLib.subst_decrypt(key, CT)


out_file = 'PT2.txt'
   
if os.path.exists(out_file):
    print('This will overwrite the file %s. (C)ontinue or (Q)uit' % (out_file))
    response = input('> ')
    if not response.lower().startswith('c'): 
        sys.exit()

OutFileObj = open(out_file, 'w')
OutFileObj.write(recPT)
OutFileObj.close()

print('Output file (%s) : ' %(out_file), end='')
print(recPT[:10], '...', recPT[-10:])

