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

#-- Find week round function s.t.
#-- F(A, rk) = B for given A, B
def Extract_RK(A, B):
    in_state = A
    state1 = TC1.LM(B)
    state2 = TC1.ISB(state1)
    rk = TC1.AR(state2, in_state)
    return rk

#-- Check Slid Pair (P1, C2), (P2, C2)
#-- F(P1, K) = P2 and
#-- F(C1, K) = C2
def IsSlidPair(P1, C1, P2, C2):
    rk = [0, 0, 0, 0]
    flag = False
    
    rk = Extract_RK(P1, P2)
    rnd_out = TC1.Enc_Round(C1, rk)
    if rnd_out == C2:
        flag = True
    else:
        flag = False
    
    return (flag, rk)

#-- Create Known Plaintext-Ciphertext (Pi, Ci)
def Generate_Known_pt_ct(num_pair, key):
    list_pool = []
    print("Generating PT-CT pairs", end='')
    for i in range(0, num_pair):
        PT = [random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(0,255)]
        CT = TC1.TC1_Enc(PT,key)
        item = copy.deepcopy([PT,CT])
        list_pool.append(item)
        if (i % (1 << 18)) == 0:
            print('.', end='', flush=True)
    print('   Done! \n')
    return list_pool

# key = [1, 2, 3 ,4]
# pool = Generate_Known_pt_ct(1<<16, key)
# save_var_to_file(pool, 'known_ptct1.var')

#=====================
# Slide Attack
#=====================

def Slide_Attack(pool):
    key = [0,0,0,0]
    
    cnt = 0
    total = len(pool)**2
    print("Start Slide Attack", end='\n')
    
    key_list = []
    flag_found = False
    
    # Initial print of the progress bar; 50 units wide
    sys.stdout.write("[{}] 0%\r".format(" " * 50))
    sys.stdout.flush()
    
    for pair1 in pool:
        P1, C1 = pair1
        # P1 = pair1[0]
        # C1 = pair1[1]
        for pair2 in pool:
            P2, C2 = pair2
            # P2 = pair2[0]
            # C2 = pair2[1]
            flag_found, key = IsSlidPair(P1, C1, P2, C2)
            if flag_found:
                print('\n key =', key)
                key_list.append(key)
            cnt += 1
            progress = 100 * cnt / total
            filled_length = int(50 * cnt // total)
            sys.stdout.write("[{}{}] {:.0f}%\r".format("#" * filled_length, " " * (50 - filled_length), progress))
            sys.stdout.flush()

    sys.stdout.write("[{}] 100%\n".format("#" * 50))  # Complete the progress bar
    print('Done!\n')
    return key_list

pool = load_var_from_file('known_ptct1.var')
key_list = Slide_Attack(pool)
print(key_list)