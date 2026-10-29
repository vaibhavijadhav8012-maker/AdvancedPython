
import numpy as np

# Method 1: Using np.array()
arr1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Method 2: Using np.arange()
arr2 = np.arange(1, 11)

print("Array using np.array():", arr1)
print("Array using np.arange():", arr2)

# Array attributes
print("Data type:", arr1.dtype)
print("Shape:", arr1.shape)
print("Dimensions:", arr1.ndim)
print("Size:", arr1.size)

# Mathematical operations
print("Array multiplied by 2:", arr1 * 2)
print("Array plus 100:", arr1 + 100)
print("Sum:", arr1.sum())
print("Mean:", arr1.mean())

# Indexing and slicing
print("First element:", arr1[0])
print("Last element:", arr1[-1])
print("First five elements:", arr1[:5])
print("Every second element:", arr1[::2])

# Check if both arrays are equal
print("Are both arrays equal?", np.array_equal(arr1, arr2))
