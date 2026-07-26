a = int(input("Enter a number: "))
n = len(str(a))
temp = a
sum = 0

while temp > 0:
    digit = temp % 10
    sum += digit ** n
    temp //= 10

if sum = a:
    print(a, "is an Armstrong number")
else:
    print(a, "is not an Armstrong number")