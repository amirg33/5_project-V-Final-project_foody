import pandas as pd
import utils


# These are the two Databases that we will be working with
ratings = pd.read_csv("../data/Unprocessed/RAW_interactions.csv") # In this DataFrame we find all the rating we got for the recipes
recipes = pd.read_csv("../data/Unprocessed/RAW_recipes.csv") # In this DataFrame we find all the recipes
def recipes_ratings_merged_cleaned():

    # We will be looking to create another Dataframe from ratings. Main propose is to get for each recipe_id the avg rating and the number of ratings it has
    # Group by 'recipe_id' and aggregate ratings
    recipe_summary = ratings.groupby('recipe_id')['rating'].agg(['mean', 'count'])

    # Round the average ratings to two decimal places
    recipe_summary['mean'] = recipe_summary['mean'].round(2)

    # Rename columns for clarity
    recipe_summary.columns = ['average_rating', 'number_of_ratings']

    # Reset index to make 'recipe_id' a column
    recipe_summary = recipe_summary.reset_index()
    #-------------------------------------------------------------------------------------------------
    # Now that we have the recipe_summary df we will merge this with our recipes df
    # Rename 'id' in recipes DataFrame to 'recipe_id' for a consistent merge key
    recipes.rename(columns={'id': 'recipe_id'}, inplace=True)

    # Merge the DataFrames
    # Using a left merge to keep all recipes and add ratings information where available
    recipes_with_ratings = recipes.merge(recipe_summary, on='recipe_id', how='left')
    # Drop rows where 'name' is NaN or not a string
    recipes_with_ratings = recipes_with_ratings.dropna(subset=['name'])
    # Replace extra spaces with a single space in the 'name' column
    recipes_with_ratings['name'] = recipes_with_ratings['name'].str.replace(r'\s+', ' ', regex=True)

    #Create a url column to get access to the link of the recipe in food.com
    recipes_with_ratings["url"] = ''
    for index, row in recipes_with_ratings.iterrows():
    # Convert 'recipe_id' to string before concatenating
        recipe_id_str = str(row['recipe_id'])
    # Replace spaces with hyphens in 'name' and concatenate with 'recipe_id'
        recipes_with_ratings.at[index, 'url'] = f"https://www.food.com/recipe/{row['name'].replace(' ', '-')}-{recipe_id_str}"

    # Convert the 'tags' column from string to list
    if isinstance(recipes_with_ratings['tags'].iloc[0], str):
        recipes_with_ratings['tags'] = recipes_with_ratings['tags'].apply(lambda x: x.strip('[]').replace("'", '').split(', '))

    # Convert the 'ingredients' column from string to list
    if isinstance(recipes_with_ratings['ingredients'].iloc[0], str):
        recipes_with_ratings['ingredients'] = recipes_with_ratings['ingredients'].apply(lambda x: x.strip('[]').replace("'", '').split(', '))

    # Convert the 'nutrition' column from string to list
    if isinstance(recipes_with_ratings['nutrition'].iloc[0], str):
        recipes_with_ratings['nutrition'] = recipes_with_ratings['nutrition'].apply(lambda x: x.strip('[]').replace("'", '').split(', '))

    # Convert the 'steps' column from string to list
    if isinstance(recipes_with_ratings['steps'].iloc[0], str):
        recipes_with_ratings['steps'] = recipes_with_ratings['steps'].apply(lambda x: x.strip('[]').replace("'", '').split(', '))
    
    # Function to categorize time into intervals
    def categorize_time(minutes):
        if minutes > 90:
            return 'More than 1h 30min'
        else:
            interval = (minutes // 15) * 15
            return f'About {interval} min' if interval != 0 else 'About 15 min'

    # Apply the function to create a new column
    recipes_with_ratings['cooking_time'] = recipes_with_ratings['minutes'].apply(categorize_time)

    # Function to categorize number of ingredients into intervals
    def categorize_ingredients(n_ingredients):
        if n_ingredients <= 5:
            return '0-5'
        elif 5 < n_ingredients <= 10:
            return '5-10'
        elif 10 < n_ingredients <= 20:
            return '10-20'
        elif 20 < n_ingredients <= 30:
            return '20-30'
        elif 30 < n_ingredients <= 40:
            return '30-40'
        else:
            return '> 40'
    
    # Drop columns we do not need for the database.  
    recipes_with_ratings.drop(columns=['contributor_id', 'submitted'], inplace=True)

    # Apply the function to create a new column
    recipes_with_ratings['ingredient_group'] = recipes_with_ratings['n_ingredients'].apply(categorize_ingredients)


    return recipes_with_ratings 
    #utils.nutrition_values(recipes_with_ratings["nutrition"])


def create_nutrition_df(df, nutrition_column, id_column):
    """
    Transforms a DataFrame column containing nutrition information into a new DataFrame
    with separate columns for each nutrient, placing the recipe_id as the first column.

    Parameters:
    df (pd.DataFrame): The original DataFrame.
    nutrition_column (str): The name of the column containing nutrition information.
    id_column (str): The name of the column containing the recipe IDs.

    Returns:
    pd.DataFrame: A new DataFrame with separate columns for each nutrient and the recipe_id as the first column.
    """

    # Define the nutrient names
    nutrients = ['calories', 'total_fat', 'sugar', 'sodium', 'protein', 'saturated_fat', 'carbohydrates']

    # Create a list of dictionaries, each representing a row in the new DataFrame
    nutrition_data = []
    for index, row in df.iterrows():
        # Create a dictionary for the row
        row_data = {id_column: row[id_column]}  # Add recipe_id as the first key-value pair

        # Extract nutrition list
        nutrition_list = row[nutrition_column]
        # Convert string representation of list to actual list (if necessary)
        if isinstance(nutrition_list, str):
            nutrition_list = eval(nutrition_list)

        # Add nutrient values to the row_data
        row_data.update({nutrient: value for nutrient, value in zip(nutrients, nutrition_list)})

        # Append the row_data to the nutrition_data list
        nutrition_data.append(row_data)

    # Create a new DataFrame from the list of dictionaries
    nutrition_df = pd.DataFrame(nutrition_data)

    return nutrition_df


