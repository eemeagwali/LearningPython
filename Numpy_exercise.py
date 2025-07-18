import numpy as np

# 1. Creating Arrays
# Create a 1D array from a list
a = np.array([1, 2, 3])
print("1D Array:", a)

# Create a 2D array (matrix)
b=np.array([[1,2],[3,4]])
print("2D Array:\n", b)

# 2. Array Properties
print("\nShape:", a.shape)
print("Dimensions:", a.ndim)
print("Data type:", a.dtype)
print("Total elements:", a.size)

# 3. Special Arrays
print("Zeros:\n", np.zeros((2,3)))
print("Ones:\n", np.ones((3, 3)))
print("Full with 7s:\n", np.full((2,3),7))
print("Identity Matrix:\n", np.eye(4))
print("Range with step:\n", np.arange(0,10,2))
print("Evenly spaced:\n", np.linspace(0,1,5))

#4. Reshaping & Flattening
arr = np.arange(1,7)
reshaped = arr.reshape((2,3))
print("Reshaped 2x3:\n", reshaped)
print("Flattened:", reshaped.flatten())
