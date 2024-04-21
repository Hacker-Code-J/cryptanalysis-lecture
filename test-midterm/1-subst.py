import random

Alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
#-- Subst-Encryption
def subst_encrypt(key, msg):
	result = ''
	InSet = Alphabet
	OutSet = key
	for ch in msg:
		if ch.upper() in InSet:
			idx = InSet.find(ch.upper())
			if ch.isupper():
				result += OutSet[idx].upper()
			else:
				result += OutSet[idx].lower()
		else:
			result += ch
	return result
#-- Subst-Decryption
def subst_decrypt(key, msg):
    result = ''
    InSet = Alphabet
    OutSet = key	
    for ch in msg:
        if ch.upper() in InSet:
            idx = InSet.find(ch.upper())
            if ch.isupper():
                result += OutSet[idx].upper()
            else:
                result += OutSet[idx].lower()
        else:
            result += ch
    return result

#-- (a)
key1 = 'ABFWQICPLZYUDNHMGKEXVTSJRO'
pt1 = 'banana'
ct1 = subst_encrypt(key1, pt1)
print('Eng =', Alphabet)
print('key1 =', key1)
print('pt1 =', pt1)
print('ct1 =', ct1)

#-- (b)
def valid_key1(key):
    list_key = list(key)
    list_key.sort()
    key_alphabet = ''.join(list_key).upper()
    return key_alphabet == Alphabet

def valid_key2(key):
    for ch in key:
        if not ch.isalpha():
            return False
    if len(set(key)) != 26:
        return False
    return True

key_b1 = 'AAADEFGHIJKLMNOPQRSTUVWXYZ'
key_b2 = 'ABCDEFGHIJKLMNOPQRSTUVWxyz'
key_b3 = 'abcDEFGHIJKLMNOPQRSTUVWXYZ'

print(f"b1 | {valid_key1(key_b1)}:{valid_key2(key_b1)}")
print(f"b2 | {valid_key1(key_b2)}:{valid_key2(key_b2)}")
print(f"b3 | {valid_key1(key_b3)}:{valid_key2(key_b3)}")

# identifiers = ['b1', 'b2', 'b3']
# max_id_length = max(len(id) for id in identifiers)

# print(f"{'b1'.ljust(max_id_length)} | {str(valid_key1(key_b1)).ljust(5)}:{str(valid_key2(key_b1)).ljust(5)}")
# print(f"{'b2'.ljust(max_id_length)} | {str(valid_key1(key_b2)).ljust(5)}:{str(valid_key2(key_b2)).ljust(5)}")
# print(f"{'b3'.ljust(max_id_length)} | {str(valid_key1(key_b3)).ljust(5)}:{str(valid_key2(key_b3)).ljust(5)}")

#-- (c)
print(subst_encrypt(key1, 'A'))

# def gen_random_key(seed):
#     random.seed(seed)
#     alpha_list = list(Alphabet)
#     random.shuffle(alpha_list)
#     shuffled_key = ''.join(alpha_list)
#     return shuffled_key

def gen_random_key(seed):
    random.seed(seed)
    alpha_list = list(Alphabet)
    valid_key = False
    while not valid_key:
        random.shuffle(alpha_list)
        shuffled_key = ''.join(alpha_list)
        valid_key = True
        for i in range(len(Alphabet)):
            # if A -> A or ... or Z -> Z
            if Alphabet[i] == shuffled_key[i]:
                valid_key = False
                break # for-break
        return shuffled_key

def gen_random_key2(seed=None):
    random.seed(seed)
    alpha_list = list(Alphabet)
    
    # Create a derangement using Sattolo's algorithm
    def sattolo_cycle(items):
        i = len(items)
        while i > 1:
            i -= 1
            j = random.randint(0, i - 1)
            items[j], items[i] = items[i], items[j]
        return items
    
    # Generate a valid derangement
    shuffled_key = sattolo_cycle(alpha_list)
    return ''.join(shuffled_key)

for _ in range(10):
    alpha_list = list(Alphabet)
    for _ in range(255):
        random.shuffle(alpha_list)
    seed = ''.join(alpha_list)
    print(gen_random_key(seed))

print("==========================")
    
for _ in range(10):
    alpha_list = list(Alphabet)
    for _ in range(255):
        random.shuffle(alpha_list)
    seed = ''.join(alpha_list)
    print(gen_random_key2(seed))