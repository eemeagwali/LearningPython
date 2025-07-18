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


# ▶️ 1. Creating a List of Lists (2D List)
# Let's say we have student scores for 3 students in 3 subjects
scores=[
[85, 92, 78], #Student 1
[76, 88, 90], #Student 2
[90, 91, 95] #Student 3
]
print("Initial scores:", scores)

# ▶️ 2. Accessing Elements
print("Score of Student 1 in Subject 2:", scores[0][1]) #92

# ✅ Task 1: Print score of Student 3 in Subject 3
print("Student 3 Subject 3:", scores[2][2])

# ▶️ 3. Iterating through a List of Lists
print("All scores row by row:")
for student_scores in scores:
    print(student_scores)

# ✅ Task 2: Print each individual score in a tabular format
print("Individual scores:")
for i, student_scores in enumerate(scores):
    for j, score in enumerate(student_scores):
        print(f"Student{i+1}, Subject{j+1}: {score}")

# ▶️ 4. Adding a New Student's Scores
scores.append([88, 79, 85])
print("After adding Student 4:", scores)

# ✅ Task 3: Add another student with scores [70, 80, 90]
scores.append([70, 80, 90])
print("After adding Student 5:", scores)

# ▶️ 5. Updating a Value
# Let's update Student 2's score in Subject 1 to 95
scores[1][0]=95
print("After updating Student 2's Subject 1 score:", scores)

# ✅ Task 4: Change Student 5's Subject 2 score to 82
scores[4][1]=82
print("After updating Student 5's Subject 2 score:", scores)

# ▶️ 6. Calculating Averages
print("Average score per student:")
for i, student_scores in enumerate(scores):
    avg=sum(student_scores)/len(student_scores)
    print(f"Student{i+1} average: {round(avg,2)}")

# ✅ Task 5: Print subject-wise average (column-wise average)
print("Average score per subject:")
num_subjects = len(scores[0])
num_students = len(scores)

for subj in range(num_subjects):
    total=sum(scores[student][subj] for student in range(num_students))
    avg=total/num_students
    print(f"Subject{subj+1} average:{round(avg,2)}")

# ▶️ 7. Flattening a List of Lists into a Single List
all_scores=[score for student in scores for score in student]
print("All scores flattened:", all_scores)

# ✅ Task 6: Find the highest score among all students
highest=max(all_scores)
print("Highest score among all students:", highest)

#Variables & Data Types
# ▶️ 1. Creating Variables and Assigning Values
name = "Emmanuel Emeagwali"
age = 35
height = 1.75 # in metres
is_student = False

print("\nName:", name)
print("Age:", age)
print("Height:", height)
print("Is student:", is_student)

# ✅ Task 1: Create variables for your city (string), number of kids (int), and has_pet (boolean)
city = "Vancouver"
num_kids = 2
has_pet = True

print("\nYour city", city)
print("Number of kids:", num_kids)
print("Has pet:", has_pet)

# ▶️ 2. Reassigning Variables
age = 48  # Happy birthday!
print("\nNew age after birthday:", age)

# ✅ Task 2: Change the value of your city variable to another city and print it
city = "Toronto"
print("\nNew city:", city)

# ▶️ 3. Using Variables in Expressions
year_born = 2025 - age
print("\nYear born:", year_born)

# ✅ Task 3: Calculate the age your kids will be in 5 years and print
kids_age_in_5_years = num_kids + 5  # Assuming num_kids is the total number, change logic as needed
print("\nKids' age in 5 years (assuming starting age = num_kids):", kids_age_in_5_years)

# ▶️ 4. Data Types Check
print("\nType of name:", type(name))
print("Type of age:", type(age))
print("Type of height:", type(height))
print("Type of is_student:", type(is_student))

# ✅ Task 4: Print the data type of your city, num_kids, and has_pet variables
print("\nType of city:", type(city))
print("Type of num_kids:", type(num_kids))
print("Type of has_pet:", type(has_pet))

# ▶️ 5. String Concatenation Using Variables
greeting = "Hello, my name is " + name + " and I live in " + city + "."
print("\n" + greeting)

# ✅ Task 5: Create a sentence introducing yourself using your variables and print it
my_intro = f"My name is {name}, I am {age} years old, and I live in {city}."
print("\n" + my_intro)

# numpy_tutorial.py
# 🧮 NumPy Tutorial: Learn NumPy by Writing and Running Code

# Import NumPy
import numpy as np



