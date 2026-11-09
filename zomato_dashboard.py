
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Zomato Business Intelligence Dashboard",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==================================================
# THEME COLOURS
# ==================================================

BG = "#111719"
CARD = "#1B2428"
TEAL = "#00C9B7"
TEAL_LIGHT = "#63E6D8"
RED = "#E23744"
WHITE = "#F5F7F7"
MUTED = "#AAB8BC"


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {BG};
        color: {WHITE};
    }}

    [data-testid="stSidebar"] {{
        display: none;
    }}

    h1, h2, h3 {{
        color: {WHITE} !important;
    }}

    [data-testid="stMetric"] {{
        background: {CARD};
        border: 1px solid #2B393D;
        border-radius: 12px;
        padding: 18px;
    }}

    [data-testid="stMetricLabel"] {{
        color: {MUTED} !important;
    }}

    [data-testid="stMetricValue"] {{
        color: {TEAL_LIGHT} !important;
    }}

    .section-caption {{
        color: {TEAL};
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: -12px;
    }}

    .dashboard-subtitle {{
        color: {MUTED};
        font-size: 15px;
    }}

    .zomato-line {{
        height: 4px;
        width: 75px;
        background: {RED};
        border-radius: 5px;
        margin: 8px 0 18px 0;
    }}

    div[data-testid="stDataFrame"] {{
        border: 1px solid #2B393D;
        border-radius: 10px;
    }}

    div.stDownloadButton button {{
        background-color: {RED};
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }}

    div.stDownloadButton button:hover {{
        background-color: #BD2935;
        color: white;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# LOAD DATASET
# ==================================================

DATA_FILE = Path(__file__).parent / "Zomato Restaurant Dataset.csv"


@st.cache_data
def load_data(file_path):

    data = pd.read_csv(file_path)

    numeric_columns = [
        "Restaurant ID",
        "Country Code",
        "Average Cost for two",
        "Price range",
        "Aggregate rating",
        "Votes"
    ]

    for column in numeric_columns:
        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )

    data["Votes"] = data["Votes"].fillna(0)

    data["City"] = data["City"].fillna("Unknown")
    data["Cuisines"] = data["Cuisines"].fillna("Unknown")
    data["Rating text"] = data["Rating text"].fillna("Not specified")
    data["Rating color"] = data["Rating color"].fillna("Unknown")

    return data


try:
    df = load_data(DATA_FILE)

except FileNotFoundError:
    st.error(
        "Dataset not found. Keep 'Zomato Restaurant Dataset.csv' "
        "in the same folder as zomato_dashboard.py."
    )
    st.stop()

except Exception as error:
    st.error(f"Dataset loading error: {error}")
    st.stop()


# ==================================================
# CHECK DATASET COLUMNS
# ==================================================

required_columns = [
    "Restaurant ID",
    "Restaurant Name",
    "Country Code",
    "City",
    "Cuisines",
    "Average Cost for two",
    "Currency",
    "Has Table booking",
    "Has Online delivery",
    "Is delivering now",
    "Price range",
    "Aggregate rating",
    "Rating color",
    "Rating text",
    "Votes"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(f"Missing columns: {missing_columns}")
    st.stop()


# ==================================================
# DASHBOARD HEADER
# ==================================================

st.caption("ZOMATO  /  BUSINESS INTELLIGENCE")

st.title("🍽️ ZOMATO BUSINESS INTELLIGENCE DASHBOARD")

st.markdown(
    '<div class="zomato-line"></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="dashboard-subtitle">'
    'Restaurant Market Analysis &nbsp; | &nbsp; '
    'Customer Insights &nbsp; | &nbsp; '
    'Business Performance'
    '</p>',
    unsafe_allow_html=True
)

st.write("")


# ==================================================
# TOP FILTER CONTROLS - NO SIDEBAR
# ==================================================

st.markdown(
    '<p class="section-caption">DASHBOARD CONTROLS</p>',
    unsafe_allow_html=True
)

st.subheader("Customize Your Analysis")

# Country filter
country_options = sorted(
    df["Country Code"].dropna().unique().tolist()
)

selected_countries = st.multiselect(
    "Country Code",
    options=country_options,
    default=country_options
)

country_df = df[
    df["Country Code"].isin(selected_countries)
]

# City filter
city_options = sorted(
    country_df["City"].dropna().unique().tolist()
)

selected_cities = st.multiselect(
    "City",
    options=city_options,
    default=city_options
)

city_df = country_df[
    country_df["City"].isin(selected_cities)
]

# Price range filter
price_options = sorted(
    city_df["Price range"].dropna().unique().tolist()
)

selected_prices = st.multiselect(
    "Price Range",
    options=price_options,
    default=price_options,
    format_func=lambda x: f"Range {int(x)}"
)

price_df = city_df[
    city_df["Price range"].isin(selected_prices)
]

# Online delivery and table booking
filter1, filter2 = st.columns(2)

with filter1:

    delivery_options = sorted(
        price_df["Has Online delivery"].dropna().unique().tolist()
    )

    selected_delivery = st.multiselect(
        "Online Delivery",
        options=delivery_options,
        default=delivery_options
    )

with filter2:

    booking_options = sorted(
        price_df["Has Table booking"].dropna().unique().tolist()
    )

    selected_booking = st.multiselect(
        "Table Booking",
        options=booking_options,
        default=booking_options
    )

filtered_df = price_df[
    price_df["Has Online delivery"].isin(selected_delivery)
    & price_df["Has Table booking"].isin(selected_booking)
].copy()

st.caption(
    f"Showing {len(filtered_df):,} of {len(df):,} restaurants"
)

st.divider()

if filtered_df.empty:
    st.warning("No restaurants match the selected filters.")
    st.stop()


# ==================================================
# PREPARE ANALYSIS DATA
# ==================================================

rated_df = filtered_df[
    filtered_df["Aggregate rating"] > 0
].copy()

average_rating = (
    rated_df["Aggregate rating"].mean()
    if not rated_df.empty else 0
)

total_votes = filtered_df["Votes"].sum()

total_cities = filtered_df["City"].nunique()


# ==================================================
# CHART DESIGN FUNCTION
# ==================================================

def style_chart(fig, height=380):

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font=dict(
            color=WHITE,
            family="Arial"
        ),
        height=height,
        margin=dict(
            l=25,
            r=25,
            t=55,
            b=35
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)"
        )
    )

    fig.update_xaxes(
        gridcolor="#344247",
        zerolinecolor="#344247"
    )

    fig.update_yaxes(
        gridcolor="#344247",
        zerolinecolor="#344247"
    )

    return fig


