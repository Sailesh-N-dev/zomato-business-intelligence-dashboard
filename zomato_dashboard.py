import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="Zomato Business Dashboard",
    page_icon="🍽️",
    layout="wide"
)

# ---------------- DASHBOARD DESIGN ----------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #101827, #202d46);
    color: white;
}
[data-testid="stSidebar"] {
    background-color: #17243a;
}
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #263650, #30445f);
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #405775;
}
h1, h2, h3, p, label {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATASET ----------------

@st.cache_data
def load_data():
    data = pd.read_csv("Zomato Restaurant Dataset.csv")

    data["Cuisines"] = data["Cuisines"].fillna("Unknown")

    return data

df = load_data()

# ---------------- TITLE ----------------

st.title("🍽️ ZOMATO BUSINESS INTELLIGENCE")
st.caption("Restaurant Market Analysis | Customer Insights | Business Performance")

st.divider()

# ---------------- SIDEBAR FILTERS ----------------

st.sidebar.title("🎛️ Dashboard Filters")

# Country filter
countries = sorted(df["Country Code"].dropna().unique())

selected_countries = st.sidebar.multiselect(
    "Select Country",
    countries,
    default=countries
)

filtered_df = df[
    df["Country Code"].isin(selected_countries)
]

# City filter
cities = sorted(filtered_df["City"].dropna().unique())

selected_cities = st.sidebar.multiselect(
    "Select City",
    cities
)

if selected_cities:
    filtered_df = filtered_df[
        filtered_df["City"].isin(selected_cities)
    ]

# Price filter
prices = sorted(filtered_df["Price range"].dropna().unique())

selected_prices = st.sidebar.multiselect(
    "Select Price Range",
    prices,
    default=prices
)

if selected_prices:
    filtered_df = filtered_df[
        filtered_df["Price range"].isin(selected_prices)
    ]
else:
    filtered_df = filtered_df.iloc[0:0]

# Delivery filter
delivery = st.sidebar.selectbox(
    "Online Delivery",
    ["All", "Yes", "No"]
)

if delivery != "All":
    filtered_df = filtered_df[
        filtered_df["Has Online delivery"] == delivery
    ]

# Table booking filter
booking = st.sidebar.selectbox(
    "Table Booking",
    ["All", "Yes", "No"]
)

if booking != "All":
    filtered_df = filtered_df[
        filtered_df["Has Table booking"] == booking
    ]

# ---------------- CHECK FILTER RESULTS ----------------

if filtered_df.empty:
    st.warning("No data available for these filters.")
    st.stop()

# ---------------- KPI CALCULATIONS ----------------

rated_df = filtered_df[
    filtered_df["Aggregate rating"] > 0
]

total_restaurants = len(filtered_df)

average_rating = (
    rated_df["Aggregate rating"].mean()
    if not rated_df.empty else 0
)

total_votes = filtered_df["Votes"].sum()

total_cities = filtered_df["City"].nunique()

# ---------------- KPI DISPLAY ----------------

st.subheader("📊 Business Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Restaurants",
    f"{total_restaurants:,}"
)

col2.metric(
    "Average Rating",
    f"{average_rating:.2f} / 5"
)

col3.metric(
    "Total Votes",
    f"{total_votes:,.0f}"
)

col4.metric(
    "Cities",
    f"{total_cities:,}"
)

st.divider()

# ---------------- CITY ANALYSIS ----------------

st.subheader("📍 Restaurant Market Analysis")

city_counts = (
    filtered_df["City"]
    .value_counts()
    .head(10)
    .reset_index()
)

city_counts.columns = ["City", "Restaurants"]

fig_city = px.bar(
    city_counts,
    x="Restaurants",
    y="City",
    orientation="h",
    color="Restaurants",
    text="Restaurants",
    color_continuous_scale="Turbo",
    title="Top 10 Cities by Restaurant Count"
)

fig_city.update_layout(
    template="plotly_dark",
    yaxis={"categoryorder": "total ascending"},
    coloraxis_showscale=False
)

st.plotly_chart(
    fig_city,
    use_container_width=True
)

# ---------------- PRICE ANALYSIS ----------------

st.subheader("💰 Price Range Analysis")

col1, col2 = st.columns(2)

with col1:

    price_rating = (
        rated_df.groupby("Price range")["Aggregate rating"]
        .mean()
        .reset_index()
    )

    fig_price = px.bar(
        price_rating,
        x="Price range",
        y="Aggregate rating",
        color="Price range",
        text_auto=".2f",
        color_continuous_scale="Plasma",
        title="Average Rating by Price Range"
    )

    fig_price.update_layout(
        template="plotly_dark",
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig_price,
        use_container_width=True
    )

with col2:

    price_count = (
        filtered_df["Price range"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    price_count.columns = ["Price Range", "Restaurants"]

    fig_pie = px.pie(
        price_count,
        names="Price Range",
        values="Restaurants",
        hole=0.5,
        color_discrete_sequence=px.colors.qualitative.Bold,
        title="Restaurant Distribution by Price"
    )

    fig_pie.update_layout(
        template="plotly_dark"
    )

    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )

# ---------------- CUISINE ANALYSIS ----------------

st.subheader("🍕 Cuisine Analysis")

cuisine_df = filtered_df.copy()

cuisine_df["Cuisine"] = cuisine_df["Cuisines"].str.split(",")

cuisine_df = cuisine_df.explode("Cuisine")

cuisine_df["Cuisine"] = cuisine_df["Cuisine"].str.strip()

cuisine_count = (
    cuisine_df.groupby("Cuisine")["Restaurant ID"]
    .nunique()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

cuisine_count.columns = ["Cuisine", "Restaurants"]

fig_cuisine = px.bar(
    cuisine_count,
    x="Restaurants",
    y="Cuisine",
    orientation="h",
    color="Restaurants",
    text="Restaurants",
    color_continuous_scale="Tealgrn",
    title="Top 10 Most Popular Cuisines"
)

fig_cuisine.update_layout(
    template="plotly_dark",
    yaxis={"categoryorder": "total ascending"},
    coloraxis_showscale=False
)

st.plotly_chart(
    fig_cuisine,
    use_container_width=True
)

# ---------------- DELIVERY ANALYSIS ----------------

st.subheader("🛵 Online Delivery Analysis")

delivery_analysis = (
    rated_df.groupby("Has Online delivery")
    .agg(
        Restaurant_Count=("Restaurant ID", "count"),
        Average_Rating=("Aggregate rating", "mean")
    )
    .reset_index()
)

fig_delivery = px.bar(
    delivery_analysis,
    x="Has Online delivery",
    y="Average_Rating",
    color="Has Online delivery",
    text_auto=".2f",
    color_discrete_sequence=["#00CC96", "#636EFA"],
    title="Online Delivery vs Average Rating"
)

fig_delivery.update_layout(
    template="plotly_dark"
)

st.plotly_chart(
    fig_delivery,
    use_container_width=True
)

# ---------------- TABLE BOOKING ANALYSIS ----------------

st.subheader("🪑 Table Booking Analysis")

booking_analysis = (
    rated_df.groupby("Has Table booking")
    .agg(
        Restaurant_Count=("Restaurant ID", "count"),
        Average_Rating=("Aggregate rating", "mean")
    )
    .reset_index()
)

fig_booking = px.bar(
    booking_analysis,
    x="Has Table booking",
    y="Average_Rating",
    color="Has Table booking",
    text_auto=".2f",
    color_discrete_sequence=["#FFA15A", "#AB63FA"],
    title="Table Booking vs Average Rating"
)

fig_booking.update_layout(
    template="plotly_dark"
)

st.plotly_chart(
    fig_booking,
    use_container_width=True
)

# ---------------- CUSTOMER ENGAGEMENT ----------------

st.subheader("⭐ Customer Engagement")

scatter_df = rated_df[
    rated_df["Votes"] > 0
]

fig_scatter = px.scatter(
    scatter_df,
    x="Votes",
    y="Aggregate rating",
    color="Price range",
    size="Votes",
    hover_name="Restaurant Name",
    title="Customer Votes vs Restaurant Ratings",
    color_continuous_scale="Turbo"
)

fig_scatter.update_layout(
    template="plotly_dark"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

# ---------------- TOP RESTAURANTS ----------------

st.subheader("🏆 Top Rated Restaurants")

top_restaurants = (
    rated_df.sort_values(
        by=["Aggregate rating", "Votes"],
        ascending=[False, False]
    )
    .head(15)
)

st.dataframe(
    top_restaurants[
        [
            "Restaurant Name",
            "City",
            "Cuisines",
            "Aggregate rating",
            "Votes",
            "Price range"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# ---------------- DOWNLOAD DATA ----------------

st.divider()

st.subheader("📥 Download Analysis Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Filtered Dataset",
    csv,
    "zomato_filtered_data.csv",
    "text/csv"
)

# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "Zomato Business Intelligence Dashboard | "
    "Built with Python, Pandas, Streamlit and Plotly"
)