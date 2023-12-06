import streamlit as st
import pandas as pd
import src.utils as ut
import src.recipe_matcher as rm
import ast
import random as random

# Page Configuration
st.set_page_config(page_title="Random Recipe Selector", page_icon="🔍", layout="wide")
streamlit_red_color = "#FF4B4B"
subheader_font_size = "24px"

@st.cache_data
def load_data():
    df = pd.read_csv("data/Processed/df_streamlit/df_recipes_final_filtered_dropped.csv")
    df.ingredients = df.ingredients.map(lambda x: ast.literal_eval(x))
    df.restrictions = df.restrictions.map(lambda x: ast.literal_eval(x))
    return df

@st.cache_data
def load_descriptions():
    df = pd.read_csv("data/Processed/df_streamlit/df_recipes_final_description.csv")
    return df

@st.cache_data
def load_nutrition():
    df = pd.read_csv("data/Processed/df_streamlit/df_recipes_final_nutrition.csv")
    return df

@st.cache_data
def load_steps(file_path1, file_path2):
    """
    Loads and merges two parts of a DataFrame from CSV files.

    Parameters:
    file_path1 (str): The file path for the first part.
    file_path2 (str): The file path for the second part.

    Returns:
    pd.DataFrame: The merged DataFrame.
    """
    df_part1 = pd.read_csv(file_path1)
    df_part2 = pd.read_csv(file_path2)

    df_part1.steps = df_part1.steps.map(lambda x: ast.literal_eval(x))
    df_part2.steps = df_part2.steps.map(lambda x: ast.literal_eval(x))

    return pd.concat([df_part1, df_part2])

@st.cache_data
def load_tags():
    df = pd.read_csv("data/Processed/df_streamlit/df_recipes_final_tags.csv")
    df.tags = df.tags.map(lambda x: ast.literal_eval(x))
    return df

# Load dataframes
df = load_data()
df_descriptions = load_descriptions()
df_nutrition = load_nutrition()
df_steps = load_steps("data/Processed/df_streamlit/df_recipes_final_steps_part1.csv", 
                      "data/Processed/df_streamlit/df_recipes_final_steps_part2.csv")
df_tags = load_tags()

st.title('Random Recipe Selector')

# Slider for preparation time
min_cooking_time, max_cooking_time = st.slider(
    'Select Preparation Time Range (minutes)',
    0, 480, (0, 480)
)

# Button to find random recipes
if st.button('Choose Random Recipe'):
    # Filter recipes based on selected preparation time
    filtered_recipes = df[(df['minutes'] >= min_cooking_time) & (df['minutes'] <= max_cooking_time)]

    # Select random recipes
    random_recipes = filtered_recipes.sample(n=min(10, len(filtered_recipes)))

    # Display recipes
    for index, row in random_recipes.iterrows():
        st.markdown(f"<h2 style='color: {streamlit_red_color}; font-size: {subheader_font_size};'>{row['name'].upper()}</h2>", unsafe_allow_html=True)
        st.write(f"Preparation Time: {row['minutes']} minutes")
        # Additional recipe details (ingredients, description, etc.) can be added here

        col1, col2 = st.columns(2)
        
        # Display the capitalized 'name' in the first column

        # Display the ingredients with label
        col1.markdown("**Ingredients:**")
        ingredients_str = ', '.join(row['ingredients']).capitalize()
        col1.write(ingredients_str)

        # Display the preparation time
        col1.markdown(f"**Preparation Time:**")
        col1.write(f"{row['minutes']} min")

        # Get the corresponding description from df_descriptions using recipe_id
        description = df_descriptions[df_descriptions['recipe_id'] == row['recipe_id']]['description'].iloc[0]
        capitalized_description = ut.capitalize_after_period(description)

        # Display the description
        col1.markdown("**Description:**")
        col1.write(capitalized_description)

        # Get the corresponding steps from df_steps using recipe_id
        steps = df_steps[df_steps['recipe_id'] == row['recipe_id']]['steps'].iloc[0]
        nutrition_data = df_nutrition[df_nutrition['recipe_id'] == row['recipe_id']].iloc[0]
        tags = df_tags[df_tags['recipe_id'] == row['recipe_id']]['tags'].iloc[0]
        url = row['url']  


        # Using an expander for steps
        with col2.expander(f"Show Steps ({row['n_steps']})"):
            for step_num, step in enumerate(steps, start=1):
                st.write(f"{step_num}. {step.capitalize()}")

        # Using an expander for Nutrition information
        with col2.expander("Show Nutrition Information per serving"):
            st.write(f"Calories: {nutrition_data['calories']}")
            st.write(f"Total Fat: {nutrition_data['total_fat']}g")
            st.write(f"Sugar: {nutrition_data['sugar']}g")
            st.write(f"Sodium: {nutrition_data['sodium']}mg")
            st.write(f"Protein: {nutrition_data['protein']}g")
            st.write(f"Saturated Fat: {nutrition_data['saturated_fat']}g")
            st.write(f"Carbohydrates: {nutrition_data['carbohydrates']}g")

        # Using an expander for Tags
        with col2.expander(f"Show Tags ({len(tags)})"):
            for tag in tags:
                st.write(f"#{tag}")

        col2.markdown(f"For more information and pictures about the Recipe, visit this [LINK]({url})")