# ==================================================
# KPI SECTION
# ==================================================

st.markdown(
    '<p class="section-caption">BUSINESS OVERVIEW</p>',
    unsafe_allow_html=True
)

st.subheader("Key Performance Indicators")

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Total Restaurants",
    f"{len(filtered_df):,}"
)

k2.metric(
    "Average Rating",
    f"{average_rating:.2f} / 5"
)

k3.metric(
    "Total Customer Votes",
    f"{total_votes:,.0f}"
)

k4.metric(
    "Cities Covered",
    f"{total_cities:,}"
)

st.write("")


# ==================================================
# CITY ANALYSIS
# ==================================================

st.markdown(
    '<p class="section-caption">LOCATION INTELLIGENCE</p>',
    unsafe_allow_html=True
)

st.subheader("Restaurant Distribution by City")

city_counts = (
    filtered_df["City"]
    .value_counts()
    .head(10)
    .reset_index()
)

city_counts.columns = [
    "City",
    "Restaurants"
]

fig_city = px.bar(
    city_counts.sort_values("Restaurants"),
    x="Restaurants",
    y="City",
    orientation="h",
    text="Restaurants",
    color="Restaurants",
    color_continuous_scale=[
        "#145B59",
        TEAL_LIGHT
    ],
    title="Top 10 Cities by Restaurant Count"
)

fig_city.update_traces(
    textposition="outside"
)

fig_city = style_chart(fig_city)

st.plotly_chart(
    fig_city,
    width="stretch",
    config={"displayModeBar": False}
)


# ==================================================
# CUISINE ANALYSIS
# ==================================================

st.markdown(
    '<p class="section-caption">FOOD & MARKET TRENDS</p>',
    unsafe_allow_html=True
)

st.subheader("Cuisine Popularity")

cuisine_series = (
    filtered_df["Cuisines"]
    .str.split(",")
    .explode()
    .str.strip()
)

