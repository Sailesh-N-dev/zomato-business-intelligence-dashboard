import pandas as pd

# Data Loading

df = pd.read_csv("Zomato Restaurant Dataset.csv")

print(df.head())
print(df.shape)
print(df.columns)
df.info()


# Data Exploration

# 1. Display first 5 rows
print(df.head())

# 2. Display last 5 rows
print(df.tail())

# 3. Check rows and columns
print(df.shape)

# 4. Display column names
print(df.columns)

# 5. Understand dataset information
df.info()

# 6. Statistical summary
print(df.describe())

# 7. Count unique restaurant names
print(df["Restaurant Name"].nunique())

# 8. Count restaurant records by city
print(df["City"].value_counts())


# Data Cleaning and Preprocessing


# 1. Check missing values
print(df.isnull().sum())

# 2. Check duplicate records
print(df.duplicated().sum())

# 3. Check unique restaurant names
print(df["Restaurant Name"].nunique())

# Check missing cuisines
print("Before cleaning:")
print(df["Cuisines"].isnull().sum())

# Replace missing cuisine values
df["Cuisines"] = df["Cuisines"].fillna("Unknown")

# Check again
print("After cleaning:")
print(df["Cuisines"].isnull().sum())

# Find restaurants with ratings above 4.0

high_rated = df[df["Aggregate rating"] >= 4.0]

print(high_rated)

print(high_rated.shape)

# Find restaurants with ratings above 4.0 and online delivery available

high_rated_delivery = df[
    (df["Aggregate rating"] > 4.0) &
    (df["Has Online delivery"] == "Yes")
]

print(high_rated_delivery.shape)

# find restaurants with ratings above 4.5 or more than 1000 votes

popular_restaurants = df[
    (df["Aggregate rating"] > 4.5) |
    (df["Votes"] > 1000)
]

print(popular_restaurants.shape)

# Find top 10 restaurants based on ratings
top_rated = df.sort_values(
    by="Aggregate rating",
    ascending=False
)

# find top 10 restaurants based on ratings and votes
print(top_rated[["Restaurant Name", "City", "Aggregate rating", "Votes"]].head(10))

top_restaurants = df.sort_values(
    by=["Aggregate rating", "Votes"],
    ascending=[False, False]
)

print(
    top_restaurants[
        ["Restaurant Name", "City", "Aggregate rating", "Votes"]
    ].head(10)
)

# Find the number of restaurants in each city and printing the top 10 cities with the most restaurants
city_restaurants = df.groupby("City")["Restaurant ID"].count()

city_restaurants = city_restaurants.sort_values(
    ascending=False
)

print(city_restaurants.head(10))

# Find the average rating of restaurants in each city and printing the top 10 cities with the highest average ratings
city_ratings = df.groupby("City")["Aggregate rating"].mean()

city_ratings = city_ratings.sort_values(
    ascending=False
)

print(city_ratings.head(10))

# Find the number of restaurants and average rating in each city and printing the top 10 cities with the most restaurants and highest average ratings

city_analysis = df.groupby("City").agg(
    restaurant_count=("Restaurant ID", "count"),
    average_rating=("Aggregate rating", "mean")
)

city_analysis = city_analysis.sort_values(
    by="restaurant_count",
    ascending=False
)

print(city_analysis.head(10))


# Find the cities with more than 100 restaurants and sort them by average rating in descending order
large_cities = city_analysis[
    city_analysis["restaurant_count"] >= 100
]

large_cities = large_cities.sort_values(
    by="average_rating",
    ascending=False
)

print(large_cities)

# Find the top 10 cuisines based on the number of restaurants serving them
cuisine_counts = df["Cuisines"].value_counts()

print(cuisine_counts.head(10))

# Find the popularity of individual cuisines by splitting the "Cuisines" column and counting the occurrences of each cuisine
individual_cuisines = df["Cuisines"].str.split(", ").explode()

cuisine_popularity = individual_cuisines.value_counts()

print(cuisine_popularity.head(10))


# Find the average rating of restaurants serving each cuisine and printing the top 10 cuisines with the highest average ratings
cuisine_ratings = df.assign(
    Cuisine=df["Cuisines"].str.split(", ")
).explode("Cuisine")

cuisine_rating_analysis = cuisine_ratings.groupby("Cuisine").agg(
    restaurant_count=("Restaurant ID", "count"),
    average_rating=("Aggregate rating", "mean")
)

cuisine_rating_analysis = cuisine_rating_analysis[
    cuisine_rating_analysis["restaurant_count"] >= 50
]

cuisine_rating_analysis = cuisine_rating_analysis.sort_values(
    by="average_rating",
    ascending=False
)

print(cuisine_rating_analysis.head(10))

# Find the average cost for two people for restaurants serving each cuisine and printing the top 10 cuisines with the highest average cost for two
cuisine_cost = df.assign(
    Cuisine=df["Cuisines"].str.split(", ")
).explode("Cuisine")

cuisine_cost_analysis = cuisine_cost.groupby("Cuisine").agg(
    restaurant_count=("Restaurant ID", "count"),
    average_cost=("Average Cost for two", "mean")
)

cuisine_cost_analysis = cuisine_cost_analysis[
    cuisine_cost_analysis["restaurant_count"] >= 50
]

cuisine_cost_analysis = cuisine_cost_analysis.sort_values(
    by="average_cost",
    ascending=False
)

# Find the top 10 cuisines with the highest average cost for two
print(cuisine_cost_analysis.head(10))

price_analysis = df["Price range"].value_counts().sort_index()

print(price_analysis)

price_rating = df.groupby("Price range")["Aggregate rating"].mean()

print(price_rating)

# Find the number of restaurants and average rating for each price range and printing the top 10 price ranges with the most restaurants and highest average ratings
delivery_analysis = df.groupby("Has Online delivery").agg(
    restaurant_count=("Restaurant ID", "count"),
    average_rating=("Aggregate rating", "mean")
)

print(delivery_analysis)

# Find the number of restaurants and average rating for each rating text and printing the top 10 rating texts with the most restaurants and highest average ratings
vote_analysis = df.groupby("Rating text").agg(
    restaurant_count=("Restaurant ID", "count"),
    average_votes=("Votes", "mean"),
    average_rating=("Aggregate rating", "mean")
)

print(vote_analysis.sort_values(
    by="average_votes",
    ascending=False
))