import cleaning
import utils
import pandas as pd
import cleaning
import ast              # Change lists that are strings to actual lists
import re
import numpy as np

df = cleaning.recipes_ratings_merged_cleaned()

def exploration_of_data():
    
    #df.to_json("../data/processed/recipes_with_ratings.json", index=False)
    #df = pd.read_json("../data/Processed/recipes_with_ratings.json")

    # Converting columns in the DataFrame from string representation to actual lists.

    #df.to_csv("../data/processed/recipes_with_ratings.csv", index=False)
    #df = pd.read_csv("../data/Processed/recipes_with_ratings.csv")
    
    df.tags = df.tags.map(lambda x: ast.literal_eval(x))
    df.steps = df.steps.map(lambda x: ast.literal_eval(x))
    df.ingredients = df.ingredients.map(lambda x: ast.literal_eval(x))
    df.nutrition = df.nutrition.map(lambda x: ast.literal_eval(x))

    # Call the ingredients function rom utils, in order to get all ingredients in a list. 
    ingredients_list = utils.aggregate_unique_lists(df, 'ingredients')
    # Save the ingredients into a csv file for later usage
    ingredients_list.to_csv("../data/Processed/ingredients_list.csv")

    # Creating a nutrition DataFrame by extracting and formatting nutrition data.
    nutrition_df = cleaning.create_nutrition_df(df, 'nutrition', 'recipe_id')
    nutrition_df.to_csv("../data/Processed/nutrition_df.csv")

    



