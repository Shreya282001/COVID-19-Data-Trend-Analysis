import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import base64

# Background CSS
def add_background_image(image_file):
    with open(image_file, "rb") as image:
        encoded_image = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_image}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function to add the background image
add_background_image("coronavirus.jpg")

# Load dataset
data = pd.read_csv("covid19_dataset.csv")
data['Last_Update'] = pd.to_datetime(data['Last_Update'])
data.columns = data.columns.str.strip()  # Clean column names

# Streamlit App Layout
st.title("COVID-19 Trend Analysis")
st.sidebar.header("Filter Options")

# Sidebar Filters
countries = data['Country_Region'].unique()
selected_country = st.sidebar.selectbox("Select a Country", countries)
date_range = st.sidebar.date_input(
    "Select Date Range",
    [data['Last_Update'].min().date(), data['Last_Update'].max().date()],
    min_value=data['Last_Update'].min().date(),
    max_value=data['Last_Update'].max().date(),
)

# Filtered Data
filtered_data = data[
    (data['Country_Region'] == selected_country) &
    (data['Last_Update'] >= pd.to_datetime(date_range[0])) &
    (data['Last_Update'] <= pd.to_datetime(date_range[1]))
]

# Metrics
latest_data = filtered_data.iloc[-1]
st.metric("Total Confirmed", latest_data["Confirmed"])
st.metric("Total Deaths", latest_data["Deaths"])
st.metric("Total Recovered", latest_data["Recovered"])


# Line Chart
st.subheader(f"COVID-19 Trends for {selected_country}")
fig_line = px.line(
    filtered_data,
    x="Last_Update",
    y=["Confirmed", "Deaths", "Recovered"],
    labels={"value": "Cases", "Last_Update": "Date"},
    title="Trend Over Time"
)
st.plotly_chart(fig_line)

# Scatter Plot for Daily Changes
filtered_data['Daily_Confirmed'] = filtered_data['Confirmed'].diff().fillna(0)
fig_scatter = px.scatter(
    filtered_data,
    x="Last_Update",
    y="Daily_Confirmed",
    title="Daily New Cases (Confirmed)",
    labels={"Last_Update": "Date", "Daily_Confirmed": "Daily Cases"},
    color="Daily_Confirmed",
    color_continuous_scale=px.colors.sequential.Viridis
)
st.plotly_chart(fig_scatter)

# Heatmap
st.subheader("Correlation Heatmap")
corr = filtered_data[["Confirmed", "Deaths", "Recovered"]].corr()
fig_heatmap, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig_heatmap)

# Pie Chart
st.subheader("Proportional Distribution")
latest_distribution = latest_data[["Confirmed", "Deaths", "Recovered"]]
fig_pie = px.pie(
    values=latest_distribution.values,
    names=latest_distribution.index,
    title="Distribution of COVID-19 Cases"
)
st.plotly_chart(fig_pie)


