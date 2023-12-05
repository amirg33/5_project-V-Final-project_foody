import pandas as pd
import ast


df = pd.read_csv("../data/Processed/df_recipes_final.csv")
df.tags = df.tags.map(lambda x: ast.literal_eval(x))
df.steps = df.steps.map(lambda x: ast.literal_eval(x))
df.ingredients = df.ingredients.map(lambda x: ast.literal_eval(x))
df.nutrition = df.nutrition.map(lambda x: ast.literal_eval(x))
df.restrictions = df.restrictions.map(lambda x: ast.literal_eval(x))
"""
Index(['name', 'recipe_id', 'minutes', 'tags', 'nutrition', 'n_steps', 'steps',
       'description', 'ingredients', 'n_ingredients', 'average_rating',
       'number_of_ratings', 'url', 'cooking_time', 'ingredient_group',
       'weighted_rating', 'restrictions'],
      dtype='object')
    
"""

def split_dataframe_columns(df, columns_to_split):
    """
    Splits specified columns from the original DataFrame into separate DataFrames, each with 'recipe_id'.
    The specified columns and 'nutrition' column are dropped from the original DataFrame.

    Parameters:
    df (pandas.DataFrame): The original DataFrame.
    columns_to_split (list): List of column names to split into separate DataFrames.

    Returns:
    dict: A dictionary containing the modified original DataFrame and new DataFrames for each specified column.
    """
    new_dfs = {}

    # Create new DataFrames for each specified column
    for column in columns_to_split:
        new_dfs[f"df_{column}"] = df[['recipe_id', column]].copy()

    # Drop specified columns and 'nutrition' from the original DataFrame
    df = df.drop(columns=columns_to_split + ['nutrition'])

    # Add the modified original DataFrame to the dictionary
    new_dfs['original_df'] = df

    return new_dfs

# Usage example
df = pd.read_csv('path_to_your_csv_file.csv') # Load your DataFrame
columns_to_extract = ['tags', 'steps', 'description']
result_dfs = split_dataframe_columns(df, columns_to_extract)

# Access the modified original DataFrame
modified_df = result_dfs['original_df']

# Access the new DataFrames
df_tags = result_dfs['df_tags']
df_steps = result_dfs['df_steps']
df_description = result_dfs['df_description']
