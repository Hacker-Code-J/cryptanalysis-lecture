import os, sys
import CaesarLib as Caesar

in_file = 'CT0.txt'
if not os.path.exists(in_file):
    print("Working directory: ", os.getcwd())
    print('File %s does not exist.' %(in_file))
    sys.exit()

InFileObj = open(in_file)
CT = InFileObj.read()
InFileObj.close()

for key in range(0, 26):
    DT = Caesar.caesar_decrypt(key, CT)
    print("Current Key: ", key, " | ", DT[:30], "...", DT[-30:])