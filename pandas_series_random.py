
import numpy as np
import pandas as pd

# Step 1: Create a Series with 10 random numbers
def create_random_series(n=10, seed=42):
    rng = np.random.default_rng(seed)
    values = rng.integers(low=1, high=100, size=n)
    return pd.Series(values)

# Step 2: Create a Series with custom labels
def create_labeled_series(series):
    labels = [f"num_{i + 1}" for i in range(len(series))]
    return pd.Series(series.values, index=labels)

# Step 3: Display Series details
def describe_series(s, title="Series"):
    print(title)
    print(s)
    print("\nData type:", s.dtype)
    print("Shape:", s.shape)
    print("Size:", s.size)
    print("Index:", list(s.index))

# Main program
if __name__ == "__main__":

    # Default index
    series = create_random_series()
    print("STEP 1: Series with default index")
    describe_series(series)

    # Custom labels
    labeled = create_labeled_series(series)
    print("\nSTEP 2: Series with custom labels")
    describe_series(labeled, "Labeled Series")

    # Basic statistics
    print("\nSTEP 3: Basic Statistics")
    print("Minimum:", series.min())
    print("Maximum:", series.max())
    print("Mean:", round(series.mean(), 2))
    print("Sum:", series.sum())

    # Sort values
    print("\nSTEP 4: Sorted Values")
    print(series.sort_values().to_string())

    # Indexing and filtering
    print("\nSTEP 5: Indexing and Filtering")
    print("First value:", series.iloc[0])
    print("Values greater than 50:")
    print(series[series > 50].to_string())
