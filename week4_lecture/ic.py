UpAlphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def IC(msg):
    AlphaDic = {}
    for ch in UpAlphabet:
        AlphaDic[ch] = 0
    num_alpha = 0
    for ch in msg:
        if ch.upper() in UpAlphabet:
            AlphaDic[ch.upper()] += 1
            num_alpha += 1
    ic = 0
    for ch in UpAlphabet:
        ic += AlphaDic[ch]*(AlphaDic[ch]-1)
    ic /= num_alpha*(num_alpha-1)
    return ic


msg1 = "What is Caesar cipher? Is it secure?"
msg2 = "Zkdw lv Fdhvdu flskhu? Lv lw vhfxuh?"
print('msg1 = ', msg1[:30],'...')
print('msg2 = ', msg2[:30],'...')
print('Index of Coincidence, IC(msg1) = %6.4f' %(IC(msg1)))
print('Index of Coincidence, IC(msg2) = %6.4f' %(IC(msg2)))