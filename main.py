import streamlit as st
import pandas as pd
import streamlit_pandas as sp
import numpy as np
import pages.Recommendation  


st.title('Foody - Recipe Generator introduction')


# Introduction text
st.write("""
Welcome to the Recipe Recommender! This app helps you find delicious recipes based on your preferences. Whether you're looking for something healthy, quick, or to satisfy a specific craving, we've got you covered. Let's get started!
""")


# Navigation (to switch between different pages)
st.sidebar.title("Pages")
page = st.sidebar.radio("Go to", ["Introduction", "Recommender"])


# Load the appropriate page
if page == "Introduction":
    st.write("Welcome to the Introduction page.")
elif page == "Recommender":
    pages.Recommendation.show()  # Function to show the page
