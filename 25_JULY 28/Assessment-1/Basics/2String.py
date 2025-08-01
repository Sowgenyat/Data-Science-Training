str=input("enter the string:")
rev=str[::-1]
print(rev)
if(str==rev):
    print("palindrome")
else:
    print("not a palindrome")