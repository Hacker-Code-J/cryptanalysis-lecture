# === [1] print formatting
# n = 100
# print('I trust you %s%%.' %(n))
# Old_name = 'Rijndael'
# New_name = 'AES'
# print('%s is the old name of %s algorithm in 1990.' %(Old_name, New_name))

# === [2] list
animals = [ 'cat', 'dog', 'snake']
print(animals)
print(animals[1])
print(animals[1:]) # sub-list

print(animals.index('dog'))
# print(animals.index('man')) # error
# print("abcde".find('x')) # Return -1

animals.append('man')
print(animals.index('man'))

animals += ['woman']
print(animals)