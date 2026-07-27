print("-"*30)
print("      Number Programming")
print("-"*30)
while True:
    print("1.Check Palindrome\n2.Check Armstrong\n3.Find Second Largest\n4.Exit\nEnter your choice")
    choice=int(input())
    match choice:
        case 1:
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

        case 2:
            a = int(input("Enter a number: "))
            n = len(str(a))
            temp = a
            sum = 0

            while temp > 0:
                digit = temp % 10
                sum += digit ** n
                temp //= 10

            if sum == a:
                print(a, "is an Armstrong number")
            else:
                print(a, "is not an Armstrong number")

        case 3:
            numbers = list(map(int, input("Enter numbers separated by space: ").split()))

            unique_numbers = list(set(numbers))

            if len(unique_numbers) < 2:
                print("There is no second largest number.")
            else:
                unique_numbers.sort()
                print("Second largest number is:", unique_numbers[-2])

        case 4:
            print("Exit")
            break

        case _:
            print("Invalid Input\nChoose from 1,2 or 3")