cuisine_counts = (
    cuisine_series[cuisine_series != "Unknown"]
    .value_counts()
    .head(10)
    .reset_index()
)

cuisine_counts.columns = [
    "Cuisine",
    "Restaurant Count"
]

fig_cuisine = px.bar(
    cuisine_counts.sort_values("Restaurant Count"),
    x="Restaurant Count",
    y="Cuisine",
    orientation="h",
    text="Restaurant Count",
    color="Restaurant Count",
    color_continuous_scale=[
        "#145B59",
        TEAL
    ],
    title="Top 10 Most Common Cuisines"
)

fig_cuisine.update_traces(
    textposition="outside"
)

fig_cuisine = style_chart(fig_cuisine)

st.plotly_chart(
    fig_cuisine,
    width="stretch",
    config={"displayModeBar": False}
)


# ==================================================
# CUSTOMER RATING ANALYSIS
# ==================================================

st.markdown(
    '<p class="section-caption">CUSTOMER EXPERIENCE</p>',
    unsafe_allow_html=True
)

st.subheader("Restaurant Rating Analysis")

rating_col1, rating_col2 = st.columns(2)

with rating_col1:

    rating_distribution = (
        filtered_df["Rating text"]
        .value_counts()
        .reset_index()
    )

    rating_distribution.columns = [
        "Rating",
        "Restaurant Count"
    ]

    fig_rating = px.pie(
        rating_distribution,
        names="Rating",
        values="Restaurant Count",
        hole=0.55,
        title="Distribution of Customer Ratings",
        color_discrete_sequence=[
            RED,
            TEAL,
            "#3E8E8C",
            "#7C8F93",
            "#D6A84F",
            "#64748B"
        ]
    )

    fig_rating = style_chart(fig_rating)

    st.plotly_chart(
        fig_rating,
        width="stretch",
        config={"displayModeBar": False}
    )

with rating_col2:

    price_rating = (
        rated_df.groupby("Price range")["Aggregate rating"]
        .mean()
        .reset_index()
    )

    price_rating["Price range"] = (
        price_rating["Price range"].astype(str)
    )

    fig_price_rating = px.bar(
        price_rating,
        x="Price range",
        y="Aggregate rating",
        text_auto=".2f",
        color="Aggregate rating",
        color_continuous_scale=[
            "#145B59",
            TEAL_LIGHT
        ],
        title="Average Rating by Price Range"
    )

    fig_price_rating.update_yaxes(
        range=[0, 5]
    )

    fig_price_rating = style_chart(fig_price_rating)

    st.plotly_chart(
        fig_price_rating,
        width="stretch",
        config={"displayModeBar": False}
    )


# ==================================================
# PRICE DISTRIBUTION
# ==================================================

st.markdown(
    '<p class="section-caption">PRICING INTELLIGENCE</p>',
    unsafe_allow_html=True
)

st.subheader("Restaurant Price Distribution")

price_counts = (
    filtered_df["Price range"]
    .value_counts()
    .sort_index()
    .reset_index()
)

price_counts.columns = [
    "Price Range",
    "Restaurant Count"
]

price_counts["Price Range"] = (
    price_counts["Price Range"]
    .apply(lambda x: f"Range {int(x)}")
)

fig_price = px.pie(
    price_counts,
    names="Price Range",
    values="Restaurant Count",
    hole=0.55,
    title="Restaurants Across Price Categories",
    color_discrete_sequence=[
        TEAL,
        "#238F89",
        "#D6A84F",
        RED
    ]
)

fig_price = style_chart(fig_price)

st.plotly_chart(
    fig_price,
    width="stretch",
    config={"displayModeBar": False}
)


# ==================================================
# ONLINE DELIVERY ANALYSIS
# ==================================================

st.markdown(
    '<p class="section-caption">DELIVERY PERFORMANCE</p>',
    unsafe_allow_html=True
)

st.subheader("Online Delivery and Customer Ratings")

delivery_rating = (
    rated_df.groupby("Has Online delivery")["Aggregate rating"]
    .mean()
    .reset_index()
)

fig_delivery = px.bar(
    delivery_rating,
    x="Has Online delivery",
    y="Aggregate rating",
    text_auto=".2f",
    color="Has Online delivery",
    color_discrete_sequence=[
        RED,
        TEAL
    ],
    title="Average Rating: Online Delivery vs No Online Delivery"
)

