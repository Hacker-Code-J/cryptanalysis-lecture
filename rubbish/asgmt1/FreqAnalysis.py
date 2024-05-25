import SubstCipherLib as substcipher

ETAOIN = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def getLetterCount(message):
    letterCount = {'A':0, 'B':0, 'C':0, 'D':0, 'E':0, 'F':0, 'G':0, 'H':0,
                   'I':0, 'J':0, 'K':0, 'L':0, 'M':0, 'N':0, 'O':0, 'P':0,
                   'Q':0, 'R':0, 'S':0, 'T':0, 'U':0, 'V':0, 'W':0, 'X':0,
                   'Y':0, 'Z':0}    
    for ch in message.upper():
        if ch in LETTERS:
            letterCount[ ch ] += 1
    return letterCount

def getItemZero(items):  
    return items[0]

def getFreqOrder(message):
    letter2freq = getLetterCount(message) 
    freq2letter = {}  
    for ch in LETTERS:
        if letter2freq[ch] not in freq2letter: 
            freq2letter[letter2freq[ch]] = [ ch ]  
        else:
            freq2letter[letter2freq[ch]].append(ch)  
    
    for freq in freq2letter: 
        freq2letter[freq].sort(key = ETAOIN.find, reverse = False)  
        freq2letter[freq] = ''.join(freq2letter[freq])  

    freqPairs = list(freq2letter.items())   
    freqPairs.sort(key = getItemZero, reverse = True)  
    freqOrder = []
    for freq_pair in freqPairs: 
        freqOrder.append(freq_pair[1]) 
        
    return ''.join(freqOrder)

def Freq2Key(freq_order):
    temp_dict = {}
    i = 0
    for ch in freq_order:
        temp_dict[ETAOIN[i]] = ch  
        i += 1
    temp_list = list(temp_dict.items()) 
    temp_list.sort(key = getItemZero, reverse = False) 
    temp_key_list = []
    for item in temp_list: 
        temp_key_list.append(item[1]) 
        
    return ''.join(temp_key_list)
        
in_file = "CT2.txt"       
msg = substcipher.ReadFile(in_file)
AlphaCount = getLetterCount(msg)
print(AlphaCount)
freq_order = getFreqOrder(msg)
print("freq_order = ", freq_order)
key_guess = Freq2Key(freq_order)
print("key_guess = ", key_guess)

out_file = "freq_DT2.txt"
freq_decrypt = substcipher.subst_decrypt(key_guess, msg)
substcipher.WriteFile(out_file, freq_decrypt)