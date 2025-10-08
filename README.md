# Dashboard_sleephealth

## Description
A simple streamlit dashboard with custom CSS and populated with dummy data on sleep and health

## Snapshot
<img width="1071" height="852" alt="Dashboard Snap" src="https://github.com/user-attachments/assets/c71f2b0a-f448-43e9-8ec7-913a87833b21" />

## Features

Contains
- 3 KPI cards
-  sidebar with filtering options with category selection and slider bar
-  Main dashboard with plotly charts
-  Using custom CSS

## Notes

- Code will run dashboard locally on your computer
- Using streamlit components so ensure streamlit installed
- To use custom CSS style in streamlit need to use arg unsafe_allow_html=TRUE, if deploying it publicly under this condition, could pose security issue if text user input can be injected into the code
- For trendlines on scatter use statsmodels package
