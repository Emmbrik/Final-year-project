import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
@st.cache_data
def load_data(sheet_name):
    data = pd.read_excel('Data/Student_Data.xlsx', sheet_name=sheet_name)
    return data

# List of sheets in the Excel file
sheets = ['Registration', 'Biodata', 'Result_Sheet', 'Academic_Performance', 'First_and_Last_Result']

# Sidebar to select sheet
st.sidebar.title('Select Sheet')
selected_sheet = st.sidebar.selectbox('Sheet Name', sheets)

# Load data from the selected sheet
data = load_data(selected_sheet)

# Title and description
st.title('Student Academic Performance Visualization')
st.write(f"""
This web application visualizes the academic performance of students from the {selected_sheet} sheet.
You can explore different aspects of the data through various charts.
""")

# Display the raw data
if st.checkbox('Show raw data'):
    st.subheader('Raw Data')
    st.write(data)

# Display basic statistics
if st.checkbox('Show Basic Statistics'):
    st.subheader('Basic Statistics')
    st.write(data.describe(include='all'))

# Histogram of grades
st.subheader('Distribution of Grades')
grade_columns = data.select_dtypes(include=['number']).columns.tolist()
if grade_columns:
    grade_column = st.selectbox('Select grade column', grade_columns)
    fig, ax = plt.subplots()
    sns.histplot(data[grade_column], kde=True, ax=ax)
    ax.set_title(f'Distribution of {grade_column}')
    st.pyplot(fig)
else:
    st.write("No numerical columns available for histogram.")

# Correlation heatmap
st.subheader('Correlation Heatmap')
if len(grade_columns) > 1:
    fig, ax = plt.subplots()
    sns.heatmap(data[grade_columns].corr(), annot=True, cmap='coolwarm', ax=ax)
    ax.set_title('Correlation Heatmap')
    st.pyplot(fig)
else:
    st.write("Not enough numerical columns for correlation heatmap.")

# Scatter plot for two selected variables
st.subheader('Scatter Plot')
if len(data.columns) > 1:
    x_var = st.selectbox('Select x-axis variable', data.columns)
    y_var = st.selectbox('Select y-axis variable', data.columns)
    fig, ax = plt.subplots()
    sns.scatterplot(x=data[x_var], y=data[y_var], ax=ax)
    ax.set_title(f'Scatter Plot of {x_var} vs {y_var}')
    st.pyplot(fig)
else:
    st.write("Not enough columns for scatter plot.")

# Box plot for a selected categorical variable
st.subheader('Box Plot')
cat_vars = data.select_dtypes(include=['object']).columns.tolist()
num_vars = data.select_dtypes(include=['number']).columns.tolist()
if cat_vars and num_vars:
    cat_var = st.selectbox('Select categorical variable', cat_vars)
    num_var = st.selectbox('Select numerical variable', num_vars)
    fig, ax = plt.subplots()
    sns.boxplot(x=data[cat_var], y=data[num_var], ax=ax)
    ax.set_title(f'Box Plot of {num_var} by {cat_var}')
    st.pyplot(fig)
else:
    st.write("Not enough categorical or numerical columns for box plot.")
