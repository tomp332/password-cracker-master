prefix = "05"
numbers = []

for i in range(100000000):
    number = prefix + str(i).zfill(8)
    numbers.append(number)

# Write the generated phone numbers to a file
with open("./phone_numbers.txt", "w") as file:
    for number in numbers:
        file.write(number + "\n")
