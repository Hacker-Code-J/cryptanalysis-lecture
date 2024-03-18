import os, sys
import CaesarLib as Caesar
import EngDicLib

in_file = 'CT1.txt'
if not os.path.exists(in_file):
    print("Working directory: ", os.getcwd())
    print('File %s does not exist.' %(in_file))
    sys.exit()

InFileObj = open(in_file)
CT = InFileObj.read()
InFileObj.close()

# Exhaustive Key Search / Brute-Force Attack
for key in range(0, 26):
    DT = Caesar.caesar_decrypt(key, CT)
    print("Current Key: ", key, " | ", DT[:20], "...", DT[-10:])
    if EngDicLib.isEnglish(DT):
        rightkey, rightPT = key, DT
        
if rightkey >= 0:
    print('right key =', rightkey)
    print('PT =', rightPT[:20], '...', rightPT[-20:])
    out_file = 'DT_by_DIC.txt'
    OutFIleObj = open(out_file, 'w')
    OutFIleObj.write(rightPT)
    OutFIleObj.close()