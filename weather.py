import pandas as pd
import matplotlib.pyplot as plt

# Load CSV file
df = pd.read_csv("weather.csv")

# Calculate temperature statistics
print("Average Temperature:", df['Temperature'].mean())
print("Maximum Temperature:", df['Temperature'].max())
print("Minimum Temperature:", df['Temperature'].min())

# Find day with highest temperature
day = df.loc[df['Temperature'].idxmax(), 'Date']
print("Day with Highest Temperature:", day)

# Line chart
plt.plot(df['Date'], df['Temperature'], marker='o')
plt.title("Daily Temperature Changes")
plt.xlabel("Date")
plt.ylabel("Temperature")
plt.xticks(rotation=45)
plt.show()

# Histogram
plt.hist(df['Temperature'], bins=5)
plt.title("Temperature Distribution")
plt.xlabel("Temperature")
plt.ylabel("Frequency")
plt.show()

# Scatter plot
plt.scatter(df['Humidity'], df['Temperature'])
plt.title("Humidity vs Temperature")
plt.xlabel("Humidity")
plt.ylabel("Temperature")
plt.show()