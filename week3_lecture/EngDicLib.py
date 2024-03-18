# English Dictionary Library

UpAlphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letters_and_space = UpAlphabet + UpAlphabet.lower() + ' \t\n'

def loadDic():
    dic_file = open('EngDic.txt')
    EnglishDic = {}
    for word in dic_file.read().split('\n'):
        EnglishDic[word] = len(word)
    dic_file.close()
    return EnglishDic

EngDic = loadDic() # Load Global Variable EngDic to English Dictionary

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
    return float(count_words) / len(possible_words)

def isEnglish(message, wordPercentage=20, letterPercentage=80):
    numLetters = len(removeNonLetters(message))
    messageLettersPercentage = (float(numLetters) / len(message)) * 100
    lettersMatch = messageLettersPercentage >= letterPercentage
    
    wordMatch = (percentEnglishWords(message) * 100) >= wordPercentage
    
    return lettersMatch and wordMatch

def main():
    msg1 = 'This is a sample text in 2024.'
    print('msg1 =', msg1)
    print(isEnglish(msg1))

if __name__ == '__main__':
    main()


# # === [1] Making Dictionary
# # items: (key, value)

# myDic = { 'DES':64, 'AES':128, 'ARIA':128 }
# print(myDic)
# print(myDic['DES'])

# myDic['LEA'] = 128
# print(myDic)
# print(len(myDic)) # number of items in Dictionary

# # === [2] Making English Dictionary
# def loadDic():
#     dic_file = open('EngDic.txt')
#     EnglishDic = {}
#     for word in dic_file.read().split('\n'):
#         EnglishDic[word] = len(word)
#     dic_file.close()
#     return EnglishDic

# EngDic = loadDic()
# print(len(EngDic))

# # === [3] Remove Special Characters
# UpAlphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# # LowAlphabet = 'abcdefghijklmnopqrstuvwxyz'
# letters_and_space = UpAlphabet + UpAlphabet.lower() + ' \t\n'

# def removeNonLetters(message):
#     letters_only = []
#     for ch in message:
#         if ch in letters_and_space:
#             letters_only.append(ch)
#     return ''.join(letters_only)

# # === [3]
# def percentEnglishWords(message):
#     message = message.lower()
#     message = removeNonLetters(message)
#     possible_words = message.split()
    
#     if possible_words == []:
#         return 0.0
#     count_words = 0
#     for word in possible_words:
#         if word in EngDic:
#             count_words += 1
#     return float(count_words) / len(possible_words)

# def isEnglish(message, wordPercentage=20, letterPercentage=80):
#     numLetters = len(removeNonLetters(message))
#     messageLettersPercentage = (float(numLetters) / len(message)) * 100
#     lettersMatch = messageLettersPercentage >= letterPercentage
    
#     wordMatch = (percentEnglishWords(message) * 100) >= wordPercentage
    
#     return lettersMatch and wordMatch

# msg1 = 'This is a sample text in 2024.'
# print('msg1 =', msg1)
# print(isEnglish(msg1))