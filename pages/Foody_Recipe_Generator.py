import streamlit as st
import pandas as pd
import src.utils as ut
import src.recipe_matcher as rm
import ast

st.set_page_config(page_title="Recipe ", page_icon="🔍", layout="wide")
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

# Load all dataframes
df = load_data()
df_descriptions = load_descriptions()
df_nutrition = load_nutrition()
df_steps = load_steps("data/Processed/df_streamlit/df_recipes_final_steps_part1.csv", 
                      "data/Processed/df_streamlit/df_recipes_final_steps_part2.csv")
df_tags = load_tags()
# Mapping between user-facing terms and DataFrame terms
restrictions_mapping = {
    "Dairy-Free": "Dairy",
    "Gluten-Free": "Gluten",
    "Nuts-Free": "Nuts",  
    "Vegetarian": "Vegetarian",
    "Vegan": "Vegan"
}

@st.cache_data
def get_ingredients_list():
    # Sort the ingredients list in ascending order
    # Remove elements enclosed in double quotes

    ingredients_list = ut.strip_string(sorted(ut.aggregate_unique_lists(df, 'ingredients')))
    return ingredients_list

ingredients_list = get_ingredients_list()
common_ingredients = ut.load_common_ingredients(ingredients_list)


st.title('Foody: Your recipe generator')
st.title('')

col1, col2 = st.columns(2)

with col1:
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
    enable_partial_matches  = st.checkbox(
        "Exclude all other ingredients", 
        value=True,
        help="As you know there are typical ingredient that you usually have in your household, this takes into account that you have those ingredients. Some examples are: Salt, Pepper, all-purpose flour, baking powder, spices, etc. "
        )

    selected_ingredients_not_wanted = st.multiselect(
        "Choose your ingredients you do not want to include:",
        options=ingredients_list,
        default=None,
        help="Start typing to see suggestions"
    )

with col2:
    # Set the minimum cooking time, defaulting to 0 if the min is NaN
    min_cooking_time = int(df['minutes'].min() or 0)

    # Set the maximum cooking time to the lesser of the dataset max or 480 minutes
    max_cooking_time_in_dataset = int(df['minutes'].max() or 0)
    max_cooking_time = min(max_cooking_time_in_dataset, 480)

    # Slider for maximum cooking time, limited to 8 hours (480 minutes)
    selected_max_cooking_time = st.slider(
        'Select Maximum Cooking Time (minutes)',
        min_value=min_cooking_time,
        max_value=max_cooking_time,
        value=max_cooking_time  # Default to the set max value
    )
    num_recipes = st.slider("Select the number of recipes to display", 1, 100, 100)



# Convert selected restrictions to DataFrame terms
selected_restrictions_df_terms = [restrictions_mapping[restriction] for restriction in selected_restrictions]

# Slider to select the number of recipes to display

# Then use these terms in your filter function
if st.button('Find Your Recipes'):
    df_filtered = rm.All_restrictions_list(df, 
                                           restrictions=selected_restrictions_df_terms, 
                                           ingredients_list=ingredients_list, 
                                           required_ingredients=selected_ingredients, 
                                           excluded_ingredients=selected_ingredients_not_wanted,
                                           use_partial_matches=enable_partial_matches,
                                           common_ingredients=common_ingredients)

    df_filtered = df_filtered[df_filtered['minutes'] <= selected_max_cooking_time]

    if df_filtered.empty:
        st.subheader("No recipes found")
        st.image("./images/no_recipes.gif") 
    else:
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

