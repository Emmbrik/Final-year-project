import streamlit as st
from data_loader import load_data
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Loading the data
data = load_data()

# Passing the Data into Variables
Academic_Performance = data["Academic_Performance"]
Biodata = data["Biodata"]
First_and_Last_Result = data["First_and_Last_Result"]
Registration = data["Registration"]
Result_Sheet = data["Result_Sheet"]


# Page title and introduction
st.title("Student Registration")

# Introducing the Student's Registration page

st.markdown("""

#### Welcome to the Student Registration Report Report.
            
This section provides a comprehensive overview of student enrollment 
            data across different academic sessions and levels.

Here, you can explore:
- **Number of Students by Session:** Track the number of students 
enrolled in each academic session to understand enrollment trends and shifts over time.

- **Number of Students by Level:** Gain insights into the distribution 
of students across various academic levels, helping to identify trends and needs at each level.

            
The slicers can be used to filter data by session, and academic level 
to get a detailed and customized view of the performance metrics.

This dynamic feature allows the viewing of specific areas of interest.
""")


# Visualizations
st.write("# Data Visualizations")


st.markdown("<br><br><br>", unsafe_allow_html=True)

# Replacing session labels with desired format
session_mapping = {
    '97/98': '1997-1998',
    '90-92': '1990-1991'
    # Add other mappings as necessary
}

# Applying the session mapping
Registration['Session'] = Registration['Session'].replace(session_mapping)

# Defining the custom sorting order for sessions from 1990 to 2011
custom_sort_order = [
    '1990-1991', '1991-1992', '1992-1993',  '1994-1995',
    '1995-1996', '1996-1997', '1997-1998', '1998-1999', '1999-2000',
    '2000-2001', '2001-2002', '2002-2003', '2003-2004', 
    '2005-2006', '2006-2007', '2007-2008', '2008-2009', '2009-2010',
    '2010-2011'
]

# Create filters for session and level
selected_sessions = st.multiselect(
    'Select Sessions',
    options=custom_sort_order,
    default=custom_sort_order  # Show all by default
)

selected_levels = st.multiselect(
    'Select Levels',
    options=sorted(Registration['Level'].unique()),
    default=sorted(Registration['Level'].unique())  # Show all by default
)

# Ensure that if no filters are selected, all data is used
if not selected_sessions:
    selected_sessions = custom_sort_order
if not selected_levels:
    selected_levels = sorted(Registration['Level'].unique())

# Filter the data based on user selection
filtered_data = Registration[
    (Registration['Session'].isin(selected_sessions)) &
    (Registration['Level'].isin(selected_levels))
]

# Group the data by 'Session' and 'Level' and count the number of distinct students
student_counts = filtered_data.groupby(['Session', 'Level'])['Matric_Number'].nunique().reset_index(name='Distinct_Students')

# Define the custom colors for each level
level_colors = {
    100: '#105CFF',
    200: '#0BE10B',
    300: '#CAD626',
    400: '#FF0DE3',
    500: '#FF7F0E'
}

# Create the grouped horizontal bar chart
fig = go.Figure()

# Loop through each level and add a trace for each level
for level in sorted(filtered_data['Level'].unique()):
    level_data = student_counts[student_counts['Level'] == level]
    fig.add_trace(go.Bar(
        y=level_data['Session'],
        x=level_data['Distinct_Students'],
        name=f'{level}L',
        marker_color=level_colors.get(level, '#000000'),  # Default color if level not in dictionary
        orientation='h',
        text=level_data['Distinct_Students'],
        textposition='outside',  # Ensure text is visible outside of the bars
        #textangle=0,
        #textfont=dict(size=80, color='black')  # Set text color to black and size for visibility
    ))

# Create a slider to adjust the height of the plot
plot_height = st.slider('Adjust plot height for Visibility', min_value=800, max_value=2500, value=1200)

# Update layout to group bars, remove background, and customize axis
fig.update_layout(
    barmode='group',
    xaxis_title='Number of Students',
    yaxis_title='Session',
    yaxis=dict(
        categoryorder='array',
        categoryarray=custom_sort_order,  # Apply custom sorting order
        autorange='reversed'  # Ensure that years are ordered from 1990 to 2011
    ),
    xaxis=dict(
        gridcolor='gray',
        showgrid=True,
        gridwidth=1,
        griddash='dot',  # Set grid lines to dotted
        zeroline=False
    ),
    plot_bgcolor='rgba(0,0,0,0)',  # Remove background color
    paper_bgcolor='rgba(0,0,0,0)',  # Remove paper background color
    showlegend=True,
    legend_title = 'Level',
    height=plot_height,  # Use height from the slider
    margin=dict(l=50, r=50, t=50, b=50)  # Adjust margins to make space for labels
)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)





