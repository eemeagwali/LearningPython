# ▶️ 1. Creating Variables and Assigning Values
name = "Emmanuel Emeagwali"
age = 35
height = 1.75  # in meters
is_student = False
print("Name:", name)
print("Age:", age)
print("Height:", height)
print("Is student:", is_student)

# ✅ Task 1: Create variables for your city (string), number of kids (int), and has_pet (boolean)
city = "Vancouver"
num_kids = 2
has_pet = True
print("Your city:", city)
print("Number of kids:", num_kids)
print("Has pet:", has_pet)

# ▶️ 2. Reassigning Variables
age = 36 # Happy birthday!

print("\nNew age after birthday:", age)
# ✅ Task 2: Change the value of your city variable to another city and print it
city = "Toronto"
print ("\nNew city:", city)

# ▶️ 3. Using Variables in Expressions
year_born = 2025-age
print ("\nYear Born:", year_born)

# ✅ Task 3: Calculate the age your kids will be in 5 years and print
kids_age_in_5_years = num_kids + 5 # Assuming Num_kids is the total number, change logic is needed
print ("Kids age in 5 years (assuming starting age = num_kids):", kids_age_in_5_years)

 #▶️ 4. Data Types Check
print("\nType of name:", type(name))
print("Type of age:", type(age))
print("Type of height:", type(height))
print("Type of is_student:", type(is_student))

# ✅ Task 4: Print the data type of your city, num_kids, and has_pet variables
print("Type of city:", type(city))
print("Type of num_kids:", type(num_kids))
print("Type of has_pet:", type(has_pet))

# ▶️ 5. String Concatenation Using Variables
greeting = "Hello, my name is " + name + " and I live in " + city + "."
print("\n" + greeting)


# ✅ Task 5: Create a sentence introducing yourself using your variables and print it


my_intro = f"My name is {name}, I am {age} years old, and I live in {city}."
print(my_intro)

# ▶️ 1. Create a List
fruits = ["apple", "banana", "cherry", "mango"]
print("Initial List:", fruits)

# ✅ Task 1: Add "orange" to the list and print the updated list
fruits.append("orange")
print("After adding 'orange':", fruits)

# ▶️ 2. Accessing List Elements
print("First fruit", fruits[0]) #index starts at 0
print("Last fruit", fruits[-1]) #negative index starts from end

# ✅ Task 2: Print the second and third fruits using slicing
print("Second and first fruits:", fruits[1:3])

# ▶️ 3. Modifying Elements
fruits[1]="blueberry" #changing banana to blueberry
print("After modification:", fruits)

# ✅ Task 3: Change "cherry" to "pineapple"
index_cherry=fruits.index("cherry")
fruits[index_cherry]="pineapple"
print("After changing 'cherry' to 'pineapple':", fruits)

# ✅ Task 4: Add "lemon" at the beginning of the list
fruits.insert(0, "lemon")
print("After adding 'lemon' at beginning:", fruits)

# ▶️ 5. Removing Items
fruits.remove("apple") #Removes first occurrence of "apple"
popped_fruit = fruits.pop() #Removes first occurrence of "apple"
print("After removing 'apple' and popping last item:", fruits)
print("Popped fruit:", popped_fruit)

# ✅ Task 5: Remove "mango" and print the list
fruits.remove("mango")
print("After removing 'mango':", fruits)

# ▶️ 6. Sorting and Reversing
fruits.sort()
print("Sorted list:", fruits)

fruits.reverse()
print("Reversed list:", fruits)

# ✅ Task 6: Sort in reverse alphabetical order without changing original list
sorted_reversed = sorted(fruits, reverse = True)
print("Reverse-sorted (new list):", sorted_reversed)
print("Original list remains:", fruits)

# ▶️ 7. Iterating Over a List
print("Fruits one by one:")
for fruit in fruits:
    print("Fruit:", fruit)

# ✅ Task 7: Print each fruit in uppercase
print("Fruits in uppercase:")
for fruit in fruits:
    print(fruit.upper())

# ▶️ 8. List Comprehension
fruit_lengths = [len(fruit) for fruit in fruits]
print("Lengths of each fruit name:", fruit_lengths)

# ✅ Task 8: New list with fruits containing the letter 'e'
fruits_with_e = [fruit for fruit in fruits if 'e' in fruit]
print("fruits with 'e':", fruits_with_e)

# 🏆 Bonus Challenge:
# Given a list of prices, write a function to apply a discount
prices = [20, 30, 50, 100, 80]
def discount_prices(prices, discount):
    """Apply a discount % to each price and return a new list."""
    discounted = [round(price*(1-discount/100), 2) for price in prices]
    return discounted

# Test the function
discounted_10 = discount_prices(prices, 10)
print("Original prices:", prices)
print("Prices after 10% discount:", discounted_10)

# ✅ Try changing the discount to 25% and print again
discounted_25=discount_prices(prices, 25)
print("Prices after 25% discount:", discounted_25)