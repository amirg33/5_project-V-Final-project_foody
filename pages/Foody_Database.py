import streamlit as st
import pandas as pd
import src.utils as ut
import src.recipe_matcher as rm

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/recipes_with_ratings_restrictions.csv")

@st.cache_data
def get_ingredients_list(df):
    return ut.aggregate_unique_lists(df, 'ingredients')

st.title('Foody - Database')

df = load_data()
ingredients_list = get_ingredients_list(df)

st.header("Select Restrictions")
selected_restrictions = st.multiselect(
    "Choose your restrictions:",
    options=["Dairy-Free", "Gluten-Free", "Nuts", "Vegetarian", "Vegan"],
    default=None,
    help="Start typing to see suggestions"
)

st.header("Select Ingredients")
selected_ingredients = st.multiselect(
    "Choose your ingredients:",
    options=ingredients_list,
    default=None,
    help="Start typing to see suggestions"
)

st.header("Select Ingredients you do not want to include")
selected_ingredients_not_wanted = st.multiselect(
    "Choose your ingredients you do not want to include:",
    options=ingredients_list,
    default=None,
    help="Start typing to see suggestions"
)

if st.button('Find Your Recipes'):
    df_filtered = rm.All_restrictions_list(df, 
                                           restrictions=selected_restrictions, 
                                           ingredients_list=ingredients_list, 
                                           required_ingredients=selected_ingredients, 
                                           excluded_ingredients=selected_ingredients_not_wanted)

    st.header("Filtered Recipes")
    st.dataframe(df_filtered)
