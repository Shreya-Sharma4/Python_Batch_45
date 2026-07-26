numbers = list(map(int, input("Enter numbers separated by space: ").split()))

unique_numbers = list(set(numbers))

if len(unique_numbers) < 2:
    print("There is no second largest number.")
else:
    unique_numbers.sort()
    print("Second largest number is:", unique_numbers[-2])