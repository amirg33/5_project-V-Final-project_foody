import pandas as pd

def recipes_ratings_merged(ratings_path, recipes_path):
    # Read data from CSV files
    ratings = pd.read_csv(ratings_path)
    recipes = pd.read_csv(recipes_path)

    # Create a summary DataFrame with average rating and number of ratings per recipe
    recipe_summary = ratings.groupby('recipe_id')['rating'].agg(['mean', 'count'])
    recipe_summary['mean'] = recipe_summary['mean'].round(2)
    recipe_summary.columns = ['average_rating', 'number_of_ratings']
    recipe_summary = recipe_summary.reset_index()

    # Prepare the recipes DataFrame for merging
    recipes.rename(columns={'id': 'recipe_id'}, inplace=True)

    # Merge the DataFrames
    recipes_with_ratings = recipes.merge(recipe_summary, on='recipe_id', how='left')

    # Drop rows where 'name' is NaN or not a string
    recipes_with_ratings = recipes_with_ratings.dropna(subset=['name'])

    # Replace extra spaces with a single space in the 'name' column
    recipes_with_ratings['name'] = recipes_with_ratings['name'].str.replace(r'\s+', ' ', regex=True)

    # Create URL column
    recipes_with_ratings["url"] = recipes_with_ratings.apply(
        lambda row: f"https://www.food.com/recipe/{row['name'].replace(' ', '-')}-{row['recipe_id']}", axis=1)

    return recipes_with_ratings

def convert_to_list(df, columns):
    for column in columns:
        if df[column].dtype == 'object':
            df[column] = df[column].apply(lambda x: x.strip('[]').replace("'", '').split(', ') if isinstance(x, str) else x)
    return df

def cleaned_df():
    # Paths to the datasets
    ratings_path = "../data/Unprocessed/RAW_interactions.csv"
    recipes_path = "../data/Unprocessed/RAW_recipes.csv"

    # Merge and clean dataframes
    recipes_with_ratings = recipes_ratings_merged(ratings_path, recipes_path)

    # Convert columns to lists
    columns_to_convert = ['tags', 'ingredients', 'nutrition', 'steps']
    recipes_with_ratings = convert_to_list(recipes_with_ratings, columns_to_convert)

    # Save the cleaned dataframe
    recipes_with_ratings.to_csv("../data/processed/recipes_with_ratings.csv", index=False)

# Execute the function
cleaned_df()
