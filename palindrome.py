num = int(input("Enter number: "))

if num < 0:
    print("Negative numbers are not palindrome")
else:
    temp = num
    rev = 0

    while num > 0:
        rem = num % 10
        rev = rev * 10 + rem
        num = num // 10

    if temp == rev:
        print("Palindrome")
    else:
        print("Not Palindrome")