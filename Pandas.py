#📊 Python Tutorial: Getting Started with pandas
# 🧠 What is pandas?
# pandas is a Python library for data manipulation and analysis.
# It offers two core data structures:
# - Series: a 1D labeled array
# - DataFrame: a 2D labeled table (like a spreadsheet)
# It is built on top of NumPy
# ---------------------------------------------
# 🛠️ Installation (run in terminal if not installed)
# pip install pandas
import pandas as pd
# 📈 1. Creating Data Structures
# ---------------------------------------------
# ➤ Series
s = pd.Series([10,20,30,40])
print("Series:\n", s)

# ➤ DataFrame
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25,30,35],
    'Salary': [70000, 80000, 90000]
}
df= pd.DataFrame(data)
print("\nDataFrame:\n", df)

# 🔍 2. Reading and Writing Files
# ➤ Reading CSV
# df = pd.read_csv('your_file.csv')  # Uncomment when file is available
# ➤ Writing CSV
# df.to_csv('output.csv', index=False)  # Uncomment to save file

# ---------------------------------------------
# 🔄 3. Basic Operations
# ---------------------------------------------
# ➤ Viewing Data
print("\nHead:\n", df.head())      # First 5 rows
print("\nTail:\n", df.tail())      # Last 5 rows
print("\nInfo:")
df.info()                          # Info about columns
print("\nDescribe:\n", df.describe())  # Summary stats

# 🎛 4. Filtering and Conditional Selection
print("\nPeople older than 30:\n", df[df['Age'] > 30])
print("\nPeople named Alice:\n", df[df['Name'] == 'Alice'])

# 🧹 5. Data Cleaning
# ➤ Handling Missing Data
print("\nCheck missing:\n", df.isnull())
# df.dropna()              # Drop missing rows
# df.fillna(0)             # Fill missing with 0

# ➤ Renaming Columns
df.rename(columns={'Age': 'Years'}, inplace=True)
print("\nRenamed column:\n", df.head())

# 🔢 6. Data Aggregation
# ---------------------------------------------
# ➤ Group by and sum
print("\nSalary by Name:\n", df.groupby('Name')['Salary'].sum())
# ➤ Mean salary
print("\nAverage Salary:", df['Salary'].mean())

# 📊 7. Sorting and Indexing
print("\nSorted by Years:\n", df.sort_values('Years'))
df.set_index('Name', inplace=True)
print("\nSet Name as index:\n", df)

# 📆 8. Working with Dates
# Add a fake date column for example
df['Date'] = pd.to_datetime(['2023-01-01', '2023-02-01', '2023-03-01'])
df['Year'] = df['Date'].dt.year
print("\nAdded Date and Year columns:\n", df)

# 🧮 9. Merging and Joining
df1 = pd.DataFrame({'ID': [1, 2], 'Name': ['Alice', 'Bob']})
df2 = pd.DataFrame({'ID': [1, 2], 'Salary': [70000, 80000]})

# Merge on ID
merged_df = pd.merge(df1, df2, on='ID')
print("\nMerged DataFrame:\n", merged_df)

# 🧪 10. Applying Functions
df.reset_index(inplace=True)  # Reset index to access Name as column again
df['Years_plus_5'] = df['Years'].apply(lambda x: x + 5)
print("\nApplied function to Years column:\n", df[['Name', 'Years', 'Years_plus_5']])

# ---------------------------------------------
# 📌 Example: End-to-End Mini Project
# ---------------------------------------------
# Simulated example if 'employees.csv' existed
# Uncomment and use when 'employees.csv' is available:
# df = pd.read_csv('employees.csv')
# high_earners = df[df['Salary'] > 75000]
# df['Tax'] = df['Salary'] * 0.3
# department_stats = df.groupby('Department')['Salary'].mean()
# print("\nDepartment Stats:\n", department_stats)
# ✅ Tutorial Complete
print("\n✅ pandas tutorial completed!")

