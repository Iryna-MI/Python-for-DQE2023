import random
#список
my_list = []

#1 create list of 100 random numbers from 0 to 1000
for i in range(0, 100): #100 numbers
    # random int - randon int value
    n = random.randint(1, 1000) #random values in range of 0 to 1000
    # add random value to the list
    my_list.append(n)

print(my_list)

#2 sort list from min to max (without using sort())
# variable for sorted list
sorted_list = []
# while the list values exist
while my_list:
    minimum = my_list[0]  # assign the first number of list as a minimum value
    for x in my_list:  # look through the every element in the list
        if x < minimum:  # check if current element is less than minimum value
            minimum = x  # if current element is less than minimum value than minimum = x
    sorted_list.append(minimum)  # add value of minimum to the sorted list
    my_list.remove(minimum)  # remove value of minimum to the sorted list

print (sorted_list)

#3 calculate average for even and odd numbers
#variables for summs of odd and even numbers
sum_odd, sum_even = 0, 0
#counters for odd and even numbers
i, j = 0, 0
#loop for looking through the list
for num in sorted_list:
    if num % 2 == 0: #check if number is odd
        i +=1 #if number is odd -> counter i is increased by 1
        sum_odd += num #if number is odd -> add number to the summ of odd mumbers
    else: # else - if number is not odd
        j += 1 #if number is not odd (even) -> counter j is increased by 1
        sum_even += num #if number is not odd (even)  -> add number to the summ of even mumbers

#4 print both average result in console
#find averages if i or j are not zero
#for the case that the list could not include odd or even numbers ->try is used (to avoid division by zero)
try:
    print("Average odd numbers = ", sum_odd / i)
    print("Average even numbers = ", sum_even / j)
except ZeroDivisionError:
    print("Division by zero")






