#-------------------------
# TC1 - Create PT and CT
#-------------------------
import TC1Lib as TC1
    
pt1 = [2, 2, 5, 0]  # P0 used in TMTO
key = [0, 218, 190, 65]  # TMTO-chain-89-237
ct1 = TC1.TC1_Enc(pt1, key)

pt2 = [3, 19, 37, 57]
ct2 = TC1.TC1_Enc(pt2, key)

print('PTCT for TMTO attack')

print('pt1 =', pt1)
print('ct1 =', ct1)

print('pt2 =', pt2)
print('ct2 =', ct2)

print('key =', key)

'''
PTCT for TMTO attack
pt1 = [2, 2, 5, 0]
ct1 = [135, 9, 44, 221]
pt2 = [3, 19, 37, 57]
ct2 = [150, 236, 50, 83]
key = [0, 218, 190, 65]
'''