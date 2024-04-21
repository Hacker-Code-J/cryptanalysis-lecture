#----------------------------------
# TMTO Attack for TC1
# - n: 32-bit, k: 24-bit
# - Parameter: m=t=l=2^8 (mtl = 2^24)
# -- m: number of starting points
# -- l: number of tables
# -- t: length of chain
# - Memory = m*l = 2^16
# - Time   = t*l = 2^16
#----------------------------------

import sys
import TC1Lib as TC1
import pickle # store variable
import random # generate random number
import copy   # deep copy 

#--- int(4bytes) to list 
#--- 0x12345678 -> [ 0x12, 0x34, 0x56, 0x78 ]
def int2list(n):
   out_list = []
   out_list.append( (n >> 24) & 0xff )
   out_list.append( (n >> 16) & 0xff )
   out_list.append( (n >>  8) & 0xff )
   out_list.append( (n      ) & 0xff )
   return out_list

#--- list to int
#--- [ 0x12, 0x34, 0x56, 0x78 ] -> 0x12345678
def list2int(l):
   n = 0
   num_byte = len(l)
   for i in range(len(l)):
      n += l[i] << 8*(num_byte - i -1)
   return n

#--- Save Variable to File
def save_var_to_file(var, filename):
   f = open(filename, 'w+b')
   pickle.dump(var, f)
   f.close()

#--- Load Variable from File
def load_var_from_file(filename):
   f = open(filename, 'rb')
   var = pickle.load(f)
   f.close()
   return var

#============================================================
#  TMTO Attack
#============================================================

# 32-bit Enc/Dec : PT = [*,*,*,*] --> CT = [*,*,*,*]
# 24-bit Key     : key = [0,*,*,*]
key_bit = 24

#---------------------------------
# TMTO Table (Dictionary): { (SP:EP) }
#   #SP = #EP = 2^8,   #chains: m = 2^8, #tables: l = 2^8
#---------------------------------

#---------------------------------
# P0 : Chosen Plaintext
# X_{j+1} = E(P0, X_{j}) 		# if k = n
# X_{j+1} = R( E(P0, X_{j}) ) 	   # R: 32-bit -> 24-bit
# SP = X0 -> X1 -> X2 -> ... -> Xt = EP  # Encryption Key Chain
#---------------------------------

#-- Reduction Function
#-- R: 32-bit [*,*,*,*] -> 24-bit [0,*,*,*]
def R(ct):
   next_key = copy.deepcopy(ct)
   next_key[0] = 0
   return next_key

#-- Create Encryption Key Chain
#-- SP : random key (24-bit)
#-- P0 : chosen plaintext (fixed)
#-- t  : length of chain
def chain_EP(SP, P0, t):
   Xj = SP
   for j in range(0,t):
      ct = TC1.TC1_Enc(P0, Xj)
      Xj = R(ct)   # next Xj (32-bit -> 24-bit)
   return Xj

#--- Debugging Chain
def chain_EP_debug_print(SP, P0, t):
   Xj = SP
   print('SP =', SP)
   for j in range(0,t):
      ct = TC1.TC1_Enc(P0, Xj)
      Xj = R(ct)   # next Xj 
      print(' -> ', ct, ' -> ', Xj)
   return Xj

#--- Debugging Chain
#--- Xj[0,*,*,*] --> ct[*,*,*,*] --> R(ct)[0,*,*,*]
def chain_EP_debug_file(SP, P0, t, chain_num, table_num):
   file_name = f'debug/TMTO-chain-{table_num}-{chain_num}.txt'
   # file_name = 'debug/TMTO-chain-' + str(table_num) + '-' + str(chain_num) + '.txt'
   f = open(file_name, 'w+')
   Xj = SP
   f.write('SP = [0, %d, %d, %d] \n' %(Xj[1], Xj[2], Xj[3]))

   for j in range(0,t):
      ct = TC1.TC1_Enc(P0, Xj)
      Xj = R(ct)
      f.write(' --> [%d, %d, %d, %d] ' %(ct[0], ct[1], ct[2], ct[3]))
      f.write(' --> [%d, %d, %d, %d] \n' %(Xj[0], Xj[1], Xj[2], Xj[3]))
   f.close()

   return Xj

# Fixed Plaintext
P0 = [2,2,5,0]
# Setup Parameter
m = 256             # m: number of chain
t = 256             # t: length of chain
num_of_tables = 256

#=====================
# (Step 2) Attack
#=====================

''' 
PTCT for TMTO attack
pt1 = [2, 2, 5, 0]
ct1 = [167, 210, 209, 11]
pt2 = [3, 19, 37, 57]
ct2 = [131, 136, 209, 69]
key = [0, 177, 27, 241]
'''

#--------------
# Key Search for one Table
def one_tmto_table_search(ct, P0, m, t, ell):
   key_candid_list = []
   file_name = f'tmto_table/TMTO-{ell}.dic'
   #file_name = 'tmto_table/TMTO-' + str(ell) + '.dic'
   tmto_dic = load_var_from_file(file_name)

   Xj = R(ct)
   current_j = t
   for idx in range(0,t):
      Xj_int = list2int(Xj)

      if Xj_int in tmto_dic: # Is Xj in EP?
         SP = int2list(tmto_dic[Xj_int]) # dic = { EP:SP }
         key_guess = chain_EP(SP, P0, current_j - 1)
         key_candid_list.append(key_guess)

      new_ct = TC1.TC1_Enc(P0,Xj)
      Xj = R(new_ct)
      current_j = current_j - 1

   return key_candid_list


#================

ct1 = [167, 210, 209, 11] # (random.seed(2024))
key_pool = []
print("TMTO Attack", end='')
for ell in range(0, num_of_tables):
   key_list = one_tmto_table_search(ct1, P0, m, t, ell)
   key_pool += key_list
   print('.', end='', flush=True)

print('\n Attack complete!\n')
print('key_pool =\n', key_pool, '\n')

# Choose final key through anther PT-CT pair
pt2 = [3, 19, 37, 57]
ct2 = [131, 136, 209, 69] # (random.seed(2024))
final_key = []

for key in key_pool:
    ct_result = TC1.TC1_Enc(pt2, key)
    if ct_result == ct2:
        final_key.append(key)

print(f"Final key ({len(final_key)}) ={final_key}")   