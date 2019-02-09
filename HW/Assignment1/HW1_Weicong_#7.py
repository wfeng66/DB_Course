# Ask the user to enter a string, and check if it is a palindrome. If yes, print True, or else print False.

str1 = input("Please input a string: ")
if str1[0] == str1[-1]:
    print('True')
else:
    print('False')
