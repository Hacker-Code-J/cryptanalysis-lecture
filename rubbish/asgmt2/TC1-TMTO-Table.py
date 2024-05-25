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

#--------------------------------
# Create one TMTO Table (Number=ell)
# Input:
#      P0: chosen plaintext (fixed)
#       m: number of SPs (row)        m=2^8: SP1 ~ SP2^8
#       t: length of chain (column)   j=0, ... , j=t
#     ell: table number               ell = 0 ~ 255
# Output: 
#    dic : { (Key=EP, Value=SP) }    
#    path: ./tmto_table/TMTO-ell.dic
#--------------------------------

def make_one_tmto_table(P0, m, t, ell):
   tmto_dic = {}  # (Key, Value) = (EP,SP)
   for i in range(0,m):
      # random starting point
      SP = [0, random.randint(0,255), random.randint(0,255), random.randint(0,255) ]
      EP = chain_EP_debug_file(SP, P0, t, i, ell)
      #EP = chain_EP(SP, P0, t)  

      # { (Key=EP, Value=SP) }
      SP_int = list2int(SP)
      EP_int = list2int(EP)
      # EP is Key
      tmto_dic[EP_int] = SP_int

   # files: TMTO-0, TMTO-1, ... , TMTO-255
   # file_name = 'tmto_table/TMTO-' + str(ell) + '.dic'
   file_name = f'tmto_table/TMTO-{ell}.dic'
   save_var_to_file(tmto_dic, file_name)

#---------------------
# Create total TMTO
# Input:
#   P0: Fixed Plaintext 
#   m: no. rows (number of chain)
#   t: no. cols (length of chain)
#   num_of_tables: 2^8 (=256)
#---------------------
   
# def make_all_tmto_tables(P0, m, t, num_of_tables):
#    print('Making TMTO tables', end='')
#    for ell in range(0, num_of_tables):
#       make_one_tmto_table(P0, m, t, ell)
#       print('.', end='', flush=True)

#    print('\n All TMTO tables are created.')
   
# def make_all_tmto_tables(P0, m, t, num_of_tables):
#     sys.stdout.write('Making TMTO tables')
#     sys.stdout.flush()
#     for ell in range(num_of_tables):
#         make_one_tmto_table(P0, m, t, ell)
#         sys.stdout.write('.')  # Blue dots
#         sys.stdout.flush()
    
#     sys.stdout.write('All TMTO tables are created.')

def make_all_tmto_tables(P0, m, t, num_of_tables):
    sys.stdout.write('\033[4;5;95mTMTO Table Generation...\033[0m\n')
    sys.stdout.flush()
    
    for ell in range(num_of_tables):
        sys.stdout.write(f'\033[96mCreating table {ell+1}/{num_of_tables}:\033[0m ')
        sys.stdout.flush()
        make_one_tmto_table(P0, m, t, ell)
        
        percent_complete = int((ell + 1) / num_of_tables * 100)
        bar_length = 30
        filled_length = int(percent_complete / 100 * bar_length)
        bar = '\033[92m' + '#' * filled_length + '\033[90m' + '-' * (bar_length - filled_length) + '\033[0m'
        sys.stdout.write(f'[{bar}] {percent_complete}%\r')
        sys.stdout.flush()
    
    # Clear line before final message
    sys.stdout.write('\033[K')
    
    # End message
    sys.stdout.write('\033[1;92mAll TMTO tables are created successfully!\033[0m\n')


#=====================
# Test Run

#random.seed(1234)  #fixed seed --> identical result
random.seed(2024)  #fixed seed --> identical result

# Fixed Plaintext
P0 = [2,2,5,0]
# Setup Parameter
m = 256             # m: number of chain
t = 256             # t: length of chain
num_of_tables = 256

#=====================
# (Step 1) Create TMTO Table (Pre-computation)
# TMTO-0, TMTO-1, ...
#=====================
make_all_tmto_tables(P0, m, t, num_of_tables)
