# Write a program that prints the number of times the string 'bob' occurs in s.
# For example, if s = 'azcbobobegghakl', then your program should print  Number of times bob occurs is: 2

strSample = 'bob'
s = 'azcbobobegghakl'
numOcc = 0
slen = len(s)
sslen = len(strSample)
for i in range(slen-sslen):
    if s[i:i+sslen] == strSample:
        numOcc += 1
print(numOcc)
