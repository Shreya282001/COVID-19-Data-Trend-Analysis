COVID-19 Data Trend Analysis

Overview
This project performs end-to-end analysis of global COVID-19 data using PySpark for large-scale processing and Streamlit for interactive visualization. It is designed to extract trends such as daily confirmed cases, deaths, recoveries, and recovery rates. The project also includes a final report notebook for visualization and a dashboard app for user exploration.

Folder Structure
- data: Contains raw data files such as covid19_dataset.csv
- output: Stores processed output data generated from Spark jobs
- notebooks: Jupyter notebooks for exploratory analysis and final reporting
- scripts: Python scripts used for processing and visualization

Files and Their Purpose

1. notebooks/data_cleaning_exploration.ipynb
   Performs initial data cleaning, inspection, and formatting before modeling or analysis.

2. notebooks/final_report_visualization.ipynb
   Generates recovery rate plots and line charts using processed data; ideal for sharing as a report.

3. scripts/trend_analysis_spark.py
   Uses PySpark to calculate total and daily trends in confirmed, deaths, and recoveries. It also computes 7-day moving averages.

4. scripts/recovery_rate_spark_sql.py
   Defines modular Spark SQL queries to compute global and country-specific COVID-19 recovery rates.

5. scripts/covid_dashboard_streamlit.py
   Launches an interactive dashboard using Streamlit. Allows users to filter COVID-19 data by country and date, and view various plots including:
   - Line chart of trends
   - Scatter plot for daily confirmed cases
   - Correlation heatmap
   - Pie chart of case distribution

How to Run

1. Install dependencies
   Use pip to install necessary packages
   pip install -r requirements.txt

2. Run the Streamlit Dashboard
   streamlit run scripts/covid_dashboard_streamlit.py

3. Use PySpark Scripts
   Ensure Spark is installed and run the analysis or SQL scripts from the scripts folder

Notes
- Input CSV data must be present in the data folder before running scripts
- Output files (processed CSVs) will be generated in the output folder
- Streamlit app supports interactive filtering and real-time metric display

Author
This project was created as part of a Cloud Computing course to demonstrate scalable data analysis and visualization techniques.