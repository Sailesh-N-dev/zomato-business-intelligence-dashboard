# 🍽️ Zomato Business Intelligence Dashboard

An interactive data analytics project exploring restaurant data to uncover business insights, customer preferences, restaurant performance, and market trends.

## 📊 Project Overview

This project uses Python to analyse the Zomato restaurant dataset and presents key findings through data visualisations and an interactive Streamlit dashboard.

## 🚀 Key Features

- Restaurant distribution across cities
- Restaurant ratings and customer voting patterns
- Popular cuisines and cuisine ratings
- Price range analysis
- Online delivery analysis
- Table booking analysis
- Interactive dashboard filters
- Top-rated restaurant exploration

## 🛠️ Technologies Used

- Python
- Pandas
- Matplotlib
- Plotly
- Streamlit

## 📁 Project Structure

```text
zomato-business-intelligence-dashboard/
│
├── zomato_analysis.py
├── zomato_visuals.py
├── zomato_dashboard.py
├── .gitignore
└── README.md
```

## ⚙️ Installation & Setup

1. Clone the repository:

```bash
git clone https://github.com/Sailesh-N-dev/zomato-business-intelligence-dashboard.git
```

2. Navigate to the project folder:

```bash
cd zomato-business-intelligence-dashboard
```

3. Create a virtual environment:

```bash
python -m venv .venv
```

4. Activate it on Windows:

```powershell
.venv\Scripts\activate
```

5. Install the required libraries:

```bash
pip install pandas matplotlib plotly streamlit
```

## 📂 Dataset

The original Zomato restaurant CSV dataset is not included in this repository.

Place `Zomato Restaurant Dataset.csv` in the project root directory before running the scripts. Make sure you have permission to use the dataset.

## ▶️ Run the Dashboard

```bash
streamlit run zomato_dashboard.py
```

## 📈 Learning Outcomes

- Data cleaning and preprocessing
- Exploratory data analysis (EDA)
- Data grouping and aggregation
- Data visualisation
- Interactive dashboard development
- Business insight interpretation

## ⚠️ Analytical Notes

- Unrated restaurants may have a rating of 0.
- Restaurants can appear under multiple cuisine categories.
- Cost comparisons across countries require currency awareness.
- Relationships in the dataset do not necessarily indicate causation.

## 👨‍💻 Author

**Sailesh N**

BSc Data Analytics Student

[GitHub Profile](https://github.com/Sailesh-N-dev)

---

*Built as a hands-on learning project to develop practical data analytics and business intelligence skills.*
