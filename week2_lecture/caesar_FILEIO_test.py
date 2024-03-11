import os, sys
import CaesarLib as Caesar

in_file = 'PT1.txt'
if not os.path.exists(in_file):
    print("Working directory: ", os.getcwd())
    print('File %s does not exist.' %(in_file))
    sys.exit()

InFileObj = open(in_file)
PT = InFileObj.read()
InFileObj.close()
# print("Some-Txt:")
# print(PT[:5], " ... ", PT[-5:])
# print("Full-Txt:")
# print(PT)

key = 3
CT = Caesar.caesar_encrypt(key, PT)
print(CT)

out_file = 'CT1.txt'
OutFileObj = open(out_file, "w")
OutFileObj.write(CT)
OutFileObj.close()

print()
DT = Caesar.caesar_decrypt(key, CT)
print(DT)