fig_delivery.update_yaxes(
    range=[0, 5]
)

fig_delivery = style_chart(fig_delivery)

st.plotly_chart(
    fig_delivery,
    width="stretch",
    config={"displayModeBar": False}
)


# ==================================================
# TABLE BOOKING ANALYSIS
# ==================================================

st.markdown(
    '<p class="section-caption">SERVICE ANALYSIS</p>',
    unsafe_allow_html=True
)

st.subheader("Table Booking and Customer Ratings")

booking_rating = (
    rated_df.groupby("Has Table booking")["Aggregate rating"]
    .mean()
    .reset_index()
)

fig_booking = px.bar(
    booking_rating,
    x="Has Table booking",
    y="Aggregate rating",
    text_auto=".2f",
    color="Has Table booking",
    color_discrete_sequence=[
        RED,
        TEAL
    ],
    title="Average Rating: Table Booking vs No Table Booking"
)

fig_booking.update_yaxes(
    range=[0, 5]
)

fig_booking = style_chart(fig_booking)

st.plotly_chart(
    fig_booking,
    width="stretch",
    config={"displayModeBar": False}
)


# ==================================================
# CUSTOMER ENGAGEMENT ANALYSIS
# ==================================================

st.markdown(
    '<p class="section-caption">CUSTOMER ENGAGEMENT</p>',
    unsafe_allow_html=True
)

st.subheader("Customer Votes vs Restaurant Ratings")

scatter_df = rated_df[
    [
        "Restaurant Name",
        "Aggregate rating",
        "Votes",
        "City"
    ]
].copy()

if len(scatter_df) > 3000:
    scatter_df = scatter_df.sample(
        n=3000,
        random_state=42
    )

fig_scatter = px.scatter(
    scatter_df,
    x="Votes",
    y="Aggregate rating",
    color="Aggregate rating",
    hover_name="Restaurant Name",
    hover_data=["City"],
    color_continuous_scale=[
        "#238F89",
        TEAL_LIGHT,
        RED
    ],
    title="Relationship Between Customer Votes and Ratings",
    opacity=0.7
)

fig_scatter.update_yaxes(
    range=[0, 5]
)

fig_scatter = style_chart(fig_scatter)

st.plotly_chart(
    fig_scatter,
    width="stretch",
    config={"displayModeBar": False}
)


# ==================================================
# TOP RESTAURANTS
# ==================================================

st.markdown(
    '<p class="section-caption">RESTAURANT PERFORMANCE</p>',
    unsafe_allow_html=True
)

st.subheader("Top 15 Restaurants by Customer Votes")

top_restaurants = (
    filtered_df[
        [
            "Restaurant Name",
            "City",
            "Cuisines",
            "Aggregate rating",
            "Rating text",
            "Votes",
            "Price range",
            "Has Online delivery"
        ]
    ]
    .sort_values(
        by=["Votes", "Aggregate rating"],
        ascending=[False, False]
    )
    .head(15)
    .reset_index(drop=True)
)

st.dataframe(
    top_restaurants,
    width="stretch",
    hide_index=True
)


# ==================================================
# DOWNLOAD FILTERED DATA
# ==================================================

st.markdown(
    '<p class="section-caption">DATA EXPORT</p>',
    unsafe_allow_html=True
)

st.subheader("Download Your Filtered Dataset")

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=csv_data,
    file_name="zomato_filtered_analysis.csv",
    mime="text/csv",
    use_container_width=True
)


# ==================================================
# DATASET INFORMATION
# ==================================================

st.divider()

with st.expander("View Dataset Information"):

    info1, info2, info3 = st.columns(3)

    info1.metric(
        "Total Dataset Rows",
        f"{len(df):,}"
    )

    info2.metric(
        "Dataset Columns",
        f"{len(df.columns)}"
    )

    info3.metric(
        "Missing Values",
        f"{df.isnull().sum().sum():,}"
    )

    st.subheader("Dataset Preview")

    st.dataframe(
        filtered_df.head(20),
        width="stretch",
        hide_index=True
    )


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "ZOMATO BUSINESS INTELLIGENCE DASHBOARD"
)

st.caption(
    "Restaurant Market Analysis | Customer Insights | Business Performance"
)

st.caption(
    "Developed using Python, Pandas, Plotly and Streamlit"
)
