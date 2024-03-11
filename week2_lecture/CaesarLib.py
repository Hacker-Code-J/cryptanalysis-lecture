UpAlphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LowAlphabet = 'abcdefghijklmnopqrstuvwxyz'

def caesar_encrypt(key, plain_msg):
    cipher_msg = ''
    for symbol in plain_msg :
        if symbol in UpAlphabet:
            symbol_idx = UpAlphabet.find(symbol)
            trans_idx = (symbol_idx + key) % len(UpAlphabet)
            cipher_msg = cipher_msg + UpAlphabet[trans_idx]
        elif symbol in LowAlphabet:
            symbol_idx = LowAlphabet.find(symbol)
            trans_idx = (symbol_idx + key) % len(LowAlphabet)
            cipher_msg = cipher_msg + LowAlphabet[trans_idx]
        else:
            cipher_msg = cipher_msg + symbol
    return cipher_msg

def caesar_decrypt(key, cipher_msg):
    recovered_msg = ''
    for symbol in cipher_msg :
        if symbol in UpAlphabet:
            symbol_idx = UpAlphabet.find(symbol)
            trans_idx = (symbol_idx - key) % len(UpAlphabet)
            recovered_msg = recovered_msg + UpAlphabet[trans_idx]
        elif symbol in LowAlphabet:
            symbol_idx = LowAlphabet.find(symbol)
            trans_idx = (symbol_idx - key) % len(LowAlphabet)
            recovered_msg = recovered_msg + LowAlphabet[trans_idx]
        else:
            recovered_msg = recovered_msg + symbol
    return recovered_msg

def test():
    plain_msg = 'This is a sample text 2024'
    key = 3 
    cipher_msg = caesar_encrypt(key, plain_msg)
    recovered_msg = caesar_decrypt(key, cipher_msg)

    print('PLAINTEXT = ', plain_msg)
    print('CIPHERTEXT = ', cipher_msg)
    print('PLAINTEXT = ', recovered_msg)
    
if __name__ == "__test()__":
    test()