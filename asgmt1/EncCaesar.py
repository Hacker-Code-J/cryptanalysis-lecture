import os, sys
import CaesarLib as Caesar

in_file = 'PT0.txt'
if not os.path.exists(in_file):
    print("Working directory: ", os.getcwd())
    print('File %s does not exist.' %(in_file))
    sys.exit()

InFileObj = open(in_file)
PT = InFileObj.read()
InFileObj.close()

key = 10
CT = Caesar.caesar_encrypt(key, PT)

out_file = 'CT0.txt'
OutFileObj = open(out_file, "w")
OutFileObj.write(CT)
OutFileObj.close()