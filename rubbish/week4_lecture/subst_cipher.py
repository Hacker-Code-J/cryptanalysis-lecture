Alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
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

message = "Cryptography is the practice and study of techniques for secure"
# communication in the presence of third parties (called adversaries) \
# More generally, it is about constructing and analyzing protocols that \
# overcome the influence of adversaries and which are related to
# various aspects in information security such as data confidentiality,
# data integrity, and authentication."

my_key = 'VWXABCDEIJKFGHLMQRSNOPTUYZ'
ciphertext = subst_encrypt(my_key, message)
print(ciphertext)