import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from data_loader import load_data


# Loading the data
data = load_data()

# Passing the Data into Variables
Academic_Performance = data["Academic_Performance"]
Biodata = data["Biodata"]
First_and_Last_Result = data["First_and_Last_Result"]
Registration = data["Registration"]
Result_Sheet = data["Result_Sheet"]


st.title("Enrollment Trend Analysis")

st.markdown("""

#### Welcome to the Enrollment Trend Section. 
         
This Section provides an in-depth look at how student enrollment has evolved over 
time, offering key insights into the patterns and changes in student demographics.

The report is designed to give a comprehensive view of the following trends:

1. **Trend of Number of Students by Session:** Explore how the total number of 
         students has varied across different academic sessions, highlighting 
         periods of growth or decline.

2. **Trend of Admitted Students by Year of Admission:** Delve into the yearly 
         admission trends, identifying the influx of new students over the years 
         and understanding the factors that may influence these patterns.

3. **Number of Students Admitted by Year and Gender:** Analyze the gender 
         distribution among admitted students year by year, offering insights 
         into gender diversity and shifts over time.

These visualizations will help one to better understand the dynamics of student 
         enrollment and support data-driven decision-making for academic 
         planning and resource allocation. 

Explore the data and uncover the stories behind the numbers!
""")


st.markdown("<br><br><br>", unsafe_allow_html=True)


# Visualizations
st.write("# Data Visualizations")
st.write("This is where the visualizations and detailed analysis will be displayed.")


st.markdown("<br><br><br>", unsafe_allow_html=True)

#------------------------------ Total Number of Students by Session ------------------------------

# Correcting the wrong entries in the Session column
Registration['Session'] = Registration['Session'].replace({
    '90-92': '1990-1991',
    '97/98': '1997-1998'
})

# Grouping the data by 'Session' and counting the number of unique 'Matric_Number'
students_by_session = Registration.groupby('Session')['Matric_Number'].nunique().reset_index()

# Creating the line chart using Plotly Express
fig = px.line(students_by_session, 
              x='Session', 
              y='Matric_Number', 
              title='Trend of Number of Students by Session',
              labels={'Matric_Number': 'Number of Students', 'Session': 'Session'})

# Customizing the line color
fig.update_traces(line=dict(color='#DE6A73'))

# Displaying the chart in Streamlit
st.plotly_chart(fig)



st.markdown("<br><br><br>", unsafe_allow_html=True)

#------------------------- Trend of Admitted Students by Year of Admissio --------------------------


# Grouping the data by 'Session' and counting the number of unique 'Matric_Number'
students_by_YOA = Biodata.groupby('YOA')['Matric_Number'].nunique().reset_index()

# Creating the line chart using Plotly Express
fig = px.line(students_by_YOA, 
              x='YOA', 
              y='Matric_Number', 
              title='Trend of Admitted Students by Year of Admission',
              labels={'Matric_Number': 'Number of Admitted Students', 'YOA': 'Year of Admission'})

# Customizing the line color
fig.update_traces(line=dict(color='#DE6A73'))

# Displaying the chart in Streamlit
st.plotly_chart(fig)

