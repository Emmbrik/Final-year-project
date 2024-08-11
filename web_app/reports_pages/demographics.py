import streamlit as st
from data_loader import load_data

# Loading the data
data = load_data()

st.title("Students' Demographics Report")

st.markdown("""

#### Welcome to the Students' Demographics Page.

This Page provides a comprehensive overview of the student population, 
offering valuable insights into various demographic attributes. Here, you 
will find detailed statistics on key aspects of the student body, including:

1. **Number of Students by State of Origin**: Discover the geographic diversity of 
            student population, with data on the number of students from each state.

2. **Total Number of Registered Students**: View the overall number of students who 
            have been enrolled.

3. **Total Number of Students with Biodata**: See how many students have 
            complete biodata information.

4. **Total Number of Graduated Students**: Track the number of students who have 
            successfully completed their studies.

5. **Number of Students by Gender (based on Biodata)**: Explore the gender 
            distribution of students based on the available biodata.

6. **Number of Students by Nationality**: Gain insights into the international 
            composition of our student community, with data on the number of 
            students from different countries.

7. **Number of Students by Marital Status**: Analyze the marital status of 
            students to better understand their demographics.

8. **Number of Students by Religion**: Understand the religious diversity within 
            the student population.

This demographic data helps us better understand the composition of the student body, 
ensuring that we can tailor our programs and services to meet the needs of our diverse 
community. Explore the dashboard to gain further insights into these key demographic areas.
""")


# Visualizations
st.write("# Data Visualizations")
st.write("This is where the visualizations and detailed analysis will be displayed.")




def app(data):
    st.title("Student Demographics")
    st.write("Welcome to the Students Demographics Report")

    st.write(data['Biodata'])
