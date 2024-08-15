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


st.title("Grade Distribution Report")

st.markdown("""

#### Welcome to the Grade Distribution Report.
 
Here, an insightful analysis of how grades are distributed across different courses 
is presented. This page visualizes the number of students who have achieved 
various grades in each course, allowing the assessment of the overall performance and 
grading trends within the academic programs.

By exploring this data, one can identify patterns in student performance, evaluate 
the effectiveness of grading standards, and make informed decisions to support 
academic development.
            
Use the interactive charts and graphs below to gain a deeper 
understanding of the distribution of grades and uncover any notable trends.
""")


# Visualization
st.write("# Data Visualizations")
st.write("This is where the visualizations and detailed analysis will be displayed.")





import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Assuming the Result_Sheet dataframe is already loaded
df = Result_Sheet.copy()

# Define the custom color map for grades
grade_colors = {
    'A': '#0BE10B',
    'B': '#105CFF',
    'C': '#CAD626',
    'D': '#FF0DE3',
    'E': '#FF7F0E',
    'F': '#744EC2'
}

# Group by Course_Title and Grade, and count distinct Matric_Number
grouped_data = df.groupby(['Course_Title', 'Grade'])['Matric_Number'].nunique().reset_index(name='Distinct_Students')

# Sorting within each Course_Title by Distinct_Students in descending order
grouped_data = grouped_data.sort_values(['Course_Title', 'Distinct_Students'], ascending=[True, False])

# Create filters for Course Title, Session, and Level
selected_courses = st.multiselect(
    'Select Course Titles',
    options=sorted(df['Course_Title'].unique()),
    default=sorted(df['Course_Title'].unique())  # Show all by default
)

selected_sessions = st.multiselect(
    'Select Sessions',
    options=sorted(df['Session'].unique()),
    default=sorted(df['Session'].unique())  # Show all by default
)

selected_levels = st.multiselect(
    'Select Levels',
    options=sorted(df['Level'].unique()),
    default=sorted(df['Level'].unique())  # Show all by default
)

# Ensure that if no filters are selected, all data is used
if not selected_courses:
    selected_courses = sorted(df['Course_Title'].unique())
if not selected_sessions:
    selected_sessions = sorted(df['Session'].unique())
if not selected_levels:
    selected_levels = sorted(df['Level'].unique())

# Filter the data based on user selection
filtered_df = df[
    (df['Course_Title'].isin(selected_courses)) &
    (df['Session'].isin(selected_sessions)) &
    (df['Level'].isin(selected_levels))
]

# Group and sort the filtered data
filtered_grouped_data = filtered_df.groupby(['Course_Title', 'Grade'])['Matric_Number'].nunique().reset_index(name='Distinct_Students')
filtered_grouped_data = filtered_grouped_data.sort_values(['Course_Title', 'Distinct_Students'], ascending=[True, False])

# Create the grouped horizontal bar chart
fig = go.Figure()

# Loop through each grade and add a trace for each grade
for grade in sorted(filtered_grouped_data['Grade'].unique()):
    grade_data = filtered_grouped_data[filtered_grouped_data['Grade'] == grade]
    fig.add_trace(go.Bar(
        y=grade_data['Course_Title'],
        x=grade_data['Distinct_Students'],
        name=f'Grade {grade}',
        marker_color=grade_colors.get(grade, '#000000'),  # Default color if grade not in dictionary
        orientation='h',
        text=grade_data['Distinct_Students'],
        textposition='outside',  # Ensure text is visible outside of the bars
    ))

# Create a slider to adjust the height of the plot
plot_height = st.slider('Adjust Plot Height for Visibility', min_value=800, max_value=2500, value=1200)

# Update layout to group bars, remove background, and customize axes
fig.update_layout(
    barmode='group',
    xaxis_title='Number of Distinct Students',
    yaxis_title='Course Title',
    yaxis=dict(
        categoryorder='total descending',  # Ensure sorting within each Course_Title
        autorange='reversed'  # Course Titles should be ordered from top to bottom
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
    legend_title='Grade',
    height=plot_height,  # Use height from the slider
    margin=dict(l=50, r=50, t=50, b=50)  # Adjust margins to make space for labels
)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

