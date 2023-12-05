import streamlit as st
import pandas as pd
import src.utils as ut
import src.recipe_matcher as rm
import ast

st.set_page_config(page_title="Recipe ", page_icon=":film_frames:", layout="wide")
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
def load_steps():
    df = pd.read_csv("data/Processed/df_streamlit/df_recipes_final_steps.csv")
    df.steps = df.steps.map(lambda x: ast.literal_eval(x))
    return df

@st.cache_data
def load_tags():
    df = pd.read_csv("data/Processed/df_streamlit/df_recipes_final_tags.csv")
    df.tags = df.tags.map(lambda x: ast.literal_eval(x))
    return df

# Load all dataframes
df = load_data()
df_descriptions = load_descriptions()
df_nutrition = load_nutrition()
df_steps = load_steps()
df_tags = load_tags()

@st.cache_data
def get_ingredients_list():
    # Sort the ingredients list in ascending order
    # Remove elements enclosed in double quotes

    ingredients_list = ut.strip_string(sorted(ut.aggregate_unique_lists(df, 'ingredients')))
    return ingredients_list

ingredients_list = get_ingredients_list()

st.title('Foody: Your recipe generator')

selected_restrictions = st.multiselect(
    "Choose your restrictions:",
    options=["Dairy-Free", "Gluten-Free", "Nuts-Free", "Vegetarian", "Vegan"],
    default=None,
    help="Start typing to see suggestions"
)
selected_ingredients = st.multiselect(
    "Choose your ingredients:",
    options=ingredients_list,
    default=None,
    help="Start typing to see suggestions"
)
selected_ingredients_not_wanted = st.multiselect(
    "Choose your ingredients you do not want to include:",
    options=ingredients_list,
    default=None,
    help="Start typing to see suggestions"
)

# Mapping between user-facing terms and DataFrame terms
restrictions_mapping = {
    "Dairy-Free": "Dairy",
    "Gluten-Free": "Gluten",
    "Nuts-Free": "Nuts",  
    "Vegetarian": "Vegetarian",
    "Vegan": "Vegan"
}

# Convert selected restrictions to DataFrame terms
selected_restrictions_df_terms = [restrictions_mapping[restriction] for restriction in selected_restrictions]

# Slider to select the number of recipes to display
num_recipes = st.slider("Select the number of recipes to display", 1, 100, 100)

# Then use these terms in your filter function
if st.button('Find Your Recipes'):
    df_filtered = rm.All_restrictions_list(df, 
                                           restrictions=selected_restrictions_df_terms, 
                                           ingredients_list=ingredients_list, 
                                           required_ingredients=selected_ingredients, 
                                           excluded_ingredients=selected_ingredients_not_wanted)
    
     # Extract unique cooking times from the filtered DataFrame
    unique_cooking_times = df_filtered['cooking_time'].unique()

    # Sidebar multiselect for cooking time
    selected_cooking_times = st.sidebar.multiselect(
        'Select Cooking Time',
        options=unique_cooking_times,
        default=None
    )

    # Button to apply the additional filter
    if st.sidebar.button('Apply Cooking Time Filter'):
        # Further filter df_filtered based on selected cooking times
        if selected_cooking_times:
            df_filtered = df_filtered[df_filtered['cooking_time'].isin(selected_cooking_times)]

    st.header("Filtered Recipes:")


     # Iterate over each row in the filtered DataFrame
    for index, row in df_filtered.head(num_recipes).iterrows():
        st.markdown(f"<h2 style='color: {streamlit_red_color}; font-size: {subheader_font_size};'>{row['name'].upper()}</h2>", unsafe_allow_html=True)

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
        with col2.expander("Show Nutrition Information"):
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

        col2.markdown(f"For more information about the Recipe, visit this [link]({url})")
