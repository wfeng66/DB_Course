# With a given integral number n, w
# rite a program to generate a dictionary that contains  (​I,I x I)
# such that is an integral number between 1 and n (both included).
# and then the program should print the dictionary.
# Suppose the following input is supplied to the program: 8
# Output is: {1: 1, 2: 4, 3: 9, 4: 16, 5: 25, 6: 36, 7: 49, 8: 64} 6

# approach 1
urDir = {}
n = 8
for i in range(1,n+1):
    urDir[i] = i*i
print(urDir)


# approach 2
l1 = [x for x in range(1,(n+1))]
l2 = [x*x for x in range(1,(n+1))]

for i in range(n):
    urDir[l1[i]]=l2[i]
print(urDir)
