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


st.title("Overall Performance Overview")

st.write("""
#### Welcome to the Overall Performance Report page.
 
This section provides an insightful analysis of the academic achievements 
of students across various sessions. The primary focus here is on the 
number of graduating students categorized by their final 
Cumulative Grade Point Average (CGPA) classifications.

In this report, the following can be explored:
         
- **Number of Graduating Students**: View the count of students 
who have graduated based on different CGPA classifications.

- **CGPA Classification**: Understand the distribution of students across 
various performance brackets, helping to gauge the overall academic 
performance of the student body.

- **Session Filter**: Use the slicer to filter the data by specific 
academic sessions to view performance trends over time.

Interact with the report to gain a comprehensive 
understanding of academic performance and track the 
progress of graduating students by their final CGPA.
         
""")


st.write("<br><br>", unsafe_allow_html=True)


# Data Visualization
st.write("# Visualization")

st.write("<br><br>", unsafe_allow_html=True)


import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import math

# Load Data (assuming CSV files, replace with actual data loading)
# Academic_Performance = pd.read_csv('Academic_Performance.csv')
# Registration = pd.read_csv('Registration.csv')

# Merging the dataframes
merged_df = pd.merge(Academic_Performance, Registration, 
                     on=['Matric_Number', 'Session', 'Semester'], 
                     how='inner')

# Sidebar - Semester Slicer
semester = st.sidebar.selectbox("Select Semester:", options=['All'] + merged_df['Semester'].unique().tolist())

# Filter the data based on the selected Semester
if semester != 'All':
    filtered_df = merged_df[merged_df['Semester'] == semester]
else:
    filtered_df = merged_df

# Group sessions by sets of 2 or 3
sessions = sorted(filtered_df['Session'].unique())
sessions_per_page = 2  # Adjust this to 3 if you want 3 sessions per page
total_pages = math.ceil(len(sessions) / sessions_per_page)

# Sidebar - Pagination Controls
pagination_cols = st.sidebar.columns([1, 2, 1])
with pagination_cols[0]:
    prev_page = st.button("Previous")
with pagination_cols[1]:
    current_page = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1, format="%d")
with pagination_cols[2]:
    next_page = st.button("Next")

# Adjust current page based on button clicks
if prev_page and current_page > 1:
    current_page -= 1

if next_page and current_page < total_pages:
    current_page += 1

# Sidebar - Slider for adjusting plot height
plot_height = st.sidebar.slider("Adjust Plot Height:", min_value=100, max_value=800, value=300)

# Determine the sessions to display on the current page
start_idx = (current_page - 1) * sessions_per_page
end_idx = start_idx + sessions_per_page
current_sessions = sessions[start_idx:end_idx]

# Filter the data for the current page sessions
page_df = filtered_df[filtered_df['Session'].isin(current_sessions)]

# CGPA Classification order and colors
classification_order = ['First Class', 'Second Class Upper', 'Second Class Lower', 'Third Class', 'Pass', 'Fail']
classification_colors = {
    'First Class': '#0BE10B',
    'Second Class Upper': '#FF7F0E',
    'Second Class Lower': '#FF0DE3',
    'Third Class': '#744EC2',
    'Pass': '#CAD626',
    'Fail': '#105CFF'
}

# Plotting the charts for each level
levels = sorted(page_df['Level'].unique())
figures = []

for level in levels:
    level_df = page_df[page_df['Level'] == level]
    grouped_df = level_df.groupby(['Session', 'CGPA_Classification']).agg(
        DistinctStudentCount=('Matric_Number', 'nunique')
    ).reset_index()

    # Create Plotly bar chart for each level
    fig = go.Figure()
    for classification in classification_order:
        class_df = grouped_df[grouped_df['CGPA_Classification'] == classification]
        fig.add_trace(go.Bar(
            x=class_df['DistinctStudentCount'],
            y=class_df['Session'],
            name=classification,
            orientation='h',
            marker_color=classification_colors[classification],
            text=class_df['DistinctStudentCount'],  # Add data labels
            textposition='outside'  # Position labels automatically
        ))

    fig.update_layout(
        barmode='group',
        height=plot_height,
        title=f"Level {level} - CGPA Classification Distribution",
        xaxis_title="Distinct Student Count",
        yaxis_title="Session",
        legend_title="CGPA Classification",
        xaxis=dict(tickformat='d'),
        yaxis=dict(categoryorder='category ascending',
                   autorange='reversed'),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    figures.append(fig)

# Display all four charts on the current page
for fig in figures:
    st.plotly_chart(fig)















st.write("<br><br><br><br>", unsafe_allow_html=True)
