# Write a program that accepts a sentence and calculate the number of uppercase letters and lowercase letters.
# Suppose the following input is supplied to the program.
# Input: Hello World
# Output: UPPERCASE: 1, LOWERCASE: 9

s = input("Please input a string: ")
cUpp, cLow = 0,0
for i in s:
    if i.isupper():
        cUpp += 1
    elif i.islower():
        cLow += 1
print("UPPERCASE: ", cUpp, ",\tLOWERCASE: ", cLow)
