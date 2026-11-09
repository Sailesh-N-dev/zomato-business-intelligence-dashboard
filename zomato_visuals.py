import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("Zomato Restaurant Dataset.csv")

# Calculate average rating
price_rating = df.groupby("Price range")["Aggregate rating"].mean()

# Create bar chart
price_rating.plot(kind="bar")

plt.title("Average Restaurant Rating by Price Range")
plt.xlabel("Price Range")
plt.ylabel("Average Rating")

plt.xticks(rotation=0)

# Display ratings above bars
for index, value in enumerate(price_rating):
    plt.text(index, value + 0.05, round(value, 2), ha="center")

plt.tight_layout()
plt.show()

# Top 10 cities by restaurant count
city_counts = df["City"].value_counts().head(10)

plt.figure(figsize=(12, 6))

city_counts.plot(kind="bar")

plt.title("Top 10 Cities by Restaurant Count")
plt.xlabel("City")
plt.ylabel("Number of Restaurants")

plt.xticks(rotation=45, ha="right")

for index, value in enumerate(city_counts):
    plt.text(index, value + 30, value, ha="center")

plt.tight_layout()
plt.show()