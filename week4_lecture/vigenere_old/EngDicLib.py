
UpAlphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letters_and_space = UpAlphabet + UpAlphabet.lower() + ' \t\n'

def loadDic():
    dic_file = open('EngDic.txt')
    EnglishDic = {} 
    for word in dic_file.read().split('\n'):
        EnglishDic[word] = len(word)
    dic_file.close()
    return EnglishDic

EngDic = loadDic()

#===============================================
#-- IC: Index of Coincidence
#===============================================
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
#===============================================

def removeNonLetters(message):
    letters_only = []
    for ch in message:
        if ch in letters_and_space:
            letters_only.append(ch)
    return ''.join(letters_only)

def percentEnglishWords(message):
    message = message.lower()
    message = removeNonLetters(message)
    possible_words = message.split()
    
    if possible_words == []:
        return 0.0
    count_words = 0 
    for word in possible_words:
        if word in EngDic:
            count_words += 1
    return float(count_words)/len(possible_words)
    
def isEnglish(message, wordPercentage=20, letterPercentage=80):
    numLetters = len(removeNonLetters(message))
    messageLettersPercentage = float(numLetters)/len(message)*100
    lettersMatch = messageLettersPercentage >= letterPercentage
    
    wordsMatch = percentEnglishWords(message)*100 >= wordPercentage
    
    return lettersMatch and wordsMatch

def main():
    msg1 = 'This is a sample text in 2024.'
    print('msg1 =', msg1)
    print(isEnglish(msg1))

if __name__ == '__main__':
    main()
