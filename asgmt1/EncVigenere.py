import os, sys
import VigenereLib as Vigenere

in_file = 'PT1.txt'
if not os.path.exists(in_file):
    print("Working directory: ", os.getcwd())
    print('File %s does not exist.' %(in_file))
    sys.exit()

InFileObj = open(in_file)
PT = InFileObj.read()
InFileObj.close()

key = 'CRYPTO'
CT = Vigenere.vigenere_encrypt(key, PT)

out_file = 'CT1.txt'
OutFileObj = open(out_file, "w")
OutFileObj.write(CT)
OutFileObj.close()