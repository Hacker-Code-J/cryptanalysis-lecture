# Week5 - Lecture
'''
ch1 = 'A'
num1 = ord(ch1) # 65
hex1 = hex(num1) # '0x41'
bin1 = format(num1, 'b') # 0100 0001

list1 = [ch1, num1, hex1, bin1]
print("list1 = ", list1)

num2 = 66
ch2 = chr(num2)
hex2 = hex(num2)

list2 = []
list2.append(num2)
list2.append(ch2)
list2.append(hex2)
print("list2 = ", list2)

hex3 = '0x43'
num3 = int(hex3, 16)
list3 = [hex3, num3]
print("list3 = ", list3)

# String -> Bit-String
str1 = 'AB'
b1 = bytearray(str1, encoding = 'utf-8')
lb1 = [ format(i, '08b') for i in b1]
print(lb1)
bit1 = ''.join(lb1)
print('bit1 = ', bit1)

str2 = 'ab'
bit2 = ''.join(format(i, '08b') for i in bytearray(str1, encoding = 'utf-8'))
print("bit2 = ", bit2)
'''

# String -> Integer List
# ['A', 'B', 'C', 'D'] = [65, 66, 67, 68]

str4 = 'ABCD'
byte4 = bytes(str4, 'ascii')
list4 = list(byte4)
print("list4 = ", list4)

list5 = [ i + 128 for i in list4]
print("list5 = ", list5)
byte5 = bytes(list5)
print("byte5 = ", byte5)

list6 = [ hex(i) for i in list5]
print("list6 = ", list6)

