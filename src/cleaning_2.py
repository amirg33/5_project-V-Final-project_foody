import pandas as pd
import utils


# These are the two Databases that we will be working with
ratings = pd.read_csv("../data/Unprocessed/RAW_interactions.csv") # In this DataFrame we find all the rating we got for the recipes
recipes = pd.read_csv("../data/Unprocessed/RAW_recipes.csv") # In this DataFrame we find all the recipes

def recipes_ratings_merged():

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
    """
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
    """
    #utils.nutrition_values(recipes_with_ratings["nutrition"])

    recipes_with_ratings.to_csv("../data/processed/recipes_with_ratings.csv", index=False) 


def convert_to_list(df):
    # Convert the 'tags' column from string to list
    if isinstance(df['tags'].iloc[0], str):
        df['tags'] = df['tags'].apply(lambda x: x.strip('[]').replace("'", '').split(', '))

    # Convert the 'ingredients' column from string to list
    if isinstance(df['ingredients'].iloc[0], str):
        df['ingredients'] = df['ingredients'].apply(lambda x: x.strip('[]').replace("'", '').split(', '))

    # Convert the 'nutrition' column from string to list
    if isinstance(df['nutrition'].iloc[0], str):
        df['nutrition'] = df['nutrition'].apply(lambda x: x.strip('[]').replace("'", '').split(', '))

    # Convert the 'steps' column from string to list
    if isinstance(df['steps'].iloc[0], str):
        df['steps'] = df['steps'].apply(lambda x: x.strip('[]').replace("'", '').split(', '))
    df.to_csv("../data/processed/recipes_with_ratings_list.csv", index=False) 


import pandas as pd
import utils


# These are the two Databases that we will be working with
ratings = pd.read_csv("../data/Unprocessed/RAW_interactions.csv") # In this DataFrame we find all the rating we got for the recipes
recipes = pd.read_csv("../data/Unprocessed/RAW_recipes.csv") # In this DataFrame we find all the recipes
def cleaned_df():
    def recipes_ratings_merged():

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
        """
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
        """
        #utils.nutrition_values(recipes_with_ratings["nutrition"])

        recipes_with_ratings.to_csv("../data/processed/recipes_with_ratings.csv", index=False) 

    recipes_ratings_merged()
    df = pd.read_csv("../data/Processed/recipes_with_ratings.csv")

    def convert_to_list(df):
        # Convert the 'tags' column from string to list
        if isinstance(df['tags'].iloc[0], str):
            df['tags'] = df['tags'].apply(lambda x: x.strip('[]').replace("'", '').split(', '))

        # Convert the 'ingredients' column from string to list
        if isinstance(df['ingredients'].iloc[0], str):
            df['ingredients'] = df['ingredients'].apply(lambda x: x.strip('[]').replace("'", '').split(', '))

        # Convert the 'nutrition' column from string to list
        if isinstance(df['nutrition'].iloc[0], str):
            df['nutrition'] = df['nutrition'].apply(lambda x: x.strip('[]').replace("'", '').split(', '))

        # Convert the 'steps' column from string to list
        if isinstance(df['steps'].iloc[0], str):
            df['steps'] = df['steps'].apply(lambda x: x.strip('[]').replace("'", '').split(', '))
        df.to_csv("../data/processed/recipes_with_ratings.csv", index=False) 
    convert_to_list(df)