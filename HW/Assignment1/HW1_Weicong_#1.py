#Write a program that counts up the number of vowels contained in the string s.
#Valid vowels are: 'a', 'e', 'i', 'o', and 'u'.
#For example, if  s = 'azcbobobegghakl', your program should print:  Number of vowels: 5

vowels = ['a','e','i','o','u']
strInput = input("Plese input a string: ")
num = 0
for c in strInput:
    if c in vowels:
        num += 1
print("Number of vowels: ",num